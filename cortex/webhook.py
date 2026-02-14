from flask import request 

def challenge(self, verify_token: str):
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == verify_token:
        return challenge, 200
    return "Verification failed", 403
    
def event(self, handler = None, q = None|str):
    data = q.json
    for entry in data.get("entry", []):
        for messaging_event in entry.get("messaging", []):
            sender_id = messaging_event["sender"]["id"]
            message = messaging_event.get("messages",{})
            message_id = message.get("mid")
            if "text" in message:
                if handler:
                    handler(sender_id, "text", message["text"], message_id)
            elif "attachments" in message:
                for att in message["attachments"]:
                    att_type = att.get("type")
                    att_url = att.get("payload", {}).get("url")
                    if handler:
                        handler(sender_id, att_type, att_url, message_id)

    return "EVENT_RECEIVED", 200

  
