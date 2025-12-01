import json, re, os

INPUT = "data/reports/recon_raw/recon_result.json"
OUTPUT = "data/reports/ai_findings.json"

PATTERNS = {
    "XSS": ["<script>", "alert(", "onerror="],
    "SQLi": ["UNION SELECT", "information_schema", "sql syntax"],
    "Misconfig": ["Index of /", "Server: Apache/2"],
}

def detect():
    print("🧠 AI Detector Scanning…")
    data = json.load(open(INPUT))
    findings = []

    for entry in data:
        content = entry.get("headers", "")
        for vuln_type, signs in PATTERNS.items():
            if any(re.search(sign, content, re.IGNORECASE) for sign in signs):
                findings.append({
                    "domain": entry["domain"],
                    "type": vuln_type,
                    "evidence": content[:200]
                })
    os.makedirs("data/reports", exist_ok=True)
    json.dump(findings, open(OUTPUT, "w"), indent=2)
    print(f"✅ {len(findings)} potential findings saved")

if __name__ == "__main__":
    detect()
