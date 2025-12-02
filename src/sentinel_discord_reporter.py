#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📡 Digital Sentinel v11.1 — Discord Reporter
Sends detailed mission reports and summaries to your Discord channel.
"""

import os
import json
import requests
from datetime import datetime

# ===== CONFIGURATION ===== #
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

REPORT_DIR = "data/reports"
LOG_DIR = "data/logs"

def load_latest_report():
    """Load latest report file if available."""
    if not os.path.exists(REPORT_DIR):
        return None
    reports = sorted(
        [os.path.join(REPORT_DIR, f) for f in os.listdir(REPORT_DIR)],
        key=os.path.getmtime,
        reverse=True
    )
    if not reports:
        return None
    latest_file = reports[0]
    with open(latest_file, "r", encoding="utf-8") as rf:
        return rf.read()

def load_recent_logs(limit=5):
    """Load last few log lines for summary context."""
    if not os.path.exists(LOG_DIR):
        return []
    logs = sorted(
        [os.path.join(LOG_DIR, f) for f in os.listdir(LOG_DIR)],
        key=os.path.getmtime,
        reverse=True
    )
    lines = []
    for log in logs[:limit]:
        try:
            with open(log, "r", encoding="utf-8") as lf:
                content = lf.readlines()
                lines.extend(content[-3:])  # last few lines
        except Exception:
            pass
    return lines[-10:]  # last 10 lines total

def send_discord_message(title, description, color=0x00ffcc):
    """Send embed message to Discord."""
    if not DISCORD_WEBHOOK:
        print("⚠️ No Discord webhook found. Skipping send.")
        return

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "footer": {"text": f"Digital Sentinel v11.1 • {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"}
    }

    payload = {"username": "Digital Sentinel", "embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ Discord report sent successfully.")
        else:
            print(f"⚠️ Discord webhook responded with status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send Discord message: {e}")

def main():
    print("📡 Preparing Discord mission report...")

    report = load_latest_report()
    logs = load_recent_logs()

    if not report and not logs:
        send_discord_message(
            "⚠️ No data available for report.",
            "No reports or logs found to send.",
            color=0xffaa00
        )
        return

    desc = ""
    if report:
        desc += f"📜 **Latest Report Extract:**\n```{report[:800]}```\n"
    if logs:
        desc += f"🧠 **Recent Log Highlights:**\n```{''.join(logs[-10:])}```"

    send_discord_message(
        "🛰️ Digital Sentinel Mission Summary",
        desc,
        color=0x1e90ff
    )

if __name__ == "__main__":
    main()
