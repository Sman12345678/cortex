import requests
from .messaging import send_msg
from .post import post
from .webhook import challenge as ch
from .webhook import event as ev


class Client:
    def __init__(self, tokens: str | dict[str, str], api_version: str | None = None) -> None:
        print("Cortex Initialised Successfully....")

        if isinstance(tokens, str):
            tokens = {"page1": tokens}

        if not isinstance(tokens, dict) or not all(isinstance(t, str) for t in tokens.values()):
            raise ValueError("Tokens must be a string or a dict of page_name.")

        self.tokens = tokens
        self.api_version = api_version if api_version else "v23.0"
        self.base_url = "https://graph.facebook.com"

        self.validate()

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}/{self.api_version}/{endpoint}"

    def auth(self, page_name: str = "page1") -> dict:
        token = self.tokens.get(page_name)
        if not token:
            raise ValueError(f"No token found for page {page_name}")
        return {"access_token": token}

    def validate(self, page_name: str = "page1"):

        token = self.tokens.get(page_name)

        url = self._url("me")

        res = requests.get(url, params={"access_token": token})
        data = res.json()

        if "error" in data:
            print(f"error: {data}")
        else:
            for field, value in data.items():
                print(f"{field}: {value}")

    sendMsg = send_msg
    postFeed = post
    challenge = ch
    event = ev
