import requests
import json
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "").strip()

def _send(message: str):
    if not DISCORD_WEBHOOK:
        print("⚠️ No Discord Webhook Found!")
        return

    payload = {"content": message}

    try:
        requests.post(
            DISCORD_WEBHOOK,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        print("📤 Discord Message Sent")
    except Exception as e:
        print(f"❌ Discord Send Error: {e}")


# -------------------------------------------------
#   SEND FINDING REPORT (Single Vuln)
# -------------------------------------------------
def send_finding_report(finding):
    sev = finding.get("severity", "UNKNOWN")
    target = finding.get("target", "unknown target")
    title = finding.get("title", "No title")
    url = finding.get("url", "No url")

    msg = f"""
🔎 **New Vulnerability Found**
🎯 Target: `{target}`
⚠️ Severity: **{sev}**
📌 {title}
🔗 {url}
"""
    _send(msg)


# -------------------------------------------------
#   SEND EXPLOIT-CHAIN REPORT
# -------------------------------------------------
def send_chain_report(chain):
    msg = "🔥 **EXPLOIT CHAIN DETECTED!**\n"
    msg += f"Total steps: {len(chain)}\n\n"

    for step in chain:
        msg += f"➡️ {step.get('title', 'Unknown')} (Severity: {step.get('severity')})\n"

    _send(msg)
