import requests

def post(self, media_type: str, text: str | None = None,
         media_url: str | None = None, title: str | None = None,
         description: str | None = None):
    
    if media_type == "text":
        if not text:
            raise ValueError("TEXT REQUIRED")
        url = self._url("me/feed")
        payload = {"message": text, **self.auth()}
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()
    
    elif media_type == "image":
        if not media_url:
            raise ValueError("Image post requires media_url")
        url = self._url("me/photos")
        payload = {"url": media_url, "caption": text, **self.auth()}
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()
    
    elif media_type == "video":
        if not media_url:
            raise ValueError("Video post requires media_url")
        url = self._url("me/videos")
        payload = {"file_url": media_url, "title": title, "description": description, **self.auth()}
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()
    
    else:
        raise ValueError(f"Unsupported media_type: {media_type}")
        
