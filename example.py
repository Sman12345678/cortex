#How to ise cortex
from flask import Flask, request
import os
import requests
import random
from dotenv import load_dotenv
from cortex import Client

load_dotenv()

app = Flask(__name__)

ACCESS_TOKEN  = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN  = os.getenv("VERIFY_TOKEN")

if not ACCESS_TOKEN or not VERIFY_TOKEN:
    raise ValueError("Missing PAGE_ACCESS_TOKEN or VERIFY_TOKEN")

fb = Client(ACCESS_TOKEN)

CAT_IMAGES = [
    "https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg",
    "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800",
    "https://images.unsplash.com/photo-1532384818465-6a7a4e6d9e8d?w=800",
    "https://images.unsplash.com/photo-1548366086-7f1b7610666d?w=800",
]

CAT_VIDEOS = [
    "https://cdn.pixabay.com/video/2023/07/18/174932-841499_small.mp4",
    "https://cdn.pixabay.com/video/2024/04/06/208064_tiny.mp4",
    "https://videos.pexels.com/video-files/31487364/13425379_1440_2560_25fps.mp4",
    "https://cdn.pixabay.com/video/2023/03/28/156499-1024x576-30fps.mp4",
]

AUDIOS = [
    "https://assets.mixkit.co/sfx/preview/mixkit-cat-purr-837.mp3",
    "https://assets.mixkit.co/sfx/preview/mixkit-cat-meow-2054.mp3",
    "https://assets.mixkit.co/music/preview/mixkit-relaxing-beat-01.mp3",
    "https://assets.mixkit.co/music/preview/mixkit-valley-sunset-118.mp3",
    "https://assets.mixkit.co/music/preview/mixkit-serene-view-118.mp3",
]

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return fb.challenge(VERIFY_TOKEN)

    if request.method == "POST":
        def post(text):
            try:
                fb.postFeed(media_type="text", text=text.strip())
                return True, None
            except Exception as e:
                print(f"Post failed: {e}")
                return False, str(e)

        def echo(sender_id, msg_type, content, message_id):
            if msg_type != "text":
                fb.sendMsg(
                    psid=sender_id,
                    text=f"{msg_type} received 🔥",
                    msg_type="text"
                )
                return

            content = content.strip().lower()

            if content == "help":
                help_text = """╭──⦿【 ⚡ BOT COMMANDS 】
│
│ 👤 User : Suleiman 
│ 📧 Email    : cortexinvader@gmail.com
│ 💬 Social   : facebook.com/cortexinvader
│
│ 📝 Available actions :
│ Send text • image • video • audio
│ to receive cool replies 😎
│
│ 🛒 Special commands :
│ - /post your message     → post to page
│ - image                  → random cat pic
│ - video                  → relaxing cat clip
│ - audio                  → purr or chill music
│
╰────────⦿"""
                fb.sendMsg(
                    psid=sender_id,
                    text=help_text,
                    msg_type="text"
                )
                fb.react(sender_id, "⚡", message_id)
                return

            if content == "image":
                fb.sendMsg(
                    psid=sender_id,
                    text=None,
                    msg_type="image",
                    media_url=random.choice(CAT_IMAGES)
                )
                fb.react(sender_id, "😁", message_id)
                return

            if content == "video":
                fb.sendMsg(
                    psid=sender_id,
                    text=None,
                    msg_type="video",
                    media_url=random.choice(CAT_VIDEOS)
                )
                fb.react(sender_id, "🎥", message_id)
                return

            if content == "audio":
                fb.sendMsg(
                    psid=sender_id,
                    text=None,
                    msg_type="audio",
                    media_url=random.choice(AUDIOS)
                )
                fb.react(sender_id, "🎵", message_id)
                return

            if content.startswith("/post"):
                post_text = content[5:].strip()
                if not post_text:
                    fb.sendMsg(
                        psid=sender_id,
                        text="Use: /post your message",
                        msg_type="text"
                    )
                    return

                success, error_msg = post(post_text)
                if success:
                    fb.react(sender_id, "🔥", message_id)
                else:
                    msg = "Couldn't post right now 😕"
                    if error_msg:
                        msg += f"\n({error_msg})"
                    fb.sendMsg(
                        psid=sender_id,
                        text=msg,
                        msg_type="text"
                    )
                    fb.react(sender_id, "❌", message_id)
                return

            fb.react(sender_id, "😁", message_id)

            try:
                ai_text = requests.get(f"https://text.pollinations.ai/{content}", timeout=60).text
                fb.sendMsg(psid=sender_id, text=ai_text, msg_type="text")
            except Exception as e:
                print(f"AI request failed: {e}")
                fb.sendMsg(
                    psid=sender_id,
                    text=f"AI is sleeping right now 😴 ({str(e)})",
                    msg_type="text"
                )

        return fb.event(handler=echo)


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════╗
    ║        CORTEX FACEBOOK BOT         ║
    ║   Lightweight Graph API wrapper    ║
    ╚════════════════════════════════════╝
    Made with ♥ by cortexinvader
    facebook.com/cortexinvader
    """)

    app.run(
        host="0.0.0.0",
        port=3000,
        debug=True
    )
