import requests

def react(self, psid: str, emoji: str, message_id: str):
    """
    React to a user's message.
    """

    if not psid:
        raise ValueError("psid is required")

    if not message_id:
        raise ValueError("message_id is required")

    if not emoji:
        raise ValueError("emoji is required")

    url = self._url("me/messages")

    payload = {
        "recipient": {"id": psid},
        "messaging_type": "RESPONSE",
        "message": {
            "reaction": {
                "action": "react",
                "mid": message_id,
                "reaction": emoji
            }
        }
    }

    r = requests.post(
        url,
        params=self.auth(),
        json=payload
    )

    # Debug output (remove in production)
    print("React status:", r.status_code)
    print("React response:", r.text)

    if not r.ok:
        raise Exception(f"React failed: {r.text}")

    return r.json()
