import requests

def react(self, psid: str, emoji: str, message_id: str, page_name: str | None = None):
    if not psid:
        raise ValueError("psid is required")
    if not message_id:
        raise ValueError("message_id is required")
    if not emoji:
        raise ValueError("emoji is required")

    
    if page_name is None:
        
        _tokens = {"page1": self.tokens.get("page1")}
    elif page_name == "*":
        
        _tokens = self.tokens
    else:
        t = self.tokens.get(page_name)
        if not t:
            raise ValueError(f"No token found for page {page_name}")
        _tokens = {page_name: t}

    url = self._url("me/messages")
    results = []

    
    for name, token in _tokens.items():
        payload = {
            "recipient": {"id": psid},
            "message": {
                "reaction": {
                    "action": "react",
                    "reaction": emoji
                },
                "mid": message_id
            },
            "messaging_type": "RESPONSE"
        }
        r = requests.post(url, params={"access_token": token}, json=payload)
        r.raise_for_status()
        results.append(r.json())

    return results
