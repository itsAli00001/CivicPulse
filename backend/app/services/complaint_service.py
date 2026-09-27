from app.providers.triage_provider import RuleBasedTriage
from app.schemas.complaint import ComplaintCreate


class ComplaintService:
    def __init__(self):
        self.triage_provider = RuleBasedTriage()

    def create_complaint(self, complaint: ComplaintCreate):
        triage_result = self.triage_provider.triage(complaint.text)

        return {
            "text": complaint.text,
            "location": complaint.location,
            "reporter_contact": complaint.reporter_contact,
            "category": triage_result.category,
            "priority": triage_result.priority,
            "status": "open",
            "ai_summary": triage_result.ai_summary,
            "triaged_by": triage_result.triaged_by
        }