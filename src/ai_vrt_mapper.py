# -----------------------------------------------------------
# Digital Sentinel v13 – AI VRT Mapper (Bugcrowd Format)
# Automatically creates the 6-section professional report:
#
# 1) Summary
# 2) Target
# 3) VRT Category
# 4) Vulnerability Details
# 5) Description
# 6) Evidence / Attachments
#
# Output is perfect for Bugcrowd submission.
# -----------------------------------------------------------

import os
import json
import requests

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
AI_MODEL = "gemini-1.5-flash"


def call_ai(prompt):
    if not GEMINI_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{AI_MODEL}:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        r = requests.post(url, json=payload, timeout=30)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return None


# -----------------------------------------------------------
# VRT Mapper
# -----------------------------------------------------------

def map_vrt(finding):
    """
    Input example:
    {
        "url": "https://example.com/profile?id=",
        "payload": "<script>alert(1)</script>",
        "severity": "high",
        "proof": "Screenshot base64…",
        "raw_request": "...",
        "raw_response": "..."
    }
    """

    prompt = f"""
You are a professional Bugcrowd triage analyst.
Your job: Create a **professional, clean, 6-section VRT bug bounty report**.

STRICT OUTPUT FORMAT (MUST be JSON only):

{{
  "summary": "",
  "target": "",
  "vrt_category": "",
  "details": "",
  "description": "",
  "evidence": ""
}}

Use the following raw finding to classify:

{json.dumps(finding, indent=2)}
"""

    result = call_ai(prompt)

    if not result:
        return {
            "summary": "AI unavailable",
            "target": finding.get("url", "unknown"),
            "vrt_category": "unknown",
            "details": "AI not reachable",
            "description": "",
            "evidence": ""
        }

    try:
        return json.loads(result)
    except:
        return {
            "summary": "AI parse error",
            "target": finding.get("url", "unknown"),
            "vrt_category": "unknown",
            "details": "AI returned invalid format",
            "description": "",
            "evidence": ""
        }


# -----------------------------------------------------------
# Bulk mapper (list of findings)
# -----------------------------------------------------------

def generate_vrt_reports(findings):
    reports = []

    for f in findings:
        rpt = map_vrt(f)
        reports.append(rpt)

    return reports
