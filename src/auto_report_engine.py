# src/auto_report_engine.py
# Digital Sentinel v6 — STEP 6: Autonomous Reporting Engine

import os
import json
import time
from datetime import datetime
import requests

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "").strip()

class AutoReportEngine:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.ai_dir = os.path.join(base_dir, "data", "results", "ai_analysis")
        self.report_dir = os.path.join(base_dir, "data", "reports")
        os.makedirs(self.report_dir, exist_ok=True)

    def generate_summary(self):
        print("🧩 Building AI Summary Report...")
        report = {"critical": [], "high": [], "medium": []}

        for file in os.listdir(self.ai_dir):
            if not file.endswith("_ai.json"):
                continue

            with open(os.path.join(self.ai_dir, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                for finding in data:
                    sev = finding["ai_severity"].lower()
                    if sev in report:
                        report[sev].append(finding)

        total = sum(len(v) for v in report.values())
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

        summary_file = os.path.join(self.report_dir, f"summary_{int(time.time())}.json")
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"✅ Report built: {summary_file}")
        return total, report, now

    def send_to_discord(self):
        if not DISCORD_WEBHOOK:
            print("⚠️ Discord webhook not set!")
            return

        total, report, now = self.generate_summary()

        msg = (
            f"🧠 **Digital Sentinel Autonomous Summary** ({now})\n"
            f"📊 Total Findings: **{total}**\n\n"
            f"🚨 Critical: {len(report['critical'])}\n"
            f"🔥 High: {len(report['high'])}\n"
            f"⚠️ Medium: {len(report['medium'])}\n\n"
            "📤 Auto-report generated successfully!"
        )

        try:
            requests.post(DISCORD_WEBHOOK, json={"content": msg})
            print("📨 Report sent to Discord.")
        except Exception as e:
            print(f"❌ Failed to send Discord report: {e}")
