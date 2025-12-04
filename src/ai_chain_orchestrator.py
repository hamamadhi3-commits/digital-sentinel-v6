# ---------------------------------------------------------
# Digital Sentinel v11.2 — AI Chain Orchestrator
# Purpose: Coordinate multi-agent AI awareness and
# manage dynamic workflow restarts + adaptive learning
# ---------------------------------------------------------

import os
import time
import json
import random
import traceback
import threading
from datetime import datetime

# Local imports (all engines and quantum layer)
from quantum_awareness_engine import QuantumAwarenessEngine
from ai_priority import analyze_vulnerability
from chain_detector import detect_exploit_chains
from sentinel_discord_reporter import send_chain_report, send_finding_report

# =========================================================
#  CONFIGURATION
# =========================================================

DATA_PATH = "data/"
RESULT_PATH = os.path.join(DATA_PATH, "results")
REPORT_PATH = os.path.join(DATA_PATH, "reports")
LOG_PATH = os.path.join(DATA_PATH, "logs")
os.makedirs(RESULT_PATH, exist_ok=True)
os.makedirs(REPORT_PATH, exist_ok=True)
os.makedirs(LOG_PATH, exist_ok=True)

AI_CHAIN_LOG = os.path.join(LOG_PATH, f"ai_chain_{int(time.time())}.log")


# =========================================================
#  LOGGING SYSTEM
# =========================================================

def log(msg):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[🧠 AI-CHAIN {timestamp}] {msg}"
    print(line)
    with open(AI_CHAIN_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# =========================================================
#  AI CHAIN ORCHESTRATOR CLASS
# =========================================================

class AIChainOrchestrator:
    def __init__(self, quantum_agents=10, scan_interval=1800):
        self.quantum_agents = quantum_agents
        self.scan_interval = scan_interval  # 30 minutes default
        self.last_cycle = None
        self.cycle_count = 0
        self.findings = []
        self.is_running = False

    # -----------------------------------------------
    # Run the full chain cycle
    # -----------------------------------------------
    def run_cycle(self):
        self.cycle_count += 1
        self.last_cycle = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        log(f"🚀 Starting AI Chain Cycle #{self.cycle_count}")

        try:
            # STEP 1: Launch Quantum Awareness
            log("🌌 Initiating Quantum Awareness Engine...")
            quantum = QuantumAwarenessEngine(max_agents=self.quantum_agents)
            quantum.run_quantum_cycle()
            self.findings = quantum.results

            # STEP 2: AI Analysis + Classification
            log("🧩 Running AI vulnerability classification...")
            enhanced = []
            for f in self.findings:
                if isinstance(f, dict):
                    enhanced.append(analyze_vulnerability(f, f.get("target", "unknown")))
            self.findings = enhanced

            # STEP 3: Chain Detection
            log("🔗 Detecting exploit-chains among findings...")
            chains = detect_exploit_chains(self.findings)
            if chains:
                log(f"🔥 {len(chains)} exploit chains detected.")
                for c in chains:
                    send_chain_report(c)
            else:
                log("✅ No exploit-chains detected this round.")

            # STEP 4: Report Prioritized Findings
            for f in self.findings:
                if f.get("cvss", 0) >= 5:
                    send_finding_report(f)

            # STEP 5: Save Report
            self._save_cycle_report()

        except Exception as e:
            log(f"❌ AI Chain Cycle Error: {e}")
            traceback.print_exc()

        log(f"✅ Cycle #{self.cycle_count} completed successfully.")
        self._sleep_and_restart()

    # -----------------------------------------------
    # Save results of this chain cycle
    # -----------------------------------------------
    def _save_cycle_report(self):
        report_file = os.path.join(REPORT_PATH, f"chain_cycle_{self.cycle_count}.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.findings, f, indent=2)
        log(f"📄 Report saved to {report_file}")

    # -----------------------------------------------
    # Sleep and restart automatically
    # -----------------------------------------------
    def _sleep_and_restart(self):
        log(f"⏳ Sleeping {self.scan_interval / 60} minutes before next cycle...")
        time.sleep(self.scan_interval)
        log("♻️ Restarting AI Chain Cycle...")
        self.run_cycle()

    # -----------------------------------------------
    # Launch orchestrator (non-blocking)
    # -----------------------------------------------
    def start(self):
        if not self.is_running:
            self.is_running = True
            t = threading.Thread(target=self.run_cycle)
            t.start()
            log("🧠 AI Chain Orchestrator launched in background thread.")
        else:
            log("⚠️ AI Chain already running.")


# =========================================================
#  ENTRYPOINT
# =========================================================

if __name__ == "__main__":
    orchestrator = AIChainOrchestrator(quantum_agents=10, scan_interval=1800)
    orchestrator.start()
