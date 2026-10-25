from uuid import UUID

from app.models.complaint import Complaint
from app.repositories.complaint_repository import ComplaintRepository
from app.schemas.complaint import ComplaintCreate


class ComplaintService:

    def __init__(self, repository: ComplaintRepository):
        self.repository = repository

    def create_complaint(self, complaint: ComplaintCreate) -> Complaint:
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

        return self.repository.create(complaint_model)

    def get_complaint(self, complaint_id: UUID) -> Complaint | None:
        return self.repository.get_by_id(complaint_id)

    def get_complaints(self) -> list[Complaint]:
        return self.repository.get_all()
