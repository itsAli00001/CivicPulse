
from dataclasses import dataclass
from typing import Protocol


@dataclass
class TriageResult:
    category: str
    priority: str
    ai_summary: str
    triaged_by: str


class TriageProvider(Protocol):
    def triage(self, text: str) -> TriageResult:
        ...


class RuleBasedTriage:
    def triage(self, text: str) -> TriageResult:
        text_lower = text.lower()

        if any(word in text_lower for word in [
            "street light", "streetlight", "street lamp",
            "lamp post", "streetlights"
        ]):
            category = "streetlights"
        elif any(word in text_lower for word in [
            "water", "pipe", "leak", "flooding"
        ]):
            category = "water"
        elif any(word in text_lower for word in [
            "electricity", "electric", "power outage",
            "power cut", "wiring", "electric wire"
        ]):
            category = "electricity"
        elif any(word in text_lower for word in [
            "road", "pothole", "pavement", "broken street"
        ]):
            category = "roads"
        elif any(word in text_lower for word in [
            "garbage", "waste", "rubbish", "sewage", "sanitation"
        ]):
            category = "sanitation"
        else:
            category = "other"

        urgent_words = [
            "urgent", "emergency", "dangerous",
            "exposed wire", "burst pipe", "severe flooding"
        ]

        if any(word in text_lower for word in urgent_words):
            priority = "high"
        else:
            priority = "normal"

        return TriageResult(
            category=category,
            priority=priority,
            ai_summary=text[:140],
            triaged_by="rules"
        )


class SimulatedTriage:
    def __init__(self):
        self.rule_provider = RuleBasedTriage()

    def triage(self, text: str) -> TriageResult:
        result = self.rule_provider.triage(text)

        return TriageResult(
            category=result.category,
            priority=result.priority,
            ai_summary=result.ai_summary,
            triaged_by="simulated"
        )
