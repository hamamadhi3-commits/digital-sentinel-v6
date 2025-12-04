#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Digital Sentinel Quantum v11.4
Autonomous Vulnerability Hunter – AI Enhanced + Watchdog
"""

import os
import sys
import time
import json
import traceback
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from ai_priority import analyze_vulnerability
from chain_detector import detect_exploit_chains
from sentinel_discord_reporter import send_chain_report, send_finding_report
from sentinel_scan_engine import run_full_scan

# ==========================
# CONFIGURATION
# ==========================
TARGET_FILE = "data/targets/global_500_targets.txt"
RESULT_DIR = "data/results"
LOG_DIR = "data/logs"
MAX_THREADS = 20
SLEEP_AFTER_CYCLE = 60 * 60 * 6  # 6 hours
MAX_RETRIES = 3

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

MAIN_LOG = os.path.join(LOG_DIR, f"controller_{int(time.time())}.log")


# ==========================
# LOGGING SYSTEM
# ==========================
def log(msg):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(MAIN_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ==========================
# LOAD TARGETS
# ==========================
def load_targets():
    if not os.path.exists(TARGET_FILE):
        log("❌ Target file not found!")
        return []
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        domains = [l.strip() for l in f if l.strip()]
    return domains


# ==========================
# SAVE FINDINGS
# ==========================
def save_result(domain, findings):
    outf = os.path.join(RESULT_DIR, f"{domain}_findings.json")
    with open(outf, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2)
    log(f"📁 Saved results for {domain}")


# ==========================
# WORKER FUNCTION
# ==========================
def process_target(domain):
    attempt = 1
    while attempt <= MAX_RETRIES:
        try:
            log(f"🟦 [{attempt}/{MAX_RETRIES}] Scanning {domain}")
            results = run_full_scan(domain)

            if not results:
                log(f"⚠️ No results found for {domain}")
                return []

            enhanced = [analyze_vulnerability(f, domain) for f in results]
            save_result(domain, enhanced)

            for f in enhanced:
                if f.get("cvss", 0) >= 5:
                    send_finding_report(f)

            return enhanced

        except Exception as e:
            log(f"❌ Error scanning {domain}: {e}")
            traceback.print_exc()
            attempt += 1
            time.sleep(10)

    log(f"🚫 Max retries reached for {domain}")
    return []


# ==========================
# MAIN CONTROLLER LOOP
# ==========================
def main_controller():
    log("🚀 Starting Digital Sentinel Quantum v11.4 Autonomous Cycle")

    while True:
        try:
            targets = load_targets()
            total = len(targets)
            if total == 0:
                log("⚠️ No targets found. Sleeping for 30 min...")
                time.sleep(1800)
                continue

            log(f"🎯 Loaded {total} targets for scanning")
            all_findings = []

            # Parallel scan
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                futures = {executor.submit(process_target, domain): domain for domain in targets}

                for future in as_completed(futures):
                    domain = futures[future]
                    try:
                        findings = future.result()
                        if findings:
                            all_findings.extend(findings)
                            log(f"✅ Completed {domain}")
                        else:
                            log(f"⚠️ No findings for {domain}")
                    except Exception as e:
                        log(f"❌ Worker crash on {domain}: {e}")

            # Detect exploit chains
            log("🧩 Running Exploit Chain Detection...")
            chains = detect_exploit_chains(all_findings)
            if chains:
                log(f"🔥 {len(chains)} exploit chains detected.")
                for ch in chains:
                    send_chain_report(ch)
            else:
                log("ℹ️ No exploit chains this cycle.")

            # Sleep before next cycle
            log(f"⏳ Cycle complete. Sleeping {SLEEP_AFTER_CYCLE / 3600} hours before restart...")
            time.sleep(SLEEP_AFTER_CYCLE)

        except Exception as e:
            log(f"💥 Fatal Controller Error: {e}")
            traceback.print_exc()
            log("♻️ Restarting in 60 seconds...")
            time.sleep(60)
            continue


# ==========================
# ENTRY POINT
# ==========================
if __name__ == "__main__":
    try:
        main_controller()
    except KeyboardInterrupt:
        log("🛑 Interrupted by user, shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        log(f"🔥 Unhandled Fatal Error: {e}")
        traceback.print_exc()
        sys.exit(1)
