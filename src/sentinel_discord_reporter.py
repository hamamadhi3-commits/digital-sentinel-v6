import os
import json
import requests

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "").strip()

def send(msg):
    if not DISCORD_WEBHOOK:
        print("❌ No DISCORD_WEBHOOK!")
        return

    try:
        requests.post(
            DISCORD_WEBHOOK,
            data=json.dumps({"content": msg}),
            headers={"Content-Type": "application/json"},
            timeout=8
        )
        print("📤 Discord message sent.")
    except Exception as e:
        print(f"❌ Discord error: {e}")

# Report for single finding
def send_finding_report(f):
    sev = f.get("severity", "UNKNOWN")
    tgt = f.get("host", "unknown")
    tpl = f.get("template-id", "N/A")

    msg = f"""
🔎 **New Finding**
🎯 Target: `{tgt}`
⚠️ Severity: **{sev}**
📄 Template: `{tpl}`
"""
    send(msg)

# Chain report (Phase 9)
def send_chain_report(chain):
    text = "🔥 **EXPLOIT CHAIN DETECTED!**\n\n"
    for c in chain:
        text += f"➡️ {c.get('template-id')} (Severity: {c.get('severity')})\n"
    send(text)
