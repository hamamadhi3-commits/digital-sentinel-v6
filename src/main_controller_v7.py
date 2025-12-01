import os
import json
import random
import time
from datetime import datetime

from src.recon_engine_parallel import run_recon_cycle
from src.ai_vuln_detector import ai_vuln_detector
from src.discord_notify import send_discord_alert

MEMORY_FILE = "data/sentinel_memory.json"
TARGET_FILE = "data/targets/global_500_targets.txt"
LOG_DIR = "data/logs"
REPORT_DIR = "data/reports"

# ==============================================================
#  DIGITAL SENTINEL v7.0 — QUANTUM INTELLIGENCE MODE
#  Self-learning, adaptive, and context-aware recon system
# ==============================================================

def load_memory():
    """Load or initialize sentinel memory."""
    if not os.path.exists(MEMORY_FILE):
        base = {"runs": 0, "avg_duration": 0.0, "last_targets": [], "failures": 0}
        json.dump(base, open(MEMORY_FILE, "w"), indent=2)
        return base
    return json.load(open(MEMORY_FILE))

def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE, "w"), indent=2)

def adaptive_target_selection():
    """Choose dynamic subset of targets intelligently."""
    with open(TARGET_FILE) as f:
        targets = [x.strip() for x in f.readlines() if x.strip()]
    subset_size = random.randint(20, 80)
    return random.sample(targets, min(subset_size, len(targets)))

def main_cycle():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    mem = load_memory()
    cycle_id = mem["runs"] + 1
    start = datetime.now()
    print(f"\n🚀 [CYCLE {cycle_id}] Digital Sentinel v7.0 Quantum Intelligence started — {start}")

    try:
        targets = adaptive_target_selection()
        print(f"🧭 Selected {len(targets)} adaptive targets for this cycle.")
        run_recon_cycle(targets)
    except Exception as e:
        print(f"❌ Recon error: {e}")
        mem["failures"] += 1
        send_discord_alert("Recon Failure", str(e))

    try:
        report = ai_vuln_detector()
        print(f"✅ AI Vulnerability Analysis → {report}")
    except Exception as e:
        print(f"⚠️ AI Detector error: {e}")

    duration = (datetime.now() - start).total_seconds()
    mem["runs"] += 1
    mem["avg_duration"] = (mem["avg_duration"] * (mem["runs"] - 1) + duration) / mem["runs"]
    mem["last_targets"] = targets
    save_memory(mem)

    print(f"🏁 [CYCLE {cycle_id}] Completed in {duration:.2f}s (Avg ={mem['avg_duration']:.2f}s)")
    send_discord_alert(
        "Digital Sentinel v7.0 Cycle Complete",
        f"Cycle {cycle_id}\nDuration {duration:.2f}s\nFailures {mem['failures']}"
    )

if __name__ == "__main__":
    while True:
        main_cycle()
        sleep_time = random.randint(300, 900)  # Adaptive sleep (5–15 min)
        print(f"🕓 Next cycle in {sleep_time // 60} minutes...\n")
        time.sleep(sleep_time)
