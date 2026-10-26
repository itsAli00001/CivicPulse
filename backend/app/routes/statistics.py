from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories.complaint_repository import ComplaintRepository
from app.services.complaint_service import ComplaintService


router = APIRouter(
    prefix="/api/statistics",
    tags=["Statistics"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_service(
    db: Session = Depends(get_db)
):
    repository = ComplaintRepository(db)
    return ComplaintService(repository)


@router.get("")
def get_statistics(
    response: Response,
    service: ComplaintService = Depends(get_service)
):
    statistics, cache_status = service.get_statistics()

    response.headers["X-Cache"] = cache_status

    return statistics