#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Digital Sentinel v11.1 — Eternal Hunter Engine
Autonomous vulnerability hunter: discovers, mutates, and re-scans targets continuously.
"""

import os
import random
import time
import json
import requests
from datetime import datetime

# ===== CONFIGURATION ===== #
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
TARGET_FILE = "data/targets/global_500_targets.txt"
REPORT_DIR = "data/reports"
LOG_DIR = "data/logs"

SCAN_DELAY = 2  # seconds between scans
MUTATION_RATE = 0.15  # probability of evolving search patterns
CYCLE_LIMIT = 100  # number of scan loops before soft reboot

# ===== SETUP ===== #
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
print("🚀 Eternal Hunter Engine started...")

# ===== HELPERS ===== #
def log(msg):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(os.path.join(LOG_DIR, "eternal_hunter.log"), "a", encoding="utf-8") as lf:
        lf.write(line + "\n")

def send_discord(msg, color=0x00ffcc):
    """Send embed to Discord"""
    if not DISCORD_WEBHOOK:
        log("⚠️ No DISCORD_WEBHOOK configured.")
        return
    payload = {
        "username": "Eternal Hunter",
        "embeds": [
            {
                "title": "⚡ Digital Sentinel Eternal Hunter",
                "description": msg,
                "color": color,
                "footer": {
                    "text": f"v11.1 • {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
                },
            }
        ],
    }
    try:
        requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
    except Exception as e:
        log(f"❌ Discord send failed: {e}")

def load_targets():
    """Load all targets from file"""
    if not os.path.exists(TARGET_FILE):
        log("❌ Target list missing!")
        return []
    with open(TARGET_FILE, "r", encoding="utf-8") as tf:
        return [line.strip() for line in tf if line.strip()]

def mutate_target(target):
    """Generate mutated scanning vector (simulate new recon patterns)"""
    patterns = ["admin", "login", "dev", "beta", "staging", "api", "dashboard"]
    if random.random() < MUTATION_RATE:
        mutation = random.choice(patterns)
        return f"{mutation}.{target}"
    return target

def simulate_scan(target):
    """Simulated vulnerability scanning engine"""
    time.sleep(random.uniform(0.8, 1.5))
    severity = random.choices(["LOW", "MEDIUM", "HIGH", "CRITICAL"], weights=[40, 30, 20, 10])[0]
    found = random.random() < 0.35  # 35% chance of finding something
    if found:
        vuln = f"{target} → Potential {severity} vulnerability"
        log(f"🧩 Found: {vuln}")
        return {"target": target, "severity": severity, "vuln": vuln}
    else:
        log(f"✅ No findings on {target}")
        return None

# ===== MAIN ENGINE ===== #
def main():
    cycle = 0
    all_findings = []

    targets = load_targets()
    total_targets = len(targets)
    if total_targets == 0:
        send_discord("⚠️ No targets found for Eternal Hunter.")
        return

    log(f"🎯 Loaded {total_targets} targets for eternal scanning.")

    while cycle < CYCLE_LIMIT:
        cycle += 1
        log(f"\n🌀 Cycle #{cycle} starting...")
        findings = []

        for idx, target in enumerate(targets, 1):
            mutated = mutate_target(target)
            result = simulate_scan(mutated)
            if result:
                findings.append(result)
                all_findings.append(result)

        # save intermediate report
        report_path = os.path.join(REPORT_DIR, f"cycle_{cycle}_report.json")
        with open(report_path, "w", encoding="utf-8") as rf:
            json.dump(findings, rf, indent=2)
        log(f"🗂️ Saved report: {report_path}")

        # send summary to Discord
        summary = (
            f"Cycle {cycle} complete.\n"
            f"Findings: {len(findings)} / {total_targets}\n"
            f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )
        color = 0x1e90ff if findings else 0x888888
        send_discord(summary, color=color)

        # cooldown before next scan loop
        time.sleep(SCAN_DELAY)

    # === FINAL SUMMARY === #
    total_findings = len(all_findings)
    criticals = [f for f in all_findings if f["severity"] == "CRITICAL"]
    summary_msg = (
        f"🏁 Eternal Hunter finished {CYCLE_LIMIT} cycles.\n"
        f"Total findings: {total_findings}\n"
        f"Criticals: {len(criticals)}"
    )
    send_discord(summary_msg, color=0xff0000)
    log(summary_msg)

if __name__ == "__main__":
    main()
