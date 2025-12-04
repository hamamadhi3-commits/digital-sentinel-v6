import requests
import json
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_finding_report(finding):
    if not DISCORD_WEBHOOK:
        print("⚠️ No Discord webhook configured.")
        return

    # Map finding fields to Bugcrowd/HackerOne style
    report_data = {
        "title": finding.get("title", "Untitled Vulnerability"),
        "target": finding.get("target", "Unknown Target"),
        "vrt_category": finding.get("category", "Unspecified"),
        "url": finding.get("url", "N/A"),
        "severity": finding.get("severity", "Unrated"),
        "description": finding.get("description", "No description available.")
    }

    message = (
        f"🧠 **New Vulnerability Found!**\n"
        f"**1️⃣ Title:** {report_data['title']}\n"
        f"**2️⃣ Target:** {report_data['target']}\n"
        f"**3️⃣ Technical Severity (VRT):** {report_data['vrt_category']} ({report_data['severity']})\n"
        f"**4️⃣ URL:** {report_data['url']}\n"
        f"**5️⃣ Description:** {report_data['description'][:800]}...\n"
        f"**6️⃣ Proof of Concept:** Auto-collected POC attached in system logs.\n"
        f"----------------------------------\n"
        f"🔗 Saved in Sentinel DB for tracking.\n"
    )

    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK, data=json.dumps(payload), headers={"Content-Type": "application/json"})
