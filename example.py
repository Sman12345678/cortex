# How to Use Cortex
from flask import Flask, request
import os
from cortex import Client
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
fb = Client(ACCESS_TOKEN)


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return fb.challenge(VERIFY_TOKEN)
    elif request.method == "POST":

        def post(text):
            fb.post(media_type="text", text=text)

        def echo(sender_id, msg_type, content, message_id):
            if msg_type == "text":
                
                if content.startswith("/post"):
                    post(content)
                
                fb.react(sender_id, "😁", message_id)
                fb.sendMsg(psid=sender_id, text=f"You sent: {content}", msg_type="text")
            else:
                
                fb.sendMsg(psid=sender_id, text=None, msg_type=msg_type, media_url=content)
                fb.sendMsg(psid=sender_id, text=f"You sent a {msg_type}: {content}", msg_type="text")

        return fb.event(handler=echo)


if __name__ == "__main__":
    print("""
CORTEX (LIGHTWEIGHT FACEBOOK GRAPH API WRAPPER)
--MADE WITH ♥️ BY CORTEXINVADER--
FACEBOOK : facebook.com/cortexinvader
""")
    app.run(port=5000, debug=True)
