from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.complaint import Complaint
from app.repositories.complaint_repository import ComplaintRepository
from app.schemas.complaint import ComplaintCreate
from app.services.complaint_service import ComplaintService


router = APIRouter(prefix="/api/complaints", tags=["Complaints"])


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
    complaint_model = Complaint(
        text=complaint.text,
        location=complaint.location,
        reporter_contact=complaint.reporter_contact,
        category="other",
        priority="normal",
        status="open",
        ai_summary=complaint.text[:140],
        triaged_by="rules",
    )

    return service.create_complaint(complaint_model)


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