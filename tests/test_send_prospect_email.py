import unittest

from langchain.tools import ToolRuntime

from gtm_agent.gtm_agent import send_prospect_email


class SendProspectEmailTest(unittest.TestCase):
    def test_disqualified_prospect_is_blocked_without_message_id(self):
        result = send_prospect_email.func(
            {
                "prospect_id": "LEAD-50001",
                "name": "Priya Nair",
                "email": "priya.nair@brightwaveapps.com",
            },
            "Follow-up",
            "Checking in.",
            ToolRuntime({}, {}, {"metadata": {}}, lambda _: None, None, None),
        )

        self.assertEqual(
            result,
            {
                "status": "blocked",
                "reason": "Prospect is marked disqualified; send is not permitted.",
            },
        )
        self.assertNotIn("message_id", result)
