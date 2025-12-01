"""
Digital Sentinel v6.0 – Main Controller
Author: Mhamad Mahdy
Purpose: Coordinates the autonomous scanning cycle
"""

import os
import time
import json
import concurrent.futures
from datetime import datetime
from src.recon_engine_parallel import run_recon_parallel
from src.auto_report_compose import generate_report
from src.discord_notify import send_discord_alert

# Load configuration
with open("data/targets/config.json", "r") as cfg:
    CONFIG = json.load(cfg)

TARGET_FILE = CONFIG["target_file"]
SCAN_INTERVAL = CONFIG["scan_interval_minutes"] * 60
MAX_THREADS = CONFIG["threads"]
LOG_DIR = CONFIG["log_directory"]
REPORT_DIR = CONFIG["report_directory"]

def load_targets():
    """Read target list from text file."""
    try:
        with open(TARGET_FILE, "r") as f:
            targets = [line.strip() for line in f if line.strip()]
        print(f"[INFO] Loaded {len(targets)} targets from {TARGET_FILE}")
        return targets
    except Exception as e:
        print(f"[ERROR] Failed to load targets: {e}")
        return []

def main_cycle():
    """Main scanning loop"""
    print(f"\n🛰️  Digital Sentinel v6.0 — Autonomous Mode Started at {datetime.now()}")
    targets = load_targets()
    if not targets:
        print("[WARN] No targets found. Exiting.")
        return

    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    # Parallel Execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_target = {executor.submit(run_recon_parallel, target): target for target in targets}
        for future in concurrent.futures.as_completed(future_to_target):
            target = future_to_target[future]
            try:
                result = future.result()
                print(f"[DONE] {target}: {result}")
            except Exception as e:
                print(f"[FAIL] {target}: {e}")

    # Generate report
    generate_report(REPORT_DIR)

    # Discord notification
    try:
        send_discord_alert(f"✅ Digital Sentinel completed a full recon cycle at {datetime.now()}")
    except Exception as e:
        print(f"[WARN] Discord notification failed: {e}")

if __name__ == "__main__":
    while True:
        main_cycle()
        print(f"🕒 Sleeping for {CONFIG['scan_interval_minutes']} minutes...\n")
        time.sleep(SCAN_INTERVAL)
