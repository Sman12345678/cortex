import requests

def send_msg(self, psid: str, text: str | None = None,
             msg_type: str | None = "text",
             media_url: str | None = None):

    url = self._url("me/messages")
    payload = {"recipient": {"id": psid}}

    if msg_type == "text":
        if not text:
            raise ValueError("Text message cannot be empty")
        payload["message"] = {"text": text}

    elif msg_type in ("image", "video", "audio", "file"):
        if not media_url:
            raise ValueError(f"{msg_type} message requires a media_url")

        payload["message"] = {
            "attachment": {
                "type": msg_type,
                "payload": {
                    "url": media_url,
                    "is_reusable": True
                }
            }
        }

    else:
        raise ValueError(f"Unsupported message type: {msg_type}")

    r = requests.post(url, params=self.auth(), json=payload)
    r.raise_for_status()
    return r.json()
