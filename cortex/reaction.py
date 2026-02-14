import requests

def react(self, psid: str, emoji: str, message_id: str):
    if not psid or not message_id or not emoji:
        raise ValueError("psid, message_id, and emoji are required")

    url = self._url("me/messages")

    payload = {
        "recipient": {"id": psid},
        "sender_action": "react",
        "payload": {
            "message_id": message_id,
            "reaction": emoji
        }
    }

    r = requests.post(url, params=self.auth(), json=payload)

    print("React status:", r.status_code)
    print("React response:", r.text)

    if not r.ok:
        raise Exception(f"React failed: {r.text}")

    return r.json()
