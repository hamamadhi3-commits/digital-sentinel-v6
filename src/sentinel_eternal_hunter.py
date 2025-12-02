#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel v11 – Eternal Hunter Autonomous Subsystem (Fixed)
Safely handles report directory conflicts and overwrites.
"""

import os
import json
import time
from datetime import datetime


REPORT_DIR = "data/reports"
REPORT_FILE = os.path.join(REPORT_DIR, "eternal_hunter_summary.json")


def ensure_report_dir():
    """Safely ensure the reports directory exists, even if a file blocks it."""
    if os.path.exists(REPORT_DIR):
        # If it's a file (not a folder), delete and recreate
        if not os.path.isdir(REPORT_DIR):
            print(f"[⚠️] {REPORT_DIR} exists as a file. Removing and recreating directory...")
            os.remove(REPORT_DIR)
            os.makedirs(REPORT_DIR, exist_ok=True)
    else:
        os.makedirs(REPORT_DIR, exist_ok=True)


def simulate_scan(targets):
    """Simulate autonomous reconnaissance scans."""
    results = []
    for t in targets:
        result = {
            "target": t,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "active",
            "response_time_ms": round(50 + 100 * (hash(t) % 10) / 10, 2),
            "vulnerabilities_found": hash(t) % 3
        }
        results.append(result)
        time.sleep(0.2)
    return results


def generate_summary(results):
    """Generate and safely write the summary report."""
    ensure_report_dir()

    summary = {
        "report_time": datetime.utcnow().isoformat(),
        "total_targets": len(results),
        "vulnerabilities_detected": sum(r["vulnerabilities_found"] for r in results),
        "average_latency_ms": round(sum(r["response_time_ms"] for r in results) / len(results), 2) if results else 0,
        "results": results
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"[✅] Report successfully written to {REPORT_FILE}")
    return summary


def execute_hunt_cycle(targets):
    """Full scan + reporting routine."""
    print("🚀 Launching Sentinel Eternal Hunter v11")
    results = simulate_scan(targets)
    summary = generate_summary(results)
    print(f"[🧠] Eternal Hunter completed scan of {len(targets)} targets.")
    return summary


if __name__ == "__main__":
    targets = [
        "apple.com",
        "microsoft.com",
        "tesla.com",
        "google.com",
        "meta.com",
        "cloudflare.com",
        "openai.com"
    ]

    print(">>> Starting sentinel_eternal_hunter.py")
    try:
        execute_hunt_cycle(targets)
    except Exception as e:
        print(f"[❌] Eternal Hunter encountered an error: {e}")
        exit(1)

    print("[✅] Eternal Hunter completed successfully.")
