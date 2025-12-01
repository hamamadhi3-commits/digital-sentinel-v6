"""
Digital Sentinel v6.0 – Auto Report Composer
Purpose: Automatically generates a vulnerability summary report
"""

import os
import json
from datetime import datetime

def generate_report(report_directory="data/reports"):
    """Collects scan logs and composes a consolidated report"""
    os.makedirs(report_directory, exist_ok=True)
    log_dir = "data/logs"
    report_path = os.path.join(report_directory, f"sentinel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    summary = {
        "version": "6.0",
        "generated_at": str(datetime.now()),
        "targets": [],
        "total_scanned": 0,
        "vulnerabilities": []
    }

    # Iterate logs
    for file in os.listdir(log_dir):
        if file.endswith(".log"):
            with open(os.path.join(log_dir, file), "r") as lf:
                try:
                    data = json.load(lf)
                    summary["targets"].append(data["target"])
                    summary["total_scanned"] += 1
                    if "vulns" in data and data["vulns"]:
                        summary["vulnerabilities"].extend(data["vulns"])
                except Exception as e:
                    print(f"[WARN] Failed to read {file}: {e}")

    with open(report_path, "w") as rf:
        json.dump(summary, rf, indent=2)

    print(f"[REPORT] Generated summary report → {report_path}")
    return report_path
