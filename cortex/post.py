import requests

def post(self, media_type: str, text: str | None = None,
         media_url: str | None = None, title: str | None = None,
         description: str | None = None, page_name: str | None = None):

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
        if media_type == "text":
            if not text:
                raise ValueError("TEXT REQUIRED")
            url = self._url("me/feed")
            payload = {"message": text}
            r = requests.post(url, params={"access_token": _token}, json=payload)
            r.raise_for_status()
            results.append(r.json())

        elif media_type == "image":
            if not media_url:
                raise ValueError("Image post requires media_url")
            url = self._url("me/photos")
            payload = {"url": media_url, "caption": text}
            r = requests.post(url, params={"access_token": _token}, json=payload)
            r.raise_for_status()
            results.append(r.json())

        elif media_type == "video":
            if not media_url:
                raise ValueError("Video post requires media_url")
            url = self._url("me/videos")
            payload = {"file_url": media_url, "title": title, "description": description}
            r = requests.post(url, params={"access_token": _token}, json=payload)
            r.raise_for_status()
            results.append(r.json())

        else:
            raise ValueError(f"Unsupported media_type: {media_type}")

    return results
