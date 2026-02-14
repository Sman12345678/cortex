from .messaging import send_msg
from .post import post
from .webhook import challenge as ch
from .webhook import event as ev
from .reaction import react as re

class Client:
    def __init__(self, access_token: str, api_version: str | None = None) -> None: 
        if not isinstance(access_token, str) or not access_token.strip():
            raise ValueError("ACCESS TOKEN REQUIRED (STRING)")
        self.access_token = access_token 
        self.api_version = api_version if api_version else "v23.0"
        self.base_url = "https://graph.facebook.com"
    def _url(self,endpoint: str):
        return f'{self.base_url}/{self.api_version}/{endpoint}'
    def auth(self)->dict:
        return {"access_token":self.access_token}
        
    sendMsg = send_msg
    postFeed = post
    challenge = ch
    event = ev
    react = re
