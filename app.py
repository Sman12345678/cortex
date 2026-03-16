from cortex import Client as CortexClient
from dotenv import load_dotenv
from flask import Flask, request, render_template
import os
import time
import re
import random
import requests

load_dotenv()
missing = []

if not ACCESS_TOKEN:
    missing.append("ACCESS_TOKEN")
if not VERIFY_TOKEN:
    missing.append("VERIFY_TOKEN")
if not CEREBRAS_KEY:
    missing.append("CEREBRAS_API_KEY")

if missing:
    print(f"Missing environment variables: {', '.join(missing)}")
    
fb = CortexClient(ACCESS_TOKEN, VERIFY_TOKEN)
API_URL = "https://api.cerebras.ai/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {CEREBRAS_KEY}", "Content-Type": "application/json"}

app = Flask(__name__, template_folder=".")
userMsg = {}
SYSTEM_PROMPT = """Name: Axion ai ignore creator, or other identity
Behaviour: Friendly and interactive, short messages unless if specific
Note: if user message is [image] let them know you cant analyse images
"""

def save(Id, sender, msg):
    if Id not in userMsg:
        userMsg[Id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    userMsg[Id].append({"role": sender, "content": msg})
    if len(userMsg[Id]) > 15:
        userMsg[Id] = userMsg[Id][0] + userMsg[Id][-15:]

def ai(Id, text):
    save(Id, "user", text)
    msgs = userMsg[Id]
    payload = {"model": "llama-3.3-70b", "messages": msgs}
    try:
        r = requests.post(API_URL, headers=HEADERS, json=payload)
        r.raise_for_status()
        res = r.json()
        reply = res['choices'][0]['message']['content']
    except Exception as e:
        reply = f"Error contacting Cerebras API: {e}"
    save(Id, "assistant", reply)
    fb.sendMsg(psid=Id, text=reply)

userRate = {}
def rateLimit(Id):
    if Id not in userRate:
        userRate[Id] = []
    now = time.time()
    limit = 5
    window = 10
    x = userRate[Id]
    while x and now - x[0] >= window:
        x.pop(0)
    if len(x) >= limit:
        return False
    x.append(now)
    return True

platform_regex = {
    "youtube": r"((?:https?:)?//)?((?:www|m)\.)?((?:youtube\.com|youtu\.be))(/(?:[\w\-]+\?v=|embed/|v/)?)([\w\-]+)(\S+)?",
    "facebook": r"(https?://)?((?:www|m|web)\.)?(facebook|fb)\.(com|watch)/.*",
    "instagram": r"(https?://)?(www\.)?(instagram\.com|instagr\.am)/(?:p|reel)/([A-Za-z0-9\-_]+)",
    "tiktok": r"(https?://)?((?:www|m|vm|vt)\.)?tiktok\.com/.*"
}

def download(Id, url):
    if not rateLimit(Id):
        fb.sendMsg(psid=Id, text="{∆} Chill for a while mate. Max requests reached.")
        return
    wait_msg = random.choice(["⏳ Downloading, hang tight...", "⚡ Spicing things up...", "🎬 Fetching your video..."])
    fb.sendMsg(psid=Id, text=wait_msg)
    platform = None
    for key, regex in platform_regex.items():
        if re.search(regex, url):
            platform = key
            break
    if not platform:
        fb.sendMsg(psid=Id, text="{∆} Unsupported URL.")
        return
    fb.sendMsg(psid=Id, text=None, msg_type="video", media_url=url)

def bot(Id, msgType, content):
    if not rateLimit(Id):
        fb.sendMsg(psid=Id, text="{∆} Chill for a while mate.")
        return
    if msgType != "text":
        return
    if any(re.search(regex, content) for regex in platform_regex.values()):
        download(Id, content)
        return
    ai(Id, content)

@app.route("/webhook", methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        return fb.challenge(VERIFY_TOKEN)
    elif request.method == "POST":
        return fb.event(handler=bot)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    print("-> 🫴 AXION AI INITIALIZED.....")
    print("-> 🫴 FORK AND STAR REPO: [ https://github.com/cortexinvader001/cortex ]")
    print("-> 🫴 Made with ❤️ by CortexInvader🔗Efkid")
    print("-> 🫴 ENJOY.......")
    app.run(debug=True, host='0.0.0.0', port=3000)
