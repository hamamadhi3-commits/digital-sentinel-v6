# src/self_evolution_engine.py
# Digital Sentinel v6 — STEP 7: Self Evolution & Adaptive Learning Engine

import os
import json
import random
from datetime import datetime

class SelfEvolutionEngine:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.ai_dir = os.path.join(base_dir, "data", "results", "ai_analysis")
        self.evolution_log = os.path.join(base_dir, "data", "logs", "evolution_history.log")

    def evolve(self):
        print("🧬 Initiating Self-Evolution Cycle...")

        # Load AI analysis results
        data_points = []
        for file in os.listdir(self.ai_dir):
            if not file.endswith("_ai.json"):
                continue
            with open(os.path.join(self.ai_dir, file), "r", encoding="utf-8") as f:
                data_points.extend(json.load(f))

        if not data_points:
            print("⚠️ No AI analysis data found. Skipping evolution.")
            return

        # Simulate a "learning" feedback process
        stats = {"critical": 0, "high": 0, "medium": 0}
        for f in data_points:
            sev = f["ai_severity"].lower()
            if sev in stats:
                stats[sev] += 1

        # Adaptive learning decision
        decision = ""
        if stats["critical"] >= 10:
            decision = "Increase scanning intensity and depth."
        elif stats["high"] >= 10:
            decision = "Maintain current speed, focus on critical hosts."
        elif stats["medium"] > 15:
            decision = "Enable deeper JS parsing and passive recon."
        else:
            decision = "Reduce load, optimize resource balance."

        # Log the adaptive decision
        line = f"[{datetime.utcnow()}] Evolved Decision: {decision}\n"
        with open(self.evolution_log, "a", encoding="utf-8") as f:
            f.write(line)

        print(f"🤖 Evolution Decision: {decision}")
        print("✅ Self-Evolution Cycle Completed.")

        return decision
