# ============================================================
# Digital Sentinel v6 - Main Quantum Controller v11.4
# Author: Themoralhack & Manus AI
# Mission: Autonomous scanning and reporting system for
#          authorized bug bounty reconnaissance.
# ============================================================

import os
import time
import json
import traceback

from datetime import datetime

# === Internal modules ===
from enumeration_engine import run_enumeration_batch
from probing_engine import run_probing_batch
from crawler_engine import run_crawling_batch
from vulnerability_scanner import run_vulnerability_scan_batch
from ai_analyzer import run_ai_analysis_batch

# 🧠 Discord reporting system
try:
    from sentinel_discord_reporter_v2 import send_discord_report as send_finding_report
except ImportError:
    print("[⚠️ WARN] Discord reporter module not found; reporting disabled.")
    send_finding_report = None


# ------------------------------------------------------------
# Environment setup
# ------------------------------------------------------------
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_WEBHOOK_URL:
    print("⚠️ Environment variable 'DISCORD_WEBHOOK_URL' not found!")
    print("💡 Please add it in GitHub repository secrets as: DISCORD_WEBHOOK_URL")
    print("Example: https://discord.com/api/webhooks/XXXXXXXXX/YYYYYYYYY")
    time.sleep(2)


# ------------------------------------------------------------
# Utility: load targets
# ------------------------------------------------------------
def load_targets(file_path="data/targets.txt"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Target list file not found: {file_path}")

    with open(file_path, "r") as f:
        targets = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
    return targets


# ------------------------------------------------------------
# Quantum main logic
# ------------------------------------------------------------
def main_cycle():
    print("\n🚀 [QUANTUM] Launching Main Quantum Controller v11.4")
    print("===================================================")

    start_time = datetime.now()
    cycle_id = start_time.strftime("%Y%m%d_%H%M%S")

    try:
        # === Phase 1: Load targets ===
        targets = load_targets()
        print(f"[🎯] Loaded {len(targets)} targets for scanning.")

        # === Phase 2: Enumeration ===
        enumeration_results = run_enumeration_batch(targets)

        # === Phase 3: Probing ===
        probing_results = run_probing_batch(enumeration_results)

        # === Phase 4: Crawling ===
        crawling_results = run_crawling_batch(probing_results)

        # === Phase 5: Vulnerability scanning ===
        vuln_results = run_vulnerability_scan_batch(crawling_results)

        # === Phase 6: AI-based analysis ===
        final_report = run_ai_analysis_batch(vuln_results)

        # === Phase 7: Save report locally ===
        os.makedirs("data/results/final_reports", exist_ok=True)
        report_path = f"data/results/final_reports/report_{cycle_id}.json"

        with open(report_path, "w") as f:
            json.dump(final_report, f, indent=2)
        print(f"[💾] Final report saved at: {report_path}")

        # === Phase 8: Send report to Discord ===
        if send_finding_report and DISCORD_WEBHOOK_URL:
            print("[📡] Sending summary report to Discord channel...")
            send_finding_report(final_report)
            print("[✅] Report successfully sent to Discord.")
        else:
            print("[⚠️] Discord webhook not available, skipping report send.")

        print("\n✨ [QUANTUM] Cycle completed successfully!")
        duration = datetime.now() - start_time
        print(f"⏱ Total runtime: {duration}")

    except Exception as e:
        error_info = traceback.format_exc()
        print(f"\n[💥 ERROR] Quantum cycle failed: {e}")
        print(error_info)

        # Save error log
        os.makedirs("data/logs", exist_ok=True)
        log_path = f"data/logs/error_{cycle_id}.log"
        with open(log_path, "w") as f:
            f.write(error_info)
        print(f"[🧾] Error details saved at: {log_path}")

        # Send to Discord if possible
        if send_finding_report and DISCORD_WEBHOOK_URL:
            send_finding_report({
                "status": "failed",
                "error": str(e),
                "trace": error_info,
                "timestamp": cycle_id
            })
            print("[⚠️] Error notification sent to Discord.")


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    print("[🧠] Digital Sentinel Quantum Autonomous Cycle")
    print("[🔁] Initializing...")
    time.sleep(1)
    main_cycle()
