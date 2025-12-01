import os
import re
import json
from datetime import datetime

# ==============================================================
#  DIGITAL SENTINEL MODULE — ai_vuln_detector.py
#  Purpose: Analyze logs and detect potential vulnerabilities
# ==============================================================

LOG_DIR = "data/logs"
OUTPUT_DIR = "data/reports"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"ai_vuln_findings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

# --- Keyword database for initial AI pattern matching ---
AI_SIGNATURES = {
    "SQLi": ["SELECT ", "UNION ALL", "DROP TABLE", "INSERT INTO", "UPDATE ", "WHERE 1=1"],
    "XSS": ["<script>", "onerror=", "alert(", "document.cookie", "javascript:"],
    "SSRF": ["file://", "gopher://", "127.0.0.1", "metadata.google.internal"],
    "Command Injection": ["; ls", "; cat /etc/passwd", "| whoami", "&&"],
    "Path Traversal": ["../", "/etc/passwd", "/root/.ssh"],
    "API Key Leak": ["api_key=", "Authorization:", "Bearer "],
    "Sensitive Info": ["password=", "secret=", "private_key", "token=", "aws_access_key_id"],
}


def scan_line_for_signatures(line):
    """Check a single line for vulnerability patterns."""
    findings = []
    for vuln_type, signatures in AI_SIGNATURES.items():
        for sig in signatures:
            if sig.lower() in line.lower():
                findings.append(vuln_type)
    return list(set(findings))


def run_ai_analysis():
    """Run full analysis over all logs."""
    print("🧠 [INFO] AI Vulnerability Detector Running...")

    all_findings = []
    if not os.path.exists(LOG_DIR):
        print("[WARN] No logs found to analyze.")
        return

    for root, _, files in os.walk(LOG_DIR):
        for name in files:
            if not name.endswith((".log", ".txt")):
                continue
            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, start=1):
                        hits = scan_line_for_signatures(line)
                        if hits:
                            all_findings.append({
                                "file": name,
                                "line": i,
                                "content": line.strip()[:200],
                                "detections": hits
                            })
            except Exception as e:
                print(f"[WARN] Failed to scan {path}: {e}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not all_findings:
        print("[INFO] No vulnerabilities detected ✅")
    else:
        print(f"[INFO] {len(all_findings)} potential findings detected ⚠️")

    report = {
        "generated_at": datetime.now().isoformat(),
        "findings": all_findings,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"📄 [INFO] AI Findings saved to {OUTPUT_FILE}")
    return OUTPUT_FILE


def ai_vuln_detector():
    """Main entry for Digital Sentinel AI Analyzer"""
    return run_ai_analysis()
