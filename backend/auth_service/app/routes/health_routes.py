from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.db import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
def liveness():
    """Liveness: the process is up. No external dependencies checked."""
    return {"status": "ok"}


@router.get("/health/ready")
def readiness(db: Session = Depends(get_db)):
    """Readiness: the service can reach its database and serve traffic."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "detail": "database unavailable"},
        )
