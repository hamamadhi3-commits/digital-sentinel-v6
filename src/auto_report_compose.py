import os
import json
from datetime import datetime

# ==============================================================
#  DIGITAL SENTINEL MODULE — auto_report_compose.py
#  Purpose: Aggregate scan logs & AI detector output into final report
# ==============================================================

LOG_DIR = "data/logs"
REPORT_DIR = "data/reports"
OUTPUT_FILE = os.path.join(REPORT_DIR, f"sentinel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

def collect_logs():
    """Collect all .log and .txt outputs from log directory."""
    logs = []
    if not os.path.exists(LOG_DIR):
        return logs
    for root, _, files in os.walk(LOG_DIR):
        for name in files:
            if name.endswith(".log") or name.endswith(".txt"):
                path = os.path.join(root, name)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        logs.append({
                            "filename": name,
                            "path": path,
                            "content": f.read()
                        })
                except Exception as e:
                    print(f"[WARN] Could not read log file {name}: {e}")
    return logs


def compose_report():
    """Compose a final aggregated JSON report."""
    print("🧩 [INFO] Composing consolidated Digital Sentinel report...")

    os.makedirs(REPORT_DIR, exist_ok=True)
    all_logs = collect_logs()

    if not all_logs:
        print("[WARN] No logs found for report generation.")
        return

    report = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_logs": len(all_logs),
        },
        "logs": all_logs
    }

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"✅ [INFO] Report generated successfully: {OUTPUT_FILE}")
    except Exception as e:
        print(f"[ERROR] Could not write report: {e}")

    return OUTPUT_FILE
