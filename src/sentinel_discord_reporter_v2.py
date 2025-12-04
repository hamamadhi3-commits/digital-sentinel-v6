# src/sentinel_discord_reporter_v2.py
import requests
import json
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_finding_report(finding):
    """Send a vulnerability report to Discord with full Bugcrowd-style format."""
    if not DISCORD_WEBHOOK:
        print("⚠️ No Discord webhook configured.")
        return

    title = finding.get("title", "Untitled Vulnerability")
    target = finding.get("target", "Unknown Target")
    vrt_category = finding.get("category", "Unspecified")
    url = finding.get("url", "N/A")
    severity = finding.get("severity", "Unrated")
    description = finding.get("description", "No description available.")
    poc = finding.get("poc", "Auto-captured proof of concept (available in logs).")

    message = (
        f"🧠 **New Vulnerability Found!**\n"
        f"**1️⃣ Title:** {title}\n"
        f"**2️⃣ Target:** {target}\n"
        f"**3️⃣ Technical Severity (VRT):** {vrt_category} ({severity})\n"
        f"**4️⃣ URL:** {url}\n"
        f"**5️⃣ Description:** {description[:800]}...\n"
        f"**6️⃣ Proof of Concept:** {poc}\n"
        f"----------------------------------\n"
        f"🕒 Detected at: {datetime.utcnow().isoformat()} UTC\n"
        f"🔗 Stored securely in Sentinel archive.\n"
    )

    try:
        payload = {"content": message}
        requests.post(DISCORD_WEBHOOK, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        print(f"✅ Discord report sent for {target}")
    except Exception as e:
        print(f"❌ Discord send failed: {e}")
