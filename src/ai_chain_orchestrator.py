# src/ai_chain_orchestrator.py
# Digital Sentinel v6 — STEP 9: AI Chain Orchestrator

import os
import time
from datetime import datetime

from engines.enumeration_engine import EnumerationEngine
from engines.active_intel_engine import ActiveIntelEngine
from engines.passive_intel_engine import PassiveIntelEngine
from engines.threat_intel_engine import ThreatIntelEngine
from engines.self_evolution_engine import SelfEvolutionEngine
from engines.auto_report_engine import AutoReportEngine

class AIChainOrchestrator:
    def __init__(self):
        self.log_file = os.path.join("data/logs", f"orchestrator_{int(time.time())}.log")
        os.makedirs("data/logs", exist_ok=True)
        self.cycles_completed = 0

    def log(self, msg):
        line = f"[{datetime.utcnow()}] {msg}"
        print(line)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def start_cycle(self):
        self.log("🚀 Initiating full intelligence cycle...")

        try:
            # === Phase 1: Enumeration ===
            self.log("🧩 Phase 1: Subdomain Enumeration")
            enum = EnumerationEngine()
            targets = enum.run_enumeration()
            self.log(f"✅ Enumeration complete ({len(targets)} targets).")

            # === Phase 2: Passive Intel ===
            self.log("🌐 Phase 2: Passive Reconnaissance")
            passive = PassiveIntelEngine()
            passive_results = passive.run_passive_scan(targets)
            self.log("✅ Passive intel collected.")

            # === Phase 3: Active Intel ===
            self.log("⚙️ Phase 3: Active Intelligence Gathering")
            active = ActiveIntelEngine()
            active_results = active.run_active_scan(passive_results)
            self.log("✅ Active intelligence complete.")

            # === Phase 4: Threat Fusion ===
            self.log("🛰 Phase 4: Threat Intelligence Fusion")
            intel = ThreatIntelEngine()
            intel.fuse_intelligence()
            self.log("✅ Threat feeds synchronized.")

            # === Phase 5: AI Analysis ===
            self.log("🤖 Phase 5: AI Analysis")
            os.system("python src/ai_priority.py")
            self.log("✅ AI vulnerability analysis finished.")

            # === Phase 6: Reporting ===
            self.log("📤 Phase 6: Auto Reporting")
            report = AutoReportEngine()
            report.send_to_discord()

            # === Phase 7: Self-Evolution ===
            self.log("🧬 Phase 7: Self Evolution")
            evolution = SelfEvolutionEngine()
            decision = evolution.evolve()

            # === Adaptive Restart ===
            self.cycles_completed += 1
            self.log(f"♻️ Cycle {self.cycles_completed} completed — Decision: {decision}")
            self.log("⏳ Sleeping 3 hours before next autonomous cycle...")
            time.sleep(10800)

            # Restart automatically
            self.start_cycle()

        except Exception as e:
            self.log(f"❌ Orchestrator Error: {e}")
            self.log("⚡ Restarting in 2 minutes...")
            time.sleep(120)
            self.start_cycle()
