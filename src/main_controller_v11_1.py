# ---------------------------------------------------------
# Digital Sentinel v11.1 — MAIN CONTROLLER
# Autonomous Vulnerability Hunter + AI Prioritization + Chains
# ---------------------------------------------------------

import os
import time
import json
import traceback
from datetime import datetime

# === Imports for AI Modules ===
from ai_priority import analyze_vulnerability
from chain_detector import detect_exploit_chains
from sentinel_discord_reporter import send_chain_report, send_finding_report
from sentinel_scan_engine import run_full_scan
from quantum_awareness_engine import QuantumAwarenessEngine  # ⬅️ Added for STEP 10 integration


# ===========================
#  CONFIGURATION
# ===========================

TARGET_FILE = "data/targets/global_500_targets.txt"
RESULT_DIR = "data/results"
LOG_DIR = "data/logs"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

MAIN_LOG = os.path.join(LOG_DIR, f"controller_{int(time.time())}.log")


# ===========================
#  LOGGING SYSTEM
# ===========================

def log(msg):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(MAIN_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ===========================
#  LOAD TARGETS
# ===========================

def load_targets():
    if not os.path.exists(TARGET_FILE):
        log("❌ Target file not found!")
        return []

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        domains = [l.strip() for l in f if l.strip()]

    return domains


# ===========================
#  SAVE FINDINGS
# ===========================

def save_result(domain, findings):
    outf = os.path.join(RESULT_DIR, f"{domain}_findings.json")
    with open(outf, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2)
    log(f"📁 Saved results for {domain}")


# ===========================
#  MAIN CONTROLLER
# ===========================

def main_controller():
    log("🚀 Starting Digital Sentinel v11.1 (Autonomous Mode)")

    while True:
        try:
            # ------------------------------------------
            # STEP 1 — Load targets
            # ------------------------------------------
            targets = load_targets()
            log(f"🎯 Loaded {len(targets)} targets.")

            if not targets:
                log("⚠️ No targets found. Sleeping 10 minutes...")
                time.sleep(600)
                continue

            # ------------------------------------------
            # STEP 2 — Loop through each domain
            # ------------------------------------------
            all_findings = []

            for domain in targets:
                log(f"🟦 Processing target → {domain}")

                # Run Scan
                results = run_full_scan(domain)

                if not results:
                    log(f"⚠️ No findings for {domain}")
                    continue

                # ------------------------------------------
                # STEP 3 — AI PRIORITY ENGINE (قۆناغ ٨)
                # ------------------------------------------
                enhanced = []
                for f in results:
                    enhanced.append(analyze_vulnerability(f, domain))

                save_result(domain, enhanced)
                all_findings.extend(enhanced)

                # ------------------------------------------
                # STEP 4 — SEND SINGLE FINDING REPORTS
                # Only CRITICAL / HIGH / MEDIUM
                # ------------------------------------------
                for f in enhanced:
                    if f.get("cvss", 0) >= 5:  # MEDIUM+
                        send_finding_report(f)

            # --------------------------------------------------
            # STEP 5 — CHAIN DETECTION ENGINE (قۆناغ ٩)
            # --------------------------------------------------
            log("🔍 Checking for exploit-chains...")

            chains = detect_exploit_chains(all_findings)

            if chains:
                log(f"🔥 {len(chains)} exploit chains detected.")
                for ch in chains:
                    send_chain_report(ch)
            else:
                log("ℹ️ No exploit chains found this round.")

            # --------------------------------------------------
            # STEP 6 — QUANTUM AWARENESS MODE (قۆناغ ١٠)
            # --------------------------------------------------
            log("🌌 Activating Quantum Awareness Mode...")
            try:
                quantum = QuantumAwarenessEngine(max_agents=10)
                quantum.run_quantum_cycle()
            except Exception as qe:
                log(f"⚠️ Quantum Awareness Engine Error: {qe}")

            # --------------------------------------------------
            # STEP 7 — AUTONOMOUS LOOP
            # --------------------------------------------------
            log("⏳ Sleeping 30 minutes before next cycle...")
            time.sleep(1800)

        except Exception as e:
            log(f"❌ Fatal Controller Error: {e}")
            traceback.print_exc()

            log("♻️ Restarting Controller in 60 seconds...")
            time.sleep(60)


# ===========================
#  ENTRYPOINT
# ===========================

if __name__ == "__main__":
    main_controller()
