from dataclasses import dataclass


@dataclass
class TriageResult:
    category: str
    priority: str
    ai_summary: str
    triaged_by: str


class TriageProvider:
    def triage(self, text: str) -> TriageResult:
        raise NotImplementedError

class RuleBasedTriage(TriageProvider):
    def triage(self, text: str) -> TriageResult:
        text_lower = text.lower()

        if "water" in text_lower or "pipe" in text_lower:
            category = "water"
        elif "electric" in text_lower or "power" in text_lower:
            category = "electricity"
        elif "road" in text_lower or "pothole" in text_lower:
            category = "roads"
        elif "garbage" in text_lower or "waste" in text_lower:
            category = "sanitation"
        elif "light" in text_lower:
            category = "streetlights"
        else:
            category = "other"

        return TriageResult(
            category=category,
            priority="normal",
            ai_summary=text[:140],
            triaged_by="rules"
        )