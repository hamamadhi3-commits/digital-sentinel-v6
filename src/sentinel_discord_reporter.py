import requests
import json
from datetime import datetime

DISCORD_WEBHOOK = "<YOUR_WEBHOOK_HERE>"  # make sure this is set in secrets

def send_message(payload: dict):
    """Send raw JSON message to Discord."""
    headers = {"Content-Type": "application/json"}
    try:
        requests.post(DISCORD_WEBHOOK, data=json.dumps(payload), headers=headers)
    except Exception as e:
        print(f"[Discord] Error sending message: {e}")

# =====================================================
# 🔥 NEW FUNCTION — REQUIRED BY main_controller_v11_1
# =====================================================
def send_finding_report(summary, target, vrt, url, description, attachments=None):
    """Send a formatted vulnerability finding to Discord."""
    
    embed = {
        "title": f"🚨 New Finding Detected — {summary}",
        "color": 15158332,
        "fields": [
            {"name": "🎯 Target", "value": target, "inline": False},
            {"name": "📌 VRT Category", "value": vrt, "inline": False},
            {"name": "🔗 URL", "value": url, "inline": False},
            {"name": "📝 Description", "value": description[:1024], "inline": False},
        ],
        "footer": {"text": f"Digital Sentinel • {datetime.utcnow().isoformat()} UTC"},
    }

    payload = {"embeds": [embed]}

    # Attachments (optional)
    if attachments:
        attach_text = "\n".join(attachments)
        payload["embeds"][0]["fields"].append(
            {"name": "📎 Attachments", "value": attach_text, "inline": False}
        )

    send_message(payload)
    print("[Discord] Finding report sent successfully!")
