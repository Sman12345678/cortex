import requests

def send_msg(self, psid: str, text: str | None = None,
             msg_type: str | None = "text",
             media_url: str | list[str] | None = None,
             page_name: str | None = None):
    
    url = self._url("me/messages")
    results = []

    
    if page_name is None:
        _tokens = {"page1": self.tokens.get("page1")}
    elif page_name == "*":
        _tokens = self.tokens
    else:
        t = self.tokens.get(page_name)
        if not t:
            raise ValueError(f"No token found for page {page_name}")
        _tokens = {page_name: t}

    
    for name, _token in _tokens.items():
        if msg_type == "text":
            if not text:
                raise ValueError("Text message cannot be empty")
            payload = {"recipient": {"id": psid}, "message": {"text": text}}
            r = requests.post(url, params={"access_token": _token}, json=payload)
            r.raise_for_status()
            results.append(r.json())

        elif msg_type in ("image", "video", "audio", "file"):
            if not media_url:
                raise ValueError(f"{msg_type} message requires a media_url")

            if isinstance(media_url, str):
                media_url = [media_url]

            for url in media_url:
                payload = {
                    "recipient": {"id": psid},
                    "message": {
                        "attachment": {
                            "type": msg_type,
                            "payload": {
                                "url": url,
                                "is_reusable": True
                            }
                        }
                    }
                }
                r = requests.post(url, params={"access_token": _token}, json=payload)
                r.raise_for_status()
                results.append(r.json())
        else:
            raise ValueError(f"Unsupported message type: {msg_type}")

    return results
