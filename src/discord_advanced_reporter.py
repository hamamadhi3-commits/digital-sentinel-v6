import requests
import json
from datetime import datetime

# -------------------------------------------------
#  Discord Advanced Embed Report System
# -------------------------------------------------

SEVERITY_COLOR = {
    "CRITICAL": 0xFF0000,
    "HIGH": 0xFF6600,
    "MEDIUM": 0xFFCC00,
}

def send_advanced_report(finding, domain):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("❌ No Discord webhook set.")
        return False

    severity = finding.get("severity", "MEDIUM")

    embed = {
        "title": f"🚨 {severity} Vulnerability Found",
        "color": SEVERITY_COLOR.get(severity, 0xFFFFFF),
        "fields": [
            {"name": "📌 Summary", "value": finding.get("summary", "No title"), "inline": False},
            {"name": "🎯 Target", "value": domain, "inline": True},
            {"name": "📂 VRT Category", "value": finding.get("vrt", "None"), "inline": True},
            {"name": "🔗 URL", "value": finding.get("url", "N/A"), "inline": False},
            {"name": "📖 Description", "value": f"```{finding.get('description','No description')}```", "inline": False},
            {"name": "📎 Attachments", "value": finding.get("attachments", "None"), "inline": False}
        ],
        "footer": {"text": "Digital Sentinel — Advanced Report System"},
        "timestamp": datetime.utcnow().isoformat()
    }

    data = {"embeds": [embed]}

    try:
        requests.post(webhook, json=data, timeout=10)
        print("📨 Sent advanced report to Discord.")
        return True
    except Exception as e:
        print(f"❌ Discord send error: {e}")
        return False
