import requests
import json
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "").strip()

def send(message: str):
    if not DISCORD_WEBHOOK:
        print("⚠️ ERROR: Discord Webhook NOT SET!")
        return False

    payload = {"content": message}

    try:
        r = requests.post(DISCORD_WEBHOOK,
                          data=json.dumps(payload),
                          headers={"Content-Type": "application/json"})
        if r.status_code in [200, 204]:
            print("📨 Discord Message Sent")
            return True
        else:
            print(f"❌ Discord Error {r.status_code} → {r.text}")
            return False

    except Exception as e:
        print(f"❌ Discord Exception: {e}")
        return False
