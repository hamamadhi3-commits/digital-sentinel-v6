# =====================================================
# Digital Sentinel v11.3 - Quantum Awareness Engine
# =====================================================
# Purpose: Self-learning intelligence layer that monitors
# patterns, detects anomalies, and auto-optimizes scanning logic.
# =====================================================

import os
import json
import numpy as np
from datetime import datetime
from collections import Counter

AWARENESS_LOG = "data/logs/quantum_awareness.log"
os.makedirs(os.path.dirname(AWARENESS_LOG), exist_ok=True)


class QuantumAwarenessEngine:
    def __init__(self):
        self.memory_file = "data/ai_memory.json"
        self.load_memory()

    # -------------------------------------------------
    # Load / save memory
    # -------------------------------------------------
    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                self.memory = json.load(f)
        else:
            self.memory = {"patterns": [], "feedback": [], "anomalies": []}

    def save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    # -------------------------------------------------
    # Register finding pattern
    # -------------------------------------------------
    def register_finding(self, finding):
        pattern = {
            "severity": finding.get("severity"),
            "cvss": finding.get("cvss"),
            "domain": finding.get("domain"),
            "time": datetime.utcnow().isoformat()
        }
        self.memory["patterns"].append(pattern)
        self.save_memory()

    # -------------------------------------------------
    # Detect anomaly or rare event
    # -------------------------------------------------
    def detect_anomalies(self):
        if len(self.memory["patterns"]) < 10:
            return None

        severities = [p["severity"] for p in self.memory["patterns"]]
        counts = Counter(severities)
        most_common = counts.most_common(1)[0][0]

        recent = self.memory["patterns"][-5:]
        recent_sev = [r["severity"] for r in recent]
        anomaly = any(s != most_common for s in recent_sev)

        if anomaly:
            msg = f"Anomaly detected: unusual severity pattern {recent_sev}"
            self.log(msg)
            self.memory["anomalies"].append(msg)
            self.save_memory()
            return msg
        return None

    # -------------------------------------------------
    # Adaptive scan tuning
    # -------------------------------------------------
    def optimize_scan_parameters(self, base_config):
        """
        Adjusts scan parallelism and depth based on previous success ratios.
        """
        total = len(self.memory["patterns"])
        critical = len([p for p in self.memory["patterns"] if p["severity"] == "CRITICAL"])
        ratio = critical / total if total else 0

        tuned_config = base_config.copy()
        if ratio > 0.3:
            tuned_config["parallel_scans"] = min(100, base_config["parallel_scans"] + 10)
            tuned_config["scan_speed_mode"] = "aggressive"
        elif ratio < 0.05:
            tuned_config["parallel_scans"] = max(10, base_config["parallel_scans"] - 5)
            tuned_config["scan_speed_mode"] = "balanced"

        self.log(f"Tuned parameters: {tuned_config}")
        return tuned_config

    # -------------------------------------------------
    # Log events
    # -------------------------------------------------
    def log(self, msg):
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with open(AWARENESS_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {msg}\n")
        print(f"[AWARENESS] {msg}")
