# ============================================================
# Digital Sentinel v6 - Discord Reporter v2
# Author: Themoralhack & Manus AI
# Mission: Securely send notifications and reports to Discord.
# ============================================================

import os
import json
import requests
from datetime import datetime

# ============================================================
# 🧠 Core Config
# ============================================================

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_WEBHOOK_URL:
    print("⚠️ [Discord Reporter] Environment variable 'DISCORD_WEBHOOK_URL' not found!")
    print("💡 Add it in GitHub Secrets as: DISCORD_WEBHOOK_URL")
    print("Example: https://discord.com/api/webhooks/XXXX/XXXX")
else:
    print("[🔗] Discord Reporter Initialized.")


# ============================================================
# 🛰️ Helper: Send basic embed
# ============================================================

def send_discord_message(content=None, embed=None):
    """Send a plain or embedded message to Discord webhook."""
    if not DISCORD_WEBHOOK_URL:
        print("[⚠️] Discord Webhook missing — skipping message send.")
        return False

    payload = {"username": "🛰️ Digital Sentinel v6", "avatar_url": "https://i.imgur.com/bhO2VtC.png"}

    if content:
        payload["content"] = content
    if embed:
        payload["embeds"] = [embed]

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 204:
            print("[✅] Discord message sent successfully.")
        else:
            print(f"[⚠️] Discord returned status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[💥] Failed to send message to Discord: {e}")


# ============================================================
# 🧩 Main Function: send_finding_report()
# ============================================================

def send_finding_report(report_data):
    """
    Sends a summary of findings (or errors) to Discord.
    report_data should be dict with fields:
      - status
      - error / trace (optional)
      - vulnerability_summary
      - affected_urls, total_urls_scanned
    """
    print("[📡] Preparing Discord report message...")

    # Build dynamic title & color
    status = report_data.get("status", "success")
    color = 0x00FF00 if status == "success" else 0xFF0000

    title = "✅ Digital Sentinel Scan Completed" if status == "success" else "🚨 Sentinel Failure Detected"

    # Embed builder
    embed = {
        "title": title,
        "color": color,
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {"text": "Digital Sentinel v6 • Quantum Cycle"},
        "fields": []
    }

    # Add summary if available
    if "vulnerability_summary" in report_data:
        summary_lines = "\n".join(
            [f"• **{vuln.upper()}** → {count} hits" for vuln, count in report_data["vulnerability_summary"].items()]
        )
        embed["fields"].append({
            "name": "Vulnerability Summary",
            "value": summary_lines or "✅ No vulnerabilities found.",
            "inline": False
        })

    if "affected_urls" in report_data:
        embed["fields"].append({
            "name": "Statistics",
            "value": f"Total URLs Scanned: **{report_data.get('total_urls_scanned', '?')}**\n"
                     f"Affected URLs: **{report_data.get('affected_urls', '?')}**",
            "inline": False
        })

    if "analysis_comment" in report_data:
        embed["fields"].append({
            "name": "AI Comment",
            "value": report_data["analysis_comment"],
            "inline": False
        })

    # Add error details if failed
    if status == "failed":
        embed["fields"].append({
            "name": "Error Details",
            "value": f"```\n{report_data.get('error', 'Unknown error')}\n```",
            "inline": False
        })

    # Send message
    send_discord_message(embed=embed)
    print("[🚀] Discord report dispatched.")
