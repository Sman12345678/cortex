import requests

def react(self, psid: str, emoji: str, message_id: str, page_name: str | None = None):
    if not psid or not message_id or not emoji:
        print("[WARN] react() called with missing arguments.")
        return None

    if page_name is None:
        _tokens = {"page1": self.tokens.get("page1")}
    elif page_name == "*":
        _tokens = self.tokens
    else:
        t = self.tokens.get(page_name)
        if not t:
            print(f"[WARN] Page token '{page_name}' not found. Skipping react.")
            return None
        _tokens = {page_name: t}

    results = []

    for name, token in _tokens.items():
        url = f"{self.base_url}/{self.api_version}/me/messages"
        payload = {
            "recipient": {"id": psid},
            "messaging_type": "RESPONSE",
            "message": None,
            "reaction": {
                "mid": message_id,
                "action": "react",
                "reaction": emoji
            }
        }

        try:
            r = requests.post(url, params={"access_token": token}, json=payload)
            if r.ok:
                print(f"[INFO] Reaction sent for page '{name}' ✅")
                results.append(r.json())
            else:
                print(f"[WARN] React failed for page '{name}': {r.text}")
        except requests.RequestException as e:
            print(f"[ERROR] Exception sending reaction for page '{name}': {e}")

    return results
