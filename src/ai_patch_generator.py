# ---------------------------------------------------------
# Digital Sentinel v11.1 – AI Patch Generator (Phase 11)
# Creates code-level fixes for vulnerabilities.
# ---------------------------------------------------------

import os
import json
import requests

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
AI_MODEL = "gemini-1.5-flash"


def call_ai(prompt):
    """Call Gemini AI."""
    if not GEMINI_KEY:
        return "AI key missing – cannot generate fix."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{AI_MODEL}:generateContent?key={GEMINI_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        r = requests.post(url, json=payload, timeout=25)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Patch generation failed."


# ---------------------------------------------------------
# Patch Builder
# ---------------------------------------------------------

def build_patch(vuln):
    """
    vuln example:
    {
        "summary": "Possible XSS injection point",
        "url": "https://test.com/?q=test",
        "impact": "medium"
    }
    """

    patch_prompt = f"""
You are a senior application security engineer.

Your task:
Generate a CLEAN, PROFESSIONAL code fix for this vulnerability.
Include:

1. Summary title
2. Risk explanation
3. Secure code patch (full code block)
4. Why this patch works (short)
5. Long-term security recommendation

Vulnerability Data:
{json.dumps(vuln, indent=2)}

Format MUST be clean.
"""

    return call_ai(patch_prompt)


# ---------------------------------------------------------
# Public function
# ---------------------------------------------------------

def generate_patch_list(findings):
    patches = []

    for f in findings:
        fix = build_patch(f)

        patches.append({
            "title": f["summary"],
            "patch": fix
        })

    return patches
