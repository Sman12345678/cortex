import requests

def send_msg(self, psid: str, text: str | None = None,
             msg_type: str | None = "text",
             media_url: str | list[str] | None = None):

    url = self._url("me/messages")
    results = []

    if msg_type == "text":
        if not text:
            raise ValueError("Text message cannot be empty")
        payload = {"recipient": {"id": psid}, "message": {"text": text}}
        r = requests.post(url, params=self.auth(), json=payload)
        r.raise_for_status()
        return r.json()

    elif msg_type in ("image", "video", "audio", "file"):
        if not media_url:
            raise ValueError(f"{msg_type} message requires a media_url")

        
        if isinstance(media_url, str):
            media_url = [media_url]

        for url_item in media_url:
            payload = {
                "recipient": {"id": psid},
                "message": {
                    "attachment": {
                        "type": msg_type,
                        "payload": {
                            "url": url_item,
                            "is_reusable": True
                        }
                    }
                }
            }

            
            r = requests.post(url, params=self.auth(), json=payload)
            r.raise_for_status()
            results.append(r.json())

        return results

    else:
        raise ValueError(f"Unsupported message type: {msg_type}")
