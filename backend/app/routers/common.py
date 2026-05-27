from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..services.auth_service import ADMIN_ROLE, security, user_from_token


def require_admin(
    x_admin_token: str | None = Header(default=None),
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
):
    if x_admin_token != settings.admin_token:
        if not credentials:
            raise HTTPException(status_code=403, detail="invalid admin token")
        user = user_from_token(credentials.credentials, db)
        if user.role != ADMIN_ROLE:
            raise HTTPException(status_code=403, detail="admin role required")


def ok(data=None, message="ok"):
    return {"success": True, "message": message, "data": data}
