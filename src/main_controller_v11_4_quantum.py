# src/main_controller_v11_4_quantum.py
"""
Digital Sentinel - Quantum Autonomous Controller v11.4
-------------------------------------------------------
Main orchestrator for the Digital Sentinel engine.

Responsibilities:
1. Load target list from /data/targets.txt
2. Dispatch enumeration, probing, crawling, scanning
3. Integrate AI analysis and autonomous cycle
4. Send results to Discord using sentinel_discord_reporter_v2.py
5. Prevent duplicate reports
"""

import os
import json
import time
import random
import traceback
from datetime import datetime

from enumeration_engine import run_enumeration
from probing_engine import run_probing
from crawler_engine import run_crawler
from vulnerability_scanner import run_scanner
from ai_analyzer import run_ai_analysis
from sentinel_discord_reporter_v2 import send_finding_report


# --------------------------------------------------------
# Utility and log functions
# --------------------------------------------------------

def log(msg):
    timestamp = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {msg}")


def save_report(target, findings, folder="data/reports"):
    """Save the full findings to a JSON file"""
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{target}_{int(time.time())}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2)
    return filename


# --------------------------------------------------------
# Duplicate Checker
# --------------------------------------------------------

def is_duplicate(finding, history_dir="data/reports"):
    """Check if this vulnerability was already reported before"""
    import glob
    sig = (finding.get("target", ""), finding.get("category", ""), finding.get("url", ""))
    for file in glob.glob(os.path.join(history_dir, "*.json")):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for old in data:
                    if (
                        old.get("target") == sig[0]
                        and old.get("category") == sig[1]
                        and old.get("url") == sig[2]
                    ):
                        return True
        except:
            continue
    return False


# --------------------------------------------------------
# Core processing pipeline
# --------------------------------------------------------

def process_target(target):
    """Run the full Sentinel process on a single target"""
    log(f"🚀 Starting scan for {target}")

    try:
        # 1️⃣ Subdomain Enumeration
        subdomains = run_enumeration(target)
        log(f"🔍 Found {len(subdomains)} subdomains for {target}")

        # 2️⃣ HTTP Probing
        alive_hosts = run_probing(subdomains)
        log(f"🌐 {len(alive_hosts)} active hosts after probing.")

        # 3️⃣ Crawling & JS Parsing
        urls = run_crawler(alive_hosts)
        log(f"🕷️ Crawled {len(urls)} URLs/endpoints.")

        # 4️⃣ Vulnerability Scanning
        findings = run_scanner(urls)
        log(f"💣 {len(findings)} potential vulnerabilities found.")

        # 5️⃣ AI Analysis & Prioritization
        analyzed = run_ai_analysis(findings)
        log(f"🧠 AI classified and prioritized {len(analyzed)} findings.")

        # 6️⃣ Duplicate check + Discord Reporting
        new_reports = []
        for f in analyzed:
            if is_duplicate(f):
                log(f"⚠️ Duplicate finding detected for {f.get('target')} → skipped.")
                continue
            send_finding_report(f)
            new_reports.append(f)

        # 7️⃣ Save report file
        save_path = save_report(target, new_reports)
        log(f"📁 Report saved: {save_path}")

        log(f"✅ Scan completed for {target}")

    except Exception as e:
        log(f"❌ Fatal error during processing {target}: {e}")
        traceback.print_exc()


# --------------------------------------------------------
# Autonomous cycle controller
# --------------------------------------------------------

def main():
    """Main loop — iterate over all targets from data/targets.txt"""
    log("🧠 Digital Sentinel Quantum Controller v11.4 initialized.")
    targets_file = "data/targets.txt"

    if not os.path.exists(targets_file):
        log("❌ No target file found.")
        return

    with open(targets_file, "r", encoding="utf-8") as f:
        targets = [t.strip() for t in f.readlines() if t.strip()]

    log(f"🎯 Loaded {len(targets)} targets for scanning.")

    for target in targets:
        process_target(target)
        # Random delay between cycles to mimic human behavior
        time.sleep(random.uniform(5, 15))

    log("🕒 Autonomous cycle finished. Waiting for next cron trigger.")


if __name__ == "__main__":
    main()
