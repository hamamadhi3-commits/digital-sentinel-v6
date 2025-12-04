# ---------------------------------------------------------
# Digital Sentinel Quantum Awareness Engine
# Multi-Agent Autonomous Coordination Layer
# ---------------------------------------------------------

import os
import time
import random
import threading
import traceback

# Fix import path (so Python finds local engines/)
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "engines"))

# Now import local modules
from enumeration_engine import EnumerationEngine
from passive_intel_engine import PassiveIntelEngine
from active_intel_engine import ActiveIntelEngine


# =========================================================
#  Quantum Awareness Engine
# =========================================================

class QuantumAwarenessEngine:
    def __init__(self, max_agents=10):
        """
        Initializes the quantum engine that runs parallel agents
        for enumeration, passive intel, and active recon simultaneously.
        """
        self.max_agents = max_agents
        self.agents = []
        self.results = []
        self.running = False

    def log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        print(f"[🌌 QuantumEngine {timestamp}] {message}")

    def _agent_task(self, agent_id, target):
        """
        Executes a single agent task cycle.
        """
        try:
            self.log(f"🧠 Agent {agent_id} started on target {target}")

            # === Step 1: Enumeration Phase ===
            enum_engine = EnumerationEngine()
            subdomains = enum_engine.enumerate(target)
            self.log(f"🔹 Agent {agent_id}: Found {len(subdomains)} subdomains.")

            # === Step 2: Passive Intelligence Phase ===
            passive_engine = PassiveIntelEngine()
            passive_data = passive_engine.run(target)
            self.log(f"🔸 Agent {agent_id}: Passive intel collected.")

            # === Step 3: Active Recon Phase ===
            active_engine = ActiveIntelEngine()
            recon_data = active_engine.run(target)
            self.log(f"🚀 Agent {agent_id}: Active recon done.")

            self.results.append({
                "agent_id": agent_id,
                "target": target,
                "subdomains": subdomains,
                "passive": passive_data,
                "active": recon_data
            })

        except Exception as e:
            self.log(f"⚠️ Agent {agent_id} failed: {e}")
            traceback.print_exc()

    # =========================================================
    #  Quantum Coordination Core
    # =========================================================

    def run_quantum_cycle(self):
        """
        Starts a multi-threaded awareness cycle with autonomous AI agents.
        """
        self.running = True
        self.log(f"⚙️ Launching {self.max_agents} Quantum Agents...")

        # Example target rotation for awareness
        default_targets = [
            "example.com",
            "tesla.com",
            "apple.com",
            "google.com",
            "microsoft.com"
        ]

        for i in range(self.max_agents):
            target = random.choice(default_targets)
            t = threading.Thread(target=self._agent_task, args=(i + 1, target))
            self.agents.append(t)
            t.start()
            time.sleep(0.5)  # Slight staggering to avoid overload

        # Wait for all agents
        for t in self.agents:
            t.join()

        self.log("✅ All Quantum Agents completed their cycles.")
        self._summarize_results()

    # =========================================================
    #  Result Summary
    # =========================================================

    def _summarize_results(self):
        """
        Prints and saves a summary of results from all agents.
        """
        summary_path = "data/reports/quantum_summary.txt"
        os.makedirs(os.path.dirname(summary_path), exist_ok=True)

        self.log("📊 Compiling Quantum Summary Report...")
        with open(summary_path, "w", encoding="utf-8") as f:
            for result in self.results:
                f.write(f"Agent {result['agent_id']} → {result['target']}\n")
                f.write(f"  Subdomains found: {len(result['subdomains'])}\n")
                f.write(f"  Passive intel keys: {list(result['passive'].keys()) if isinstance(result['passive'], dict) else 'N/A'}\n")
                f.write(f"  Active ports: {result['active'].get('ports', []) if isinstance(result['active'], dict) else 'N/A'}\n")
                f.write("-" * 60 + "\n")

        self.log(f"📄 Quantum summary saved to {summary_path}")
