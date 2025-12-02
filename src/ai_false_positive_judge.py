# ---------------------------------------------------------
# Digital Sentinel v12 – AI False Positive Judge
# Removes weak / fake / duplicate / invalid findings
# Keeps only real, high-value vulnerabilities
# ---------------------------------------------------------

import os
import requests
import json

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
AI_MODEL = "gemini-1.5-flash"


def call_ai(prompt):
    if not GEMINI_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{AI_MODEL}:generateContent?key={GEMINI_KEY}"

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        r = requests.post(url, json=payload, timeout=25)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return None


# ---------------------------------------------------------
# Judge function
# ---------------------------------------------------------

def judge_finding(f):
    """
    f example:
    {
        "summary": "XSS found",
        "url": "...",
        "severity": "medium",
        "proof": "alert(1)",
        "raw_request": "...",
        "raw_response": "..."
    }
    """

    prompt = f"""
You are an Application Security AI Judge.
Determine if this finding is VALID or FALSE-POSITIVE.

Rules:
- Reject trivial reflections.
- Reject errors caused by CDN, WAF, rate-limit.
- Reject findings reported previously by anyone.
- Reject anything without strong PoC.
- Reject if impact is too small.
- Validate only: CRITICAL / HIGH / strong MEDIUM.
- MUST respond in pure JSON with this structure:

{{
  "valid": true/false,
  "reason": "string explanation",
  "final_severity": "critical/high/medium"
}}

Finding:
{json.dumps(f, indent=2)}
"""

    result = call_ai(prompt)

    if not result:
        return {"valid": False, "reason": "AI unavailable", "final_severity": "none"}

    try:
        clean = json.loads(result)
        return clean
    except:
        return {"valid": False, "reason": "AI bad format", "final_severity": "none"}


# ---------------------------------------------------------
# Bulk judge
# ---------------------------------------------------------

def filter_valid_findings(findings):
    good = []

    for f in findings:
        decision = judge_finding(f)

        if decision["valid"]:
            f["severity"] = decision["final_severity"]
            f["judge_reason"] = decision["reason"]
            good.append(f)

    return good
