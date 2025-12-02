# ---------------------------------------------------------
# Digital Sentinel v11.1 – AI PoC Maker (Phase 10)
# Generates full PoC + report text for Bugcrowd/HackerOne
# ---------------------------------------------------------

import os
import json
import requests

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

AI_MODEL = "gemini-1.5-flash"


def ask_ai(prompt):
    """Send a prompt to Gemini AI."""
    if not GEMINI_KEY:
        return "AI key not set. Cannot generate PoC."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{AI_MODEL}:generateContent?key={GEMINI_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        r = requests.post(url, json=payload, timeout=20)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI generation failed."


# ---------------------------------------------------------
# Build a full PoC report text for a vuln
# ---------------------------------------------------------

def build_poc(vuln):
    """
    Input format example:
    {
        "summary": "Possible XSS injection point",
        "url": "https://example.com/?q=test",
        "impact": "medium",
        "vector": "network",
        "ease": "easy"
    }
    """

    prompt = f"""
You are a professional bug bounty analyst.

Generate a full vulnerability PoC with these sections:

1. Summary title
2. Target
3. VRT Category
4. Vulnerability details (technical)
5. Description (human readable)
6. Attachments (what tester should provide)

Use professional Bugcrowd format.

Vulnerability data:
{json.dumps(vuln, indent=2)}
"""

    return ask_ai(prompt)


# ---------------------------------------------------------
# Public function called from controller
# ---------------------------------------------------------

def generate_poc_report(findings):
    """
    findings = list of detected vulnerabilities
    returns: list of { "title":..., "content":... }
    """

    reports = []

    for f in findings:
        poc = build_poc(f)

        reports.append({
            "title": f["summary"],
            "content": poc
        })

    return reports
