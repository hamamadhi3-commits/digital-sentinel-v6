# src/ai_priority_engine.py
# AI Vulnerability Prioritization Engine - Digital Sentinel v6
# STEP 5: Auto CVSS Scoring + AI Risk Interpretation

import os
import json
from transformers import pipeline

class AIPriorityEngine:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.vuln_dir = os.path.join(base_dir, "data", "results", "vulnscan")
        self.ai_summary_dir = os.path.join(base_dir, "data", "results", "ai_analysis")
        os.makedirs(self.ai_summary_dir, exist_ok=True)
        self.classifier = pipeline("zero-shot-classification",
                                   model="facebook/bart-large-mnli")

    def analyze(self, target):
        input_file = os.path.join(self.vuln_dir, f"{target}_nuclei.json")
        if not os.path.exists(input_file):
            print(f"⚠️ No vulnerability data found for {target}")
            return None

        print(f"🤖 Running AI prioritization for {target} ...")
        with open(input_file, "r", encoding="utf-8") as f:
            lines = [json.loads(l) for l in f if l.strip()]

        analyzed = []
        for entry in lines:
            title = entry.get("info", {}).get("name", "Unknown Vulnerability")
            severity_guess = entry.get("info", {}).get("severity", "medium")
            host = entry.get("host", "")
            context = f"Vulnerability {title} with severity {severity_guess} at {host}"

            labels = ["critical", "high", "medium", "low"]
            result = self.classifier(context, labels)
            ai_severity = result["labels"][0].upper()

            analyzed.append({
                "title": title,
                "url": host,
                "ai_severity": ai_severity,
                "confidence": float(result["scores"][0])
            })

        output_file = os.path.join(self.ai_summary_dir, f"{target}_ai.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(analyzed, f, indent=2)

        print(f"✅ AI prioritization complete for {target}")
        return analyzed
