# ---------------------------------------------------------------
# Digital Sentinel v16 – Autonomous Re-Scan Smart Scheduler
# Learns where scanning stopped and restarts exactly from there.
# Prioritizes HOT companies and dangerous patterns.
# ---------------------------------------------------------------

import os
import json
import time
from datetime import datetime
from learning_brain import (
    suggest_priority_targets,
    suggest_hotspot_signatures,
    suggest_hot_technologies
)

STATE_FILE = "data/state.json"
TARGET_FILE = "data/targets/global_500_targets.txt"


def load_state():
    """Load last scan state (where it stopped)."""
    if not os.path.exists(STATE_FILE):
        return {"last_index": 0}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    """Save current scan state."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)


def load_targets():
    """Load all 500+ targets."""
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]


def get_priority_targets():
    """Mix priority companies with normal list."""
    priority = suggest_priority_targets(limit=50)
    normal = load_targets()

    final_list = []

    # Add priority first
    for p in priority:
        if p in normal:
            final_list.append(p)

    # Add rest
    for n in normal:
        if n not in final_list:
            final_list.append(n)

    return final_list


def smart_next_target():
    """
    Returns next target:
    - Resumes where it stopped last time.
    - If finished full cycle → restart, but with priority hot companies.
    """
    targets = get_priority_targets()
    total = len(targets)

    state = load_state()
    idx = state.get("last_index", 0)

    if idx >= total:  # finished full cycle
        idx = 0  # restart cycle

    target = targets[idx]
    state["last_index"] = idx + 1
    save_state(state)

    return target, idx + 1, total


def log(msg):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")


def run_scheduler():
    log("🔁 Starting Autonomous Smart Scheduler (v16)...")

    while True:
        try:
            target, index, total = smart_next_target()

            log(f"🎯 Next Target [{index}/{total}] → {target}")

            # give target to scan engine
            os.system(f"python3 scan_engine.py --single {target}")

        except Exception as e:
            log(f"⚠️ Scheduler error: {e}")
            time.sleep(300)   # wait 5 minutes before retry

        # wait before next target
        time.sleep(2)


if __name__ == "__main__":
    run_scheduler()
