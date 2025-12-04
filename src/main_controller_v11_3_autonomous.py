# =====================================================
# DIGITAL SENTINEL v11.3 - AUTONOMOUS MAIN CONTROLLER
# =====================================================
# Core control module for the Sentinel Quantum Autonomous Cycle
# Layers:
# 1️⃣ Enumeration  (Subfinder / Amass / Assetfinder)
# 2️⃣ HTTP Probing (HTTPX)
# 3️⃣ Crawler & JS Parser (Katana)
# 4️⃣ Vulnerability Scanner (Nuclei)
# 5️⃣ AI Analysis Layer (Python models for classification)
# 6️⃣ Autonomous Cycle (Cron + Watchdog + Discord Alerts)
# =====================================================

import os
import time
from datetime import datetime

# Local modules
from sentinel_scan_engine import SentinelScanEngine
from sentinel_discord_reporter import DiscordReporter
from ai_priority import analyze_vulnerability
from chain_detector import detect_exploit_chains


class SentinelMainController:
    def __init__(self, target_domain):
        self.target_domain = target_domain
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = os.path.join("data", "results", self.target_domain, self.timestamp)
        os.makedirs(self.base_dir, exist_ok=True)

        self.reporter = DiscordReporter()
        self.findings = []

    # -------------------------------------------------
    # STEP 1–4 : Run scan engine (enumeration → nuclei)
    # -------------------------------------------------
    def run_autonomous_scan(self):
        self.reporter.send_message(
            "🚀 Sentinel Cycle Started",
            f"Target: `{self.target_domain}` • Timestamp: `{self.timestamp}`"
        )
        engine = SentinelScanEngine(self.target_domain, output_dir=self.base_dir)
        engine.run_full_scan()
        self.reporter.send_message("🧩 Scan Engine Completed", "Enumeration → Vulnerability phases done.")

    # -------------------------------------------------
    # STEP 5 : AI analysis + prioritization
    # -------------------------------------------------
    def analyze_results(self):
        print("[AI] Analyzing vulnerabilities with ML models...")
        results_file = os.path.join(self.base_dir, "vulns_latest.txt")
        if not os.path.exists(results_file):
            print("[!] No Nuclei results found.")
            return

        with open(results_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        for line in lines:
            if not line.strip():
                continue
            vuln_data = {"title": line.strip(), "description": "Auto-discovered issue"}
            analyzed = analyze_vulnerability(vuln_data, self.target_domain)
            self.findings.append(analyzed)

        print(f"[AI] {len(self.findings)} findings processed.")
        self.reporter.send_message("🤖 AI Analysis Complete", f"Processed {len(self.findings)} vulnerabilities.")

    # -------------------------------------------------
    # STEP 6 : Correlate exploit chains
    # -------------------------------------------------
    def correlate_findings(self):
        print("[CHAIN] Detecting possible exploit chains...")
        chains = detect_exploit_chains(self.findings)
        if not chains:
            print("[CHAIN] No exploit chains detected.")
            self.reporter.send_message("🔗 Exploit Chain Analysis", "No critical links found.")
            return

        summary = "\n".join([f"- {c['chain_name']} (risk {c['combined_risk']})" for c in chains[:5]])
        self.reporter.send_message("⚠️ Exploit Chain Detected", f"```\n{summary}\n```")

    # -------------------------------------------------
    # Save final report
    # -------------------------------------------------
    def save_final_report(self):
        report_path = os.path.join(self.base_dir, "final_report.txt")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=== DIGITAL SENTINEL FINAL REPORT ===\n")
            f.write(f"Target: {self.target_domain}\n")
            f.write(f"Timestamp: {self.timestamp}\n")
            f.write(f"Total Findings: {len(self.findings)}\n\n")

            for item in self.findings:
                f.write(f"- {item['title']} [{item['severity']}] CVSS {item['cvss']}\n")
                f.write(f"  → {item['ai_analysis']}\n\n")

        print(f"[+] Final report saved → {report_path}")
        self.reporter.send_report_summary(report_path)

    # -------------------------------------------------
    # Full autonomous cycle
    # -------------------------------------------------
    def run_full_cycle(self):
        try:
            print("===============================================")
            print("🚀 Starting Sentinel Quantum Autonomous Cycle v11.3")
            print("===============================================")

            self.run_autonomous_scan()
            self.analyze_results()
            self.correlate_findings()
            self.save_final_report()

            print("✅ Cycle completed successfully.")
            self.reporter.send_message("✅ Sentinel Cycle Finished", "All modules executed successfully.")
        except Exception as e:
            err_msg = f"[!] Cycle crashed: {str(e)}"
            print(err_msg)
            self.reporter.send_message("💥 Sentinel Failure", err_msg)
        finally:
            print("Cycle cleanup complete.")


# =====================================================
# Entry point
# =====================================================
if __name__ == "__main__":
    target = os.getenv("TARGET_DOMAIN", "example.com")
    controller = SentinelMainController(target)
    controller.run_full_cycle()
