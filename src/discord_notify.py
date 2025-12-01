"""
Digital Sentinel v6.0 – Discord Notification Engine
Purpose: Sends mission status updates to Discord Webhook channels
"""

import requests
import json
import os

# Default webhook path (configure it in .env or config.json)
def _get_webhook_url():
    """Safely fetch Discord webhook URL from config or env"""
    config_path = "data/targets/config.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as cf:
            try:
                cfg = json.load(cf)
                if "discord_webhook" in cfg:
                    return cfg["discord_webhook"]
            except Exception:
                pass
    return os.getenv("DISCORD_WEBHOOK", None)

def send_discord_alert(message: str, title: str = "Digital Sentinel v6.0"):
    """
    Sends a formatted message to Discord webhook.
    Example:
        send_discord_alert("Recon cycle complete ✅")
    """
    webhook_url = _get_webhook_url()
    if not webhook_url:
        print("[WARN] No Discord webhook configured.")
        return

    payload = {
        "username": title,
        "embeds": [
            {
                "title": title,
                "description": message,
                "color": 65280,  # green color
                "footer": {"text": "Digital Sentinel Autonomous Mode"}
            }
        ]
    }

    try:
        resp = requests.post(webhook_url, json=payload)
        if resp.status_code == 204:
            print("[DISCORD] Alert sent successfully ✅")
        else:
            print(f"[DISCORD] Failed to send alert ({resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"[ERROR] Discord alert failed: {e}")
