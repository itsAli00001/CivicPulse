
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.complaint import Complaint
from app.repositories.complaint_repository import ComplaintRepository
from app.schemas.complaint import ComplaintCreate
from app.services.complaint_service import ComplaintService


router = APIRouter(prefix="/api/complaints", tags=["Complaints"])


class ComplaintStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in {"open", "in_progress", "resolved", "rejected"}:
            raise ValueError("Invalid complaint status")
        return value


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db: Session = Depends(get_db)):
    repository = ComplaintRepository(db)
    return ComplaintService(repository)


@router.post("")
def create_complaint(
    complaint: ComplaintCreate,
    service: ComplaintService = Depends(get_service)
):
    return service.create_complaint(complaint)


@router.get("/{complaint_id}")
def get_complaint(
    complaint_id: UUID,
    service: ComplaintService = Depends(get_service)
):
    complaint = service.get_complaint(complaint_id)

    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    return complaint


@router.get("")
def get_complaints(
    service: ComplaintService = Depends(get_service)
):
    return service.get_complaints()


@router.patch("/{complaint_id}/status")
def update_complaint_status(
    complaint_id: UUID,
    update: ComplaintStatusUpdate,
    service: ComplaintService = Depends(get_service)
):
    try:
        complaint = service.update_complaint_status(
            complaint_id,
            update.status
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error

    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")

    return complaint
