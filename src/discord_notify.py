import os
import requests
from datetime import datetime

# === Load Webhook from GitHub Secret ===
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")


def send_discord_report(title: str, description: str, color: int = 0x3498DB, fields: list = None):
    """
    Send formatted report to Discord channel.
    :param title: Title of embed message
    :param description: Main content text
    :param color: Embed color (hex)
    :param fields: Optional list of dicts [{"name": "", "value": "", "inline": True}]
    """

    if not DISCORD_WEBHOOK:
        print("⚠️ Discord webhook not configured or missing from environment.")
        return False

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": "🛰️ Digital Sentinel v11 • Eternal Hunter",
        }
    }

    if fields:
        embed["fields"] = fields

    payload = {"embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        if response.status_code in [200, 204]:
            print("✅ Discord notification sent successfully.")
            return True
        else:
            print(f"⚠️ Discord returned status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"💥 Discord send error: {e}")
        return False


# === Backward compatibility for older imports ===
def send_discord_alert(title: str, message: str, color: int = 0xE67E22):
    """ Legacy alias for compatibility with main_controller_v11 """
    return send_discord_report(title, message, color=color)
