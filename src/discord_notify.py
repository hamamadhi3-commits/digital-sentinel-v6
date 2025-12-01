import requests
import os

# ==============================================================
#  DIGITAL SENTINEL MODULE — discord_notify.py
#  Purpose: Send alerts & AI analysis notifications to Discord
# ==============================================================

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")


def send_discord_message(message: str):
    """Send a formatted alert message to Discord via webhook."""
    if not DISCORD_WEBHOOK_URL:
        print("[WARN] Discord Webhook URL not set. Skipping alert.")
        return False

    payload = {
        "content": f"🚨 **Digital Sentinel Alert** 🚨\n{message}"
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("[INFO] Discord alert sent successfully ✅")
            return True
        else:
            print(f"[WARN] Discord webhook response: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to send Discord message: {e}")
        return False


def send_discord_alert(title: str, details: str):
    """Send a detailed alert with a title and description."""
    msg = f"**{title}**\n\n{details}"
    return send_discord_message(msg)
