# Digital Sentinel v9 – Discord Reporter (Updated for Chains)
# -----------------------------------------------------------

import requests
import json
import os

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_chain_report(chain):
    if not WEBHOOK:
        return

    text = f"""
🚨 **EXPLOIT CHAIN DETECTED**  
**Domain:** {chain['domain']}
**Type:** {chain['type']}
**Severity:** {chain['severity']}
**CVSS:** {chain['score']}
**Reward Prediction:** {chain['reward']}

**Exploit Steps:**
{" → ".join(chain['steps'])}
"""

    payload = {"content": text}

    requests.post(WEBHOOK, json=payload)
