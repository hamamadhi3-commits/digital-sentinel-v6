import os
import json
import asyncio
from datetime import datetime
from src.recon_engine_parallel import run_recon_parallel
from src.scope_fetcher import fetch_targets
from src.ai_vuln_detector import analyze_vulnerabilities
from src.auto_report_compose import compose_report
from src.discord_notify import send_discord_notification
from src.duplication_checker import remove_duplicates

CONFIG_PATH = "data/config.json"

async def main():
    # === Load Configuration ===
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    threads = config.get("threads", 4)
    target_file = config.get("target_file", "data/targets/global_500_targets.txt")
    report_dir = config.get("report_directory", "data/reports")
    log_dir = config.get("log_directory", "data/logs")

    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    # === Step 1: Fetch targets ===
    print("[1] Fetching and cleaning target list...")
    targets = fetch_targets(target_file)
    targets = remove_duplicates(targets)
    print(f"[+] Loaded {len(targets)} unique targets")

    # === Step 2: Recon Parallel Scan ===
    print(f"[2] Launching Parallel Recon Engine with {threads} threads...")
    recon_results = await run_recon_parallel(targets, threads)

    # === Step 3: AI Vulnerability Analysis ===
    print("[3] Analyzing potential vulnerabilities using AI module...")
    ai_results = analyze_vulnerabilities(recon_results)

    # === Step 4: Auto Compose Reports ===
    print("[4] Generating autonomous reports...")
    report_path = compose_report(ai_results, report_dir)

    # === Step 5: Discord Notification ===
    print("[5] Sending completion notification...")
    msg = f"✅ Sentinel Autonomous v6.1 completed.\n🕓 {datetime.now()}\n📄 Report: {report_path}"
    send_discord_notification(msg)

    print("[✔] All systems completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
