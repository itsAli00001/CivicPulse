
from app.config import settings
from app.providers.triage_provider import (
    RuleBasedTriage,
    SimulatedTriage,
    TriageProvider,
)


class FallbackTriage:
    def __init__(self, primary_provider: TriageProvider):
        self.primary_provider = primary_provider
        self.fallback_provider = RuleBasedTriage()

    def triage(self, text: str):
        try:
            return self.primary_provider.triage(text)
        except Exception:
            result = self.fallback_provider.triage(text)
            result.triaged_by = "rules:fallback"
            return result


def get_triage_provider() -> TriageProvider:
    provider_name = settings.triage_provider.lower()

    if provider_name == "rules":
        return RuleBasedTriage()

    if provider_name == "simulated":
        return FallbackTriage(SimulatedTriage())

    raise ValueError(f"Unsupported TRIAGE_PROVIDER: {provider_name}")
