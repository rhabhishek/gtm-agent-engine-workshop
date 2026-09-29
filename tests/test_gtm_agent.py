import os

os.environ.setdefault("OPENAI_API_KEY", "test")
os.environ.setdefault("LANGSMITH_TRACING", "false")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


SENSITIVE_FIELDS = {
    "billing_qualification",
    "tax_id",
    "date_of_birth",
    "card_on_file",
    "credit_check_ref",
}


def nested_keys(value):
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(nested_keys(item))
        return keys
    if isinstance(value, list):
        keys = set()
        for item in value:
            keys.update(nested_keys(item))
        return keys
    return set()


def test_prospect_tools_do_not_return_billing_fields():
    data_service._PROFILES.clear()

    contact = get_prospect.invoke("LEAD-12853")
    profile = build_prospect_profile.invoke("LEAD-12853")

    assert not SENSITIVE_FIELDS & nested_keys(contact)
    assert not SENSITIVE_FIELDS & nested_keys(profile)


def test_build_prospect_profile_sanitizes_existing_cached_profile():
    data_service._PROFILES["LEAD-12853"] = {
        "prospect_id": "LEAD-12853",
        "nested": [{"billing_qualification": {"tax_id": "secret"}}],
    }

    result = build_prospect_profile.invoke("LEAD-12853")

    assert not SENSITIVE_FIELDS & nested_keys(result)
    assert not SENSITIVE_FIELDS & nested_keys(data_service._PROFILES["LEAD-12853"])
