# =====================================================
# Digital Sentinel v11.3 — MAIN CONTROLLER (Self-Healing)
# Autonomous Vulnerability Hunter + AI Prioritization + Chain Recovery
# =====================================================

import os
import time
import json
import traceback
from datetime import datetime

from ai_priority import analyze_vulnerability
from chain_detector import detect_exploit_chains
from sentinel_discord_reporter import send_chain_report, send_finding_report
from sentinel_scan_engine import run_full_scan

# =====================================================
# CONFIGURATION
# =====================================================

TARGET_FILE = "data/targets/global_500_targets.txt"
RESULT_DIR = "data/results"
LOG_DIR = "data/logs"
RECOVERY_LOG = os.path.join(LOG_DIR, "recovery.log")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

MAIN_LOG = os.path.join(LOG_DIR, f"controller_{int(time.time())}.log")

# =====================================================
# LOGGING SYSTEM
# =====================================================

def log(msg: str, show=True):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    if show:
        print(line)
    with open(MAIN_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# =====================================================
# TARGET LOADER
# =====================================================

def load_targets():
    if not os.path.exists(TARGET_FILE):
        log("❌ Target file not found!")
        return []
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        domains = [line.strip() for line in f if line.strip()]
    return domains


# =====================================================
# RESULT HANDLER
# =====================================================

def save_result(domain, findings):
    outf = os.path.join(RESULT_DIR, f"{domain}_findings.json")
    with open(outf, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2)
    log(f"📁 Saved results for {domain}")


# =====================================================
# SELF-HEALING CONTROLLER
# =====================================================

def main_controller():
    log("🚀 Starting Digital Sentinel v11.3 — Autonomous Recovery Mode")

    retry_count = 0
    max_retries = 3
    cooldown_time = 300  # seconds (5 min)
    success_cycles = 0

    while True:
        try:
            log(f"🧭 Initiating new scan cycle | Success cycles: {success_cycles} | Retries: {retry_count}")

            targets = load_targets()
            if not targets:
                log("⚠️ No targets found, sleeping 10 minutes...")
                time.sleep(600)
                continue

            all_findings = []

            # STEP 1 — Scan All Targets
            for domain in targets:
                log(f"🟦 Scanning Target → {domain}")
                results = run_full_scan(domain)

                if not results:
                    log(f"⚠️ No findings for {domain}")
                    continue

                # STEP 2 — AI Priority Analysis
                enhanced = []
                for f in results:
                    try:
                        enhanced.append(analyze_vulnerability(f, domain))
                    except Exception as e:
                        log(f"❌ AI Analysis Error for {domain}: {e}")

                save_result(domain, enhanced)
                all_findings.extend(enhanced)

                # STEP 3 — Send High Severity Findings
                for f in enhanced:
                    sev = f.get("severity", "LOW").upper()
                    if sev in ["CRITICAL", "HIGH", "MEDIUM"]:
                        send_finding_report(f)

            # STEP 4 — Detect Exploit Chains
            log("🔍 Checking for exploit chains across all targets...")
            chains = detect_exploit_chains(all_findings)

            if chains:
                log(f"🔥 {len(chains)} Exploit Chains Found.")
                for ch in chains:
                    send_chain_report(ch)
            else:
                log("ℹ️ No exploit chains found this round.")

            # STEP 5 — Success Loop Management
            success_cycles += 1
            retry_count = 0
            log(f"✅ Cycle {success_cycles} completed successfully.")
            log("⏳ Sleeping 30 minutes before next cycle...")
            time.sleep(1800)

        except Exception as e:
            retry_count += 1
            log(f"❌ FATAL Controller Error: {e}")
            traceback.print_exc()

            # Write to recovery log
            with open(RECOVERY_LOG, "a", encoding="utf-8") as f:
                f.write(f"{datetime.utcnow()} — Cycle failure #{retry_count}: {e}\n")

            if retry_count < max_retries:
                log(f"♻️ Attempting recovery... Cooling {cooldown_time // 60} minutes.")
                time.sleep(cooldown_time)
                continue
            else:
                log("💀 MAX RETRIES REACHED — System entering deep cooldown mode.")
                with open(RECOVERY_LOG, "a", encoding="utf-8") as f:
                    f.write(f"{datetime.utcnow()} — SYSTEM STOP AFTER MAX RETRIES.\n")
                time.sleep(3600)
                retry_count = 0  # reset after long cooldown


# =====================================================
# ENTRYPOINT
# =====================================================

if __name__ == "__main__":
    main_controller()
