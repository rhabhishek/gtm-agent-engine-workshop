import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LANGSMITH_TRACING", "false")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile


class UpdateProspectInfoTest(unittest.TestCase):
    def test_update_persists_technology_and_invalidates_profile(self):
        prospect_id = "LEAD-71001"
        original_tech_stack = list(data_service.PROSPECTS[prospect_id]["tech_stack"])
        data_service._PROFILES.pop(prospect_id, None)

        try:
            build_prospect_profile.invoke({"prospect_id": prospect_id})
            result = data_service.update_prospect_info(prospect_id, "Kafka")
            profile = build_prospect_profile.invoke({"prospect_id": prospect_id})

            self.assertTrue(result["updated"])
            self.assertIn("Kafka", data_service.fetch_tech_stack(prospect_id))
            self.assertIn("Kafka", profile["prospect_profile"]["tech_stack"])
        finally:
            data_service.PROSPECTS[prospect_id]["tech_stack"] = original_tech_stack
            data_service._PROFILES.pop(prospect_id, None)


if __name__ == "__main__":
    unittest.main()
