import requests
import os

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_report_to_discord(message):
    if not WEBHOOK:
        print("⚠️ No DISCORD_WEBHOOK found")
        return False

    payload = {
        "content": message
    }

    try:
        requests.post(WEBHOOK, json=payload)
        print("📨 Auto-Report sent to Discord.")
        return True
    except Exception as e:
        print("❌ Discord sending failed: ", e)
        return False
