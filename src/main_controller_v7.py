import os
import time
from datetime import datetime

from src.recon_engine_parallel import run_recon_cycle
from src.ai_vuln_detector import ai_vuln_detector
from src.duplication_checker import check_duplicates
from src.auto_report_compose import compose_report
from src.discord_notify import send_discord_alert

# ==============================================================
#  DIGITAL SENTINEL v6.5 — INTELLIGENT AUTONOMOUS CONTROLLER
#  Master brain of the Digital Sentinel ecosystem
# ==============================================================

LOG_DIR = "data/logs"
REPORT_DIR = "data/reports"
TARGET_FILE = "data/targets/global_500_targets.txt"

CYCLE_LIMIT = int(os.getenv("MAX_CYCLES", "1"))       # For scheduled automation
SLEEP_INTERVAL = int(os.getenv("CYCLE_INTERVAL", "10"))  # Delay between cycles (seconds)


def main_cycle():
    """Run one autonomous intelligent cycle."""
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    cycle_start = datetime.now()
    print(f"\n🚀 [START] Digital Sentinel v6.5 Intelligent Cycle — {cycle_start}")

    # Step 1 — Reconnaissance Phase
    try:
        print("🌐 [PHASE 1] Reconnaissance Engine Running...")
        recon_result = run_recon_cycle(TARGET_FILE)
        print("✅ Reconnaissance completed successfully.")
    except Exception as e:
        print(f"❌ [ERROR] Recon failed: {e}")
        send_discord_alert("Recon Failure", str(e))
        recon_result = None

    # Step 2 — AI Vulnerability Detection
    try:
        print("🧠 [PHASE 2] AI Vulnerability Analysis Started...")
        vuln_report = ai_vuln_detector()
        print(f"✅ AI Vulnerability Analysis Finished → {vuln_report}")
    except Exception as e:
        print(f"❌ [ERROR] AI Analysis failed: {e}")
        send_discord_alert("AI Analyzer Failure", str(e))

    # Step 3 — Duplicate Report Cleaning
    try:
        print("🔍 [PHASE 3] Checking for duplicate reports...")
        check_duplicates()
    except Exception as e:
        print(f"⚠️ [WARN] Duplication check failed: {e}")

    # Step 4 — Report Composing
    try:
        print("📊 [PHASE 4] Composing consolidated report...")
        compose_report()
        print("✅ Report composed successfully.")
    except Exception as e:
        print(f"⚠️ [WARN] Report compose failed: {e}")

    # Step 5 — Finalization
    cycle_end = datetime.now()
    duration = (cycle_end - cycle_start).total_seconds()
    print(f"\n🏁 [COMPLETE] Cycle finished in {duration:.2f}s — {cycle_end}")
    send_discord_alert("Digital Sentinel v6.5 Cycle Completed",
                       f"Duration: {duration:.2f}s\nTime: {cycle_end}")


def run_autonomous_loop():
    """Run multiple cycles in autonomous intelligent mode."""
    print("🤖 [INFO] Digital Sentinel v6.5 – Autonomous Intelligence Active")
    for i in range(CYCLE_LIMIT):
        print(f"\n🌀 [LOOP] Starting Cycle {i + 1}/{CYCLE_LIMIT}")
        main_cycle()
        if i + 1 < CYCLE_LIMIT:
            print(f"⏳ Sleeping for {SLEEP_INTERVAL}s before next cycle...")
            time.sleep(SLEEP_INTERVAL)
    print("🌙 [INFO] All autonomous cycles completed.")


if __name__ == "__main__":
    run_autonomous_loop()
