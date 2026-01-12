import requests

def react(self,emoji:str, message_id:str)
    if not message_id:
        raise ValueError("message_id is required to react to a message")

    url = self._url("me/messages")

    payload = {
        "recipient": {"id": psid},
        "message": {
            "reaction": {
                "action": "react",
                "reaction": emoji
            },
            "mid": message_id
        }
    }

    r = requests.post(
        url,
        params=self.auth(),
        json=payload
    )

    r.raise_for_status()
    return r.json()
