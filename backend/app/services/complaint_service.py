
from uuid import UUID

from app.models.complaint import Complaint
from app.providers.triage_provider import RuleBasedTriage
from app.repositories.complaint_repository import ComplaintRepository
from app.schemas.complaint import ComplaintCreate


class ComplaintService:

    VALID_TRANSITIONS = {
        "open": {"in_progress", "rejected"},
        "in_progress": {"resolved", "rejected"},
        "resolved": set(),
        "rejected": set(),
    }

    def __init__(self, repository: ComplaintRepository):
        self.repository = repository
        self.triage_provider = RuleBasedTriage()

    def create_complaint(self, complaint: ComplaintCreate) -> Complaint:
        triage_result = self.triage_provider.triage(complaint.text)

        complaint_model = Complaint(
            text=complaint.text,
            location=complaint.location,
            reporter_contact=complaint.reporter_contact,
            category=triage_result.category,
            priority=triage_result.priority,
            status="open",
            ai_summary=triage_result.ai_summary,
            triaged_by=triage_result.triaged_by,
        )

        return self.repository.create(complaint_model)

    def get_complaint(self, complaint_id: UUID) -> Complaint | None:
        return self.repository.get_by_id(complaint_id)

    def get_complaints(self) -> list[Complaint]:
        return self.repository.get_all()

    def update_complaint_status(
        self,
        complaint_id: UUID,
        new_status: str
    ) -> Complaint | None:
        complaint = self.repository.get_by_id(complaint_id)

        if complaint is None:
            return None

        allowed_statuses = self.VALID_TRANSITIONS.get(
            complaint.status, set()
        )

        if new_status not in allowed_statuses:
            raise ValueError(
                f"Cannot change status from {complaint.status} to {new_status}"
            )

        return self.repository.update_status(complaint, new_status)
