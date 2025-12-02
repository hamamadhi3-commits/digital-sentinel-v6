import json
import random
import string
import requests
from datetime import datetime

# --------------------------------------------
#  Auto PoC Generator — Digital Sentinel v7.0
# --------------------------------------------

def random_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))

def generate_poc(finding, domain):
    """
    Create a professional PoC similar to HackerOne/Tesla reports.
    """
    url = finding.get("url", f"https://{domain}")
    payload = finding.get("payload", f"?test={random_token()}")

    poc = {
        "title": finding.get("summary", "Untitled Vulnerability"),
        "target": domain,
        "url": url,
        "steps": [
            "1. Open the vulnerable endpoint:",
            f"   {url}",
            "2. Attach payload:",
            f"   " + payload,
            "",
            "3. Observe abnormal behavior:",
            f"   → " + finding.get("effect", "Unexpected server response / bypass"),
        ],
        "curl": f"curl -X GET '{url}{payload}' -H 'User-Agent: DigitalSentinel-AutoPoC'",
        "raw_request": f"""
GET {url}{payload} HTTP/1.1
Host: {domain}
User-Agent: DigitalSentinel-AutoPoC
Accept: */*
""",
        "expected": "Normal server validation or block",
        "actual": finding.get("effect", "Server accepts malicious payload"),
        "evidence": finding.get("evidence", "Server responded with 200 OK, payload executed."),
        "timestamp": datetime.utcnow().isoformat()
    }

    return poc


def validate_poc(poc):
    """
    Actually send the PoC request to confirm if the issue is real.
    """
    try:
        response = requests.get(
            poc["url"],
            headers={"User-Agent": "DigitalSentinel-AutoPoC"},
            timeout=6
        )
        return {
            "status": response.status_code,
            "success": True if response.status_code < 500 else False,
            "response_sample": response.text[:250]
        }
    except Exception as e:
        return {"status": "error", "success": False, "response_sample": str(e)}


def poc_to_text(poc, validation):
    """
    Convert PoC into a formatted text block for Discord.
    """
    text = f"""
🚨 Auto-Generated PoC (Digital Sentinel v7.0)
====================================

🎯 **Target:** {poc['target']}
🔗 **URL:** {poc['url']}

📌 **Summary:** {poc['title']}

🔍 **Steps to Reproduce**
```
{chr(10).join(poc['steps'])}
```

📡 **CURL Command**
```
{poc['curl']}
```

📝 **Raw HTTP Request**
```
{poc['raw_request']}
```

✅ **Validation Result**
Status: {validation['status']}
Server Says:
```
{validation['response_sample']}
```

🧪 Expected:
```
{poc['expected']}
```
⚠ Actual:
```
{poc['actual']}
```

📎 Evidence:
```
{poc['evidence']}
```
    """

    return text.strip()
