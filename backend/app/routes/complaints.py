from fastapi import APIRouter

from app.schemas.complaint import ComplaintCreate
from app.services.complaint_service import ComplaintService


router = APIRouter(prefix="/api/complaints", tags=["Complaints"])

complaint_service = ComplaintService()


@router.post("")
def create_complaint(complaint: ComplaintCreate):
    return complaint_service.create_complaint(complaint)