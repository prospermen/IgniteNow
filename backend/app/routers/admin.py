import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Drama, Episode, HighlightEvent
from ..schemas import (
    AnalyzeRequest,
    DramaCreate,
    DramaOut,
    EpisodeCreate,
    EpisodeOut,
    HighlightBulkStatusUpdate,
    HighlightCreate,
    HighlightOut,
    HighlightUpdate,
)
from ..services.highlight_service import (
    apply_highlight_update,
    assert_no_published_overlap,
    create_highlight,
)
from .common import ok, require_admin

router = APIRouter()


@router.get("/dramas", dependencies=[Depends(require_admin)])
def list_dramas(db: Session = Depends(get_db)):
    return ok([DramaOut.model_validate(item).model_dump() for item in db.query(Drama).order_by(Drama.id.desc()).all()])


@router.post("/dramas", dependencies=[Depends(require_admin)])
def create_drama(payload: DramaCreate, db: Session = Depends(get_db)):
    drama = Drama(**payload.model_dump())
    db.add(drama)
    db.commit()
    db.refresh(drama)
    return ok(DramaOut.model_validate(drama).model_dump(), "drama created")


@router.get("/episodes", dependencies=[Depends(require_admin)])
def list_episodes(drama_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Episode)
    if drama_id:
        query = query.filter(Episode.drama_id == drama_id)
    episodes = query.order_by(Episode.id.desc()).all()
    return ok([EpisodeOut.model_validate(item).model_dump() for item in episodes])


@router.post("/episodes", dependencies=[Depends(require_admin)])
def create_episode(payload: EpisodeCreate, db: Session = Depends(get_db)):
    if not db.get(Drama, payload.drama_id):
        raise HTTPException(status_code=404, detail="drama not found")
    episode = Episode(**payload.model_dump())
    db.add(episode)
    db.commit()
    db.refresh(episode)
    return ok(EpisodeOut.model_validate(episode).model_dump(), "episode created")


@router.post("/episodes/{episode_id}/analyze", dependencies=[Depends(require_admin)])
def analyze_episode(episode_id: int, payload: AnalyzeRequest | None = None, db: Session = Depends(get_db)):
    payload = payload or AnalyzeRequest()
    episode = db.get(Episode, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="episode not found")
    if episode.analyze_status == "processing":
        raise HTTPException(status_code=409, detail="episode is already processing")
    if not (episode.subtitle_content or episode.subtitle_url):
        episode.analyze_status = "failed"
        episode.analyze_error = "subtitle is required"
        db.commit()
        raise HTTPException(status_code=400, detail="subtitle is required")

    existing = db.query(HighlightEvent).filter(HighlightEvent.episode_id == episode_id).count()
    if existing and episode.analyze_status == "success" and not payload.force_reanalyze:
        return ok({"highlight_count": existing}, "existing highlights returned")

    episode.analyze_status = "processing"
    episode.analyze_error = ""
    db.commit()

    try:
        repo_root = Path(__file__).resolve().parents[3]
        sys.path.insert(0, str(repo_root))
        from ai_service.highlight_analyzer import analyze_subtitle_text

        result = analyze_subtitle_text(episode.subtitle_content or episode.subtitle_url or "")
        if payload.force_reanalyze:
            db.query(HighlightEvent).filter(HighlightEvent.episode_id == episode_id).delete()

        created: list[HighlightEvent] = []
        invalid_reasons: list[str] = []
        for item in result["highlights"]:
            try:
                highlight = create_highlight(db, episode, item)
            except ValueError as exc:
                invalid_reasons.append(str(exc))
                continue
            created.append(highlight)

        episode.analyze_status = "success"
        episode.analyze_error = "; ".join(invalid_reasons[:3])
        db.commit()
        return ok(
            {
                "highlight_count": len(created),
                "provider": result.get("provider", "unknown"),
                "llm_error": result.get("llm_error", ""),
                "invalid_count": len(invalid_reasons),
            },
            "analysis completed",
        )
    except Exception as exc:
        episode.analyze_status = "failed"
        episode.analyze_error = str(exc)
        db.commit()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/episodes/{episode_id}/highlights", dependencies=[Depends(require_admin)])
def list_highlights(episode_id: int, db: Session = Depends(get_db)):
    highlights = db.query(HighlightEvent).filter(HighlightEvent.episode_id == episode_id).order_by(HighlightEvent.start_time).all()
    return ok([HighlightOut.model_validate(item).model_dump() for item in highlights])


@router.post("/episodes/{episode_id}/highlights", dependencies=[Depends(require_admin)])
def add_highlight(episode_id: int, payload: HighlightCreate, db: Session = Depends(get_db)):
    episode = db.get(Episode, episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="episode not found")
    try:
        highlight = create_highlight(db, episode, payload)
        db.flush()
        if highlight.status == "published":
            assert_no_published_overlap(db, episode_id, [highlight])
        db.commit()
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    db.refresh(highlight)
    return ok(HighlightOut.model_validate(highlight).model_dump(), "highlight created")


@router.put("/highlights/{highlight_id}", dependencies=[Depends(require_admin)])
def update_highlight(highlight_id: int, payload: HighlightUpdate, db: Session = Depends(get_db)):
    highlight = db.get(HighlightEvent, highlight_id)
    if not highlight:
        raise HTTPException(status_code=404, detail="highlight not found")
    try:
        apply_highlight_update(highlight, payload, highlight.episode)
        if highlight.status == "published":
            assert_no_published_overlap(db, highlight.episode_id, [highlight])
        db.commit()
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    db.refresh(highlight)
    return ok(HighlightOut.model_validate(highlight).model_dump(), "highlight updated")


@router.delete("/highlights/{highlight_id}", dependencies=[Depends(require_admin)])
def archive_highlight(highlight_id: int, db: Session = Depends(get_db)):
    highlight = db.get(HighlightEvent, highlight_id)
    if not highlight:
        raise HTTPException(status_code=404, detail="highlight not found")
    highlight.status = "archived"
    db.commit()
    db.refresh(highlight)
    return ok(HighlightOut.model_validate(highlight).model_dump(), "highlight archived")


@router.post("/episodes/{episode_id}/highlights/bulk-status", dependencies=[Depends(require_admin)])
def bulk_update_highlight_status(episode_id: int, payload: HighlightBulkStatusUpdate, db: Session = Depends(get_db)):
    if payload.status not in {"draft", "published", "rejected", "archived"}:
        raise HTTPException(status_code=400, detail="illegal status")
    query = db.query(HighlightEvent).filter(HighlightEvent.episode_id == episode_id)
    if payload.highlight_ids is not None:
        query = query.filter(HighlightEvent.id.in_(payload.highlight_ids))
    highlights = query.all()
    if payload.highlight_ids is not None and len(highlights) != len(set(payload.highlight_ids)):
        raise HTTPException(status_code=404, detail="some highlights not found for episode")
    for item in highlights:
        item.status = payload.status
    try:
        if payload.status == "published":
            assert_no_published_overlap(db, episode_id, highlights)
        db.commit()
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ok({"updated_count": len(highlights), "status": payload.status}, "highlight status updated")


@router.post("/episodes/{episode_id}/highlights/publish", dependencies=[Depends(require_admin)])
def publish_highlights(episode_id: int, db: Session = Depends(get_db)):
    highlights = db.query(HighlightEvent).filter(HighlightEvent.episode_id == episode_id, HighlightEvent.status == "draft").all()
    for item in highlights:
        item.status = "published"
    try:
        assert_no_published_overlap(db, episode_id, highlights)
        db.commit()
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ok({"published_count": len(highlights)}, "highlights published")
