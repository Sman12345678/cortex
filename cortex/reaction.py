import requests

def react(self, psid: str, emoji: str, message_id: str):
    if not psid:
        raise ValueError("psid is required")
    if not message_id:
        raise ValueError("message_id is required")
    if not emoji:
        raise ValueError("emoji is required")

    url = self._url("me/messages")

    payload = {
        "recipient": {"id": psid},
        "message": {
            "reaction": emoji,
            "mid": message_id
        },
        "messaging_type": "RESPONSE"  
    }

    r = requests.post(url, params=self.auth(), json=payload)
    r.raise_for_status()
    return r.json()
