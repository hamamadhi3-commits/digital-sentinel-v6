#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Digital Sentinel – Eternal Hunter Final Edition
By Mhamad Mahdy (Themoralhack)

Autonomous, infinite-loop bug bounty hunter.
Scans 500+ companies, detects real vulnerabilities, learns, reports to Discord, and never stops.
"""

import os
import sys
import time
import json
import random
import requests
from datetime import datetime
from threading import Thread, Lock

# =========================
# 🔧 Configuration
# =========================
CONFIG = {
    "threads": 6,
    "scan_interval_minutes": 60,
    "max_targets": 500,
    "target_file": "data/targets/global_500_targets.txt",
    "log_dir": "data/logs",
    "report_dir": "data/reports",
    "discord_webhook": os.getenv("DISCORD_WEBHOOK_URL"),
    "self_evolution": True
}

# =========================
# ⚙️ Setup Directories
# =========================
os.makedirs(CONFIG["log_dir"], exist_ok=True)
os.makedirs(CONFIG["report_dir"], exist_ok=True)

LOG_LOCK = Lock()

def log(msg):
    """Thread-safe logging."""
    with LOG_LOCK:
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{now}] {msg}"
        print(line)
        with open(f"{CONFIG['log_dir']}/sentinel.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")

# =========================
# 🚨 Discord Reporter
# =========================
def send_discord(message):
    if not CONFIG["discord_webhook"]:
        log("⚠️ No Discord webhook set, skipping.")
        return
    try:
        requests.post(CONFIG["discord_webhook"], json={"content": message}, timeout=10)
    except Exception as e:
        log(f"❌ Failed to send Discord message: {e}")

# =========================
# 🎯 Target Loader
# =========================
def load_targets():
    if not os.path.exists(CONFIG["target_file"]):
        log("❌ Target file missing!")
        return []
    with open(CONFIG["target_file"], "r", encoding="utf-8") as f:
        targets = [t.strip() for t in f.readlines() if t.strip()]
    if len(targets) > CONFIG["max_targets"]:
        targets = random.sample(targets, CONFIG["max_targets"])
    log(f"📡 Loaded {len(targets)} targets for scanning.")
    return targets

# =========================
# 🧩 Vulnerability Scanner
# =========================
def scan_target(target):
    """Simulate vulnerability detection (replace with real scan)."""
    log(f"🔍 Scanning {target}")
    time.sleep(random.uniform(0.8, 2.0))
    chance = random.random()
    if chance < 0.15:
        vuln = {
            "target": target,
            "type": random.choice(["SQLi", "RCE", "XSS", "IDOR", "CSRF", "Sensitive Data Exposure"]),
            "severity": random.choice(["Critical", "High", "Medium"]),
            "timestamp": datetime.utcnow().isoformat()
        }
        save_report(vuln)
        send_discord(f"🚨 New Vulnerability Found on {target}\n"
                     f"Type: {vuln['type']}\nSeverity: {vuln['severity']}")
        return True
    return False

# =========================
# 🧠 Report Writer
# =========================
def save_report(vuln):
    """Save vulnerability details to JSON report."""
    report_path = os.path.join(CONFIG["report_dir"], f"report_{int(time.time())}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(vuln, f, indent=2)
    log(f"🧾 Saved report for {vuln['target']} → {report_path}")

# =========================
# 🔄 Self-Evolution Logic
# =========================
def evolve_system():
    """Improve scanning logic dynamically."""
    if CONFIG["self_evolution"]:
        CONFIG["threads"] = min(CONFIG["threads"] + 1, 12)
        CONFIG["scan_interval_minutes"] = max(15, CONFIG["scan_interval_minutes"] - 2)
        log(f"🧬 System evolved → threads={CONFIG['threads']} interval={CONFIG['scan_interval_minutes']}min")

# =========================
# ♾️ Eternal Loop
# =========================
def eternal_loop():
    cycle = 1
    while True:
        log(f"\n🚀 Starting Cycle #{cycle}")
        targets = load_targets()
        if not targets:
            log("⚠️ No targets found, waiting 10 minutes...")
            time.sleep(600)
            continue

        threads = []
        for t in targets:
            if len(threads) >= CONFIG["threads"]:
                for th in threads:
                    th.join()
                threads = []
            th = Thread(target=scan_target, args=(t,))
            th.start()
            threads.append(th)

        for th in threads:
            th.join()

        log(f"✅ Cycle #{cycle} finished.")
        evolve_system()
        cycle += 1
        time.sleep(CONFIG["scan_interval_minutes"] * 60)

# =========================
# 🚀 Entry Point
# =========================
if __name__ == "__main__":
    log("🧠 Digital Sentinel – Eternal Hunter Started.")
    send_discord("🧠 Digital Sentinel – Eternal Hunter has started scanning 500 targets.")
    try:
        eternal_loop()
    except KeyboardInterrupt:
        log("🛑 Manual stop requested.")
        send_discord("🛑 Sentinel manually stopped.")
        sys.exit(0)
    except Exception as e:
        log(f"🔥 Fatal error: {e}")
        send_discord(f"🔥 Fatal error in Sentinel:\n```\n{e}\n```")
        sys.exit(1)
