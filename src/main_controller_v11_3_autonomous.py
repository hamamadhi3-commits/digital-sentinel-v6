# ============================================================
# DIGITAL SENTINEL v11.3 - AUTONOMOUS MAIN CONTROLLER
# ============================================================
# Master brain of the system — orchestrates every layer:
#   1️⃣ Enumeration (Subfinder, Amass, etc.)
#   2️⃣ HTTP Probing (HTTPX)
#   3️⃣ Crawling & JS Analysis (Katana)
#   4️⃣ Vulnerability Scanning (Nuclei)
#   5️⃣ AI Prioritization (ML models)
#   6️⃣ Exploit Chain Detection
#   7️⃣ Quantum Awareness (Self-learning)
# ============================================================

import os
import time
from datetime import datetime
from sentinel_scan_engine import SentinelScanEngine
from sentinel_discord_reporter import DiscordReporter
from ai_priority import analyze_vulnerability
from chain_detector import detect_exploit_chains
from quantum_awareness_engine import QuantumAwarenessEngine


class SentinelMainController:
    def __init__(self, target_domain):
        self.target_domain = target_domain.strip()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create folders
        self.base_dir = os.path.join("data", "results", self.target_domain, self.timestamp)
        os.makedirs(self.base_dir, exist_ok=True)

        # Core modules
        self.reporter = DiscordReporter()
        self.awareness = QuantumAwarenessEngine()
        self.findings = []

    # --------------------------------------------------------
    # STEP 1–4 : Run Autonomous Scanning Pipeline
    # --------------------------------------------------------
    def run_autonomous_scan(self):
        self.reporter.send_message(
            "🚀 Sentinel Autonomous Scan Started",
            f"🎯 Target: `{self.target_domain}`\n🕒 Timestamp: `{self.timestamp}`"
        )
        engine = SentinelScanEngine(self.target_domain, output_dir=self.base_dir)
        engine.run_full_scan()
        self.reporter.send_message("🧩 Scanning Complete", "Enumeration → Vulnerability phases done.")

    # --------------------------------------------------------
    # STEP 5 : AI Prioritization / Risk Analysis
    # --------------------------------------------------------
    def analyze_results(self):
        print("[AI] Launching vulnerability prioritization engine...")
        results_file = os.path.join(self.base_dir, "vulns_latest.txt")

        if not os.path.exists(results_file):
            print("[!] No Nuclei result file found.")
            return

        with open(results_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip()]

        for line in lines:
            finding = {
                "title": line,
                "target": self.target_domain,
                "severity": "UNKNOWN",
                "description": "Auto-discovered issue"
            }
            analyzed = analyze_vulnerability(finding, self.target_domain)
            self.findings.append(analyzed)
            self.awareness.register_finding(analyzed)

        total = len(self.findings)
        print(f"[AI] {total} findings analyzed.")
        self.reporter.send_message("🤖 AI Prioritization Complete", f"Processed {total} findings.")

    # --------------------------------------------------------
    # STEP 6 : Detect Exploit Chains
    # --------------------------------------------------------
    def correlate_findings(self):
        print("[CHAIN] Running exploit-chain detection module...")
        chains = detect_exploit_chains(self.findings)

        if not chains:
            print("[CHAIN] No exploit chains found.")
            self.reporter.send_message("🔗 Exploit Chain Analysis", "No active exploit chains detected.")
            return

        msg = "\n".join(
            [f"- {c['chain_name']} (risk {c['combined_risk']})" for c in chains[:5]]
        )
        self.reporter.send_message("⚠️ Exploit Chain Alert", f"```\n{msg}\n```")

    # --------------------------------------------------------
    # STEP 7 : Awareness / Anomaly Detection
    # --------------------------------------------------------
    def awareness_feedback(self):
        anomaly = self.awareness.detect_anomalies()
        if anomaly:
            self.reporter.send_message("🧠 Quantum Awareness Alert", anomaly)

    # --------------------------------------------------------
    # FINAL REPORT GENERATION
    # --------------------------------------------------------
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

    # --------------------------------------------------------
    # FULL AUTONOMOUS CYCLE
    # --------------------------------------------------------
    def run_full_cycle(self):
        try:
            print("===================================================")
            print("🚀 Starting Digital Sentinel Quantum Cycle v11.3")
            print("===================================================\n")

            # Main pipeline
            self.run_autonomous_scan()
            self.analyze_results()
            self.correlate_findings()
            self.awareness_feedback()
            self.save_final_report()

            print("\n✅ Cycle completed successfully.")
            self.reporter.send_message(
                "✅ Sentinel Cycle Finished",
                "All modules executed successfully and data saved."
            )

        except Exception as e:
            err_msg = f"[!] FATAL ERROR in cycle: {str(e)}"
            print(err_msg)
            self.reporter.send_message("💥 Sentinel Failure", err_msg)

        finally:
            print("Cycle cleanup complete.")
            print("🕒 Waiting 30 minutes before next autonomous cycle...\n")
            time.sleep(1800)
            self.run_full_cycle()  # Restart automatically


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    target = os.getenv("TARGET_DOMAIN", "example.com")
    controller = SentinelMainController(target)
    controller.run_full_cycle()
