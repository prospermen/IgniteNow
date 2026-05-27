from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Episode, Job, JobLog
from ..schemas import JOB_TYPES, JobCreate, JobLogOut, JobOut
from ..services.auth_service import ADMIN_ROLE, UPLOADER_ROLE
from ..services.job_service import create_and_enqueue_job, retry_job
from .common import ok, require_roles

router = APIRouter(prefix="/system")
require_workspace_user = require_roles(ADMIN_ROLE, UPLOADER_ROLE)


def _job_out(job: Job) -> dict:
    return JobOut.model_validate(job).model_dump()


@router.get("/jobs", dependencies=[Depends(require_workspace_user)])
def list_jobs(
    status: str | None = None,
    type: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    if type:
        query = query.filter(Job.type == type)
    jobs = query.order_by(Job.id.desc()).limit(min(max(limit, 1), 200)).all()
    return ok([_job_out(item) for item in jobs])


@router.post("/jobs", dependencies=[Depends(require_workspace_user)])
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    if payload.type not in JOB_TYPES:
        raise HTTPException(status_code=400, detail="unsupported job type")
    if payload.type != "ai_analyze":
        raise HTTPException(status_code=400, detail="job type is not implemented yet")
    episode_id = payload.payload.get("episode_id")
    if not isinstance(episode_id, int):
        raise HTTPException(status_code=400, detail="payload.episode_id is required")
    if not db.get(Episode, episode_id):
        raise HTTPException(status_code=404, detail="episode not found")
    try:
        job = create_and_enqueue_job(db, payload.type, payload.payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"failed to enqueue job: {exc}") from exc
    return ok(_job_out(job), "job queued")


@router.get("/jobs/{job_id}", dependencies=[Depends(require_workspace_user)])
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return ok(_job_out(job))


@router.get("/jobs/{job_id}/logs", dependencies=[Depends(require_workspace_user)])
def list_job_logs(job_id: int, db: Session = Depends(get_db)):
    if not db.get(Job, job_id):
        raise HTTPException(status_code=404, detail="job not found")
    logs = db.query(JobLog).filter(JobLog.job_id == job_id).order_by(JobLog.id.asc()).all()
    return ok([JobLogOut.model_validate(item).model_dump() for item in logs])


@router.post("/jobs/{job_id}/retry", dependencies=[Depends(require_workspace_user)])
def retry_failed_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    try:
        retry = retry_job(db, job)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"failed to enqueue job: {exc}") from exc
    return ok(_job_out(retry), "job retried")
