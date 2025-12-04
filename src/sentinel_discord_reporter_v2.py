# ============================================================
# Digital Sentinel - Discord Vulnerability Reporter v2
# ============================================================

import os
import json
import requests
from datetime import datetime

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()

if not DISCORD_WEBHOOK_URL:
    print("[⚠️] No Discord Webhook URL found in environment variable 'DISCORD_WEBHOOK_URL'!")
    print("[💡] Please add it in GitHub repository secrets as: DISCORD_WEBHOOK_URL")
else:
    print("[🔗] Discord Webhook detected successfully.")


# ------------------------------------------------------------
# Helper Function: Format Report
# ------------------------------------------------------------
def format_discord_message(finding):
    """
    Format a finding into a Discord message payload (Embed style)
    """

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    embed = {
        "title": f"🛡️ New Vulnerability Discovered on {finding.get('target', 'Unknown Target')}",
        "color": 15158332,  # red color
        "fields": [
            {"name": "🎯 Target", "value": finding.get("target", "Unknown"), "inline": False},
            {"name": "📁 Category", "value": finding.get("category", "N/A"), "inline": True},
            {"name": "⚙️ Severity", "value": finding.get("severity", "N/A"), "inline": True},
            {"name": "🌐 URL", "value": finding.get("url", "N/A"), "inline": False},
            {"name": "🧠 AI Note", "value": finding.get("ai_note", "N/A"), "inline": False},
            {"name": "🧩 Description", "value": finding.get("description", "No details provided."), "inline": False},
            {"name": "💣 Proof of Concept", "value": f"```bash\n{finding.get('poc', 'N/A')}\n```", "inline": False},
            {"name": "🕓 Detected At", "value": timestamp, "inline": False}
        ],
        "footer": {"text": "Digital Sentinel v6 • Quantum Cycle"},
    }

    payload = {"embeds": [embed]}
    return payload


# ------------------------------------------------------------
# Main Reporter Function
# ------------------------------------------------------------
def send_discord_report(findings):
    """
    Send all vulnerability findings to Discord in rich embed format.
    """

    if not findings:
        print("[ℹ️] No findings to report.")
        return

    if not DISCORD_WEBHOOK_URL:
        print("[🚫] Cannot send to Discord - webhook not configured.")
        return

    print(f"[📡] Sending {len(findings)} findings to Discord...")

    for finding in findings:
        try:
            payload = format_discord_message(finding)
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)

            if response.status_code == 204:
                print(f"[✅] Report sent successfully for {finding.get('target')}")
            else:
                print(f"[⚠️] Failed to send report for {finding.get('target')} - "
                      f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            print(f"[❌] Error sending report: {e}")

    print("[🏁] Discord reporting cycle completed.")
