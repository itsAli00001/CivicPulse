from app.providers.triage_factory import FallbackTriage
from app.providers.triage_provider import RuleBasedTriage, SimulatedTriage


def test_water_complaint():
    result = RuleBasedTriage().triage(
        "There is a leaking water pipe near our house."
    )
    assert result.category == "water"


def test_electricity_complaint():
    result = RuleBasedTriage().triage(
        "There is a power outage in our area."
    )
    assert result.category == "electricity"


def test_road_complaint():
    result = RuleBasedTriage().triage(
        "There is a large pothole on our road."
    )
    assert result.category == "roads"


def test_sanitation_complaint():
    result = RuleBasedTriage().triage(
        "Garbage waste has not been collected."
    )
    assert result.category == "sanitation"


def test_streetlight_complaint():
    result = RuleBasedTriage().triage(
        "The street light is not working."
    )
    assert result.category == "streetlights"


def test_unknown_complaint():
    result = RuleBasedTriage().triage(
        "There is a broken public bench in our park."
    )
    assert result.category == "other"


def test_urgent_complaint_has_high_priority():
    result = RuleBasedTriage().triage(
        "Emergency: there is an exposed wire near a school."
    )
    assert result.priority == "high"


def test_normal_complaint_has_normal_priority():
    result = RuleBasedTriage().triage(
        "There is a small pothole on our street."
    )
    assert result.priority == "normal"


def test_summary_is_limited_to_140_characters():
    text = "water " * 50
    result = RuleBasedTriage().triage(text)
    assert len(result.ai_summary) <= 140


def test_triaged_by_rules():
    result = RuleBasedTriage().triage(
        "There is a broken water pipe near our street."
    )
    assert result.triaged_by == "rules"

def test_simulated_triage_identifies_provider():
    result = SimulatedTriage().triage(
        "There is a leaking water pipe near our house."
    )

    assert result.triaged_by == "simulated"


def test_simulated_triage_preserves_category():
    result = SimulatedTriage().triage(
        "There is a leaking water pipe near our house."
    )

    assert result.category == "water"


def test_simulated_triage_preserves_priority():
    result = SimulatedTriage().triage(
        "Emergency: there is an exposed wire near a school."
    )

    assert result.priority == "high"

class FailingProvider:
    def triage(self, text: str):
        raise RuntimeError("Provider failed")


def test_fallback_uses_rules_when_provider_fails():
    provider = FallbackTriage(FailingProvider())

    result = provider.triage(
        "There is a leaking water pipe near our house."
    )

    assert result.category == "water"
    assert result.triaged_by == "rules:fallback"