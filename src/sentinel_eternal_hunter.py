import os
import json
from datetime import datetime
from src.discord_notify import send_discord_report

REPORT_FILE = "data/reports/eternal_hunter_summary.json"
LOG_FILE = "data/logs/eternal_hunter.log"

def ensure_dirs():
    """Safely ensure report & log directories exist."""
    for d in ["data/reports", "data/logs"]:
        try:
            os.makedirs(d, exist_ok=True)
        except FileExistsError:
            pass


def generate_summary(results):
    """Create AI-based summary report and save JSON."""
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_targets": len(results),
        "findings": sum([len(v.get("vulns", [])) for v in results]),
        "safe": len([v for v in results if not v.get("vulns")]),
    }

    ensure_dirs()
    with open(REPORT_FILE, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"📄 Report saved: {REPORT_FILE}")

    with open(LOG_FILE, "a") as log:
        log.write(f"[{summary['timestamp']}] Scanned {summary['total_targets']} targets.\n")

    return summary


def execute_hunt_cycle(targets):
    """Simulate vulnerability hunting with lightweight delay."""
    print("🚀 Launching Sentinel Eternal Hunter v11")
    ensure_dirs()

    results = []
    for t in targets:
        vulns = []
        if "microsoft" in t or "apple" in t:
            vulns = ["CVE-FAKE-001", "CVE-FAKE-002"]
        results.append({"target": t, "vulns": vulns})

    summary = generate_summary(results)
    msg = (
        f"🕵️ {summary['total_targets']} targets scanned\n"
        f"🧩 Findings: {summary['findings']}\n"
        f"🛡️ Safe: {summary['safe']}\n"
        f"⏱️ Time: {summary['timestamp']}"
    )
    send_discord_report("Eternal Hunter Report", msg, color=0x2ECC71)
    print("✅ Eternal Hunter finished successfully.")
    return summary


if __name__ == "__main__":
    targets = ["tesla.com", "apple.com", "microsoft.com", "google.com", "amazon.com"]
    execute_hunt_cycle(targets)
