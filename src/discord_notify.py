import os
import json
import requests
from datetime import datetime

# 🛰️ Discord Webhook Token
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# 🎨 Colors by severity level
COLOR_MAP = {
    "critical": 0xE74C3C,  # Red
    "high": 0xE67E22,      # Orange
    "medium": 0xF1C40F,    # Yellow
    "low": 0x2ECC71,       # Green
    "info": 0x3498DB       # Blue
}

# 🧠 Core function to send a Discord message
def send_discord_message(title: str, description: str, severity: str = "info", fields: list = None):
    """
    Send structured embed message to Discord with severity color and custom fields.
    """
    if not DISCORD_WEBHOOK:
        print("⚠️ Discord webhook not configured.")
        return False

    color = COLOR_MAP.get(severity, 0x95A5A6)  # Default gray if undefined
    timestamp = datetime.utcnow().isoformat()

    embed = {
        "title": f"📡 {title}",
        "description": description,
        "color": color,
        "timestamp": timestamp,
        "footer": {
            "text": "Digital Sentinel v11 • Eternal Hunter",
            "icon_url": "https://i.imgur.com/0Zt6JwX.png"
        },
        "fields": fields or []
    }

    payload = {"embeds": [embed]}

    try:
        r = requests.post(DISCORD_WEBHOOK, json=payload)
        if r.status_code in [200, 204]:
            print(f"✅ Report sent to Discord: {title}")
            return True
        else:
            print(f"⚠️ Discord API error: {r.status_code} → {r.text}")
            return False
    except Exception as e:
        print(f"💥 Discord send failed: {e}")
        return False


# 🚀 Example: send report summary automatically
def send_daily_summary():
    """
    Compose and send daily mission summary from logs or reports.
    """
    summary_path = "data/reports/last_summary.json"
    if not os.path.exists(summary_path):
        send_discord_message(
            "Daily Summary Missing",
            "⚠️ No summary file found in `data/reports/`. Skipping...",
            severity="low"
        )
        return

    try:
        with open(summary_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)

        target_count = report_data.get("targets_scanned", 0)
        vulns_found = report_data.get("vulns_found", 0)
        high_vulns = report_data.get("high_severity", 0)
        critical_vulns = report_data.get("critical_severity", 0)

        fields = [
            {"name": "🛰️ Targets Scanned", "value": str(target_count), "inline": True},
            {"name": "🧠 Vulns Found", "value": str(vulns_found), "inline": True},
            {"name": "🔥 High Severity", "value": str(high_vulns), "inline": True},
            {"name": "💀 Critical", "value": str(critical_vulns), "inline": True}
        ]

        send_discord_message(
            "📊 Daily Recon Summary",
            "Autonomous cycle report generated successfully.",
            severity="info",
            fields=fields
        )

    except Exception as e:
        send_discord_message(
            "❌ Summary Processing Error",
            f"Failed to read or send summary file.\nError: `{str(e)}`",
            severity="critical"
        )


if __name__ == "__main__":
    # 🔁 Auto-trigger when called standalone
    print("🚀 Launching Discord Notify Engine...")
    send_daily_summary()
