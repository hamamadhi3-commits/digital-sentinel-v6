import os, json, time
from datetime import datetime

from src.threat_feed_integrator import fuse_threat_feeds
from src.recon_engine_parallel import run_recon_cycle
from src.ai_vuln_detector import ai_vuln_detector
from src.quantum_reasoner import run_quantum_reasoning
from src.overlord_commander import prioritize_targets, allocate_resources, generate_overlord_report
from src.discord_notify import send_discord_alert

MEMORY_FILE = "data/sentinel_memory.json"
LOG_DIR, REPORT_DIR = "data/logs", "data/reports"

# ==============================================================
#  DIGITAL SENTINEL v9.0 — QUANTUM OVERLORD MODE
# ==============================================================

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        base = {"runs": 0, "failures": 0, "last_targets": [], "avg_time": 0.0}
        json.dump(base, open(MEMORY_FILE, "w"), indent=2)
        return base
    return json.load(open(MEMORY_FILE))

def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE, "w"), indent=2)

def main_cycle():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    mem = load_memory()

    start = datetime.now()
    print(f"\n🚀 [CYCLE {mem['runs']+1}] Quantum Overlord Mode started — {start}")

    # === Threat Feed ===
    feed = fuse_threat_feeds()
    targets = [p["url"] for p in feed.get("bugcrowd_feed", [])[:100]]

    # === Overlord Decision ===
    prioritized = prioritize_targets(targets)
    clusters = allocate_resources(prioritized)
    decision_report = generate_overlord_report(prioritized)

    # === Recon + AI Reasoning ===
    try:
        for tier, group in clusters.items():
            print(f"\n⚙️ Launching {tier.upper()} cluster scan ({len(group)} targets)...")
            run_recon_cycle(group)
            ai_vuln_detector()
            run_quantum_reasoning()
    except Exception as e:
        print(f"[ERROR] Cluster cycle failure: {e}")
        mem["failures"] += 1

    duration = (datetime.now() - start).total_seconds()
    mem["runs"] += 1
    mem["avg_time"] = (mem["avg_time"]*(mem["runs"]-1) + duration)/mem["runs"]
    mem["last_targets"] = targets
    save_memory(mem)

    print(f"🏁 Cycle finished in {duration:.2f}s — {len(targets)} targets processed.")
    send_discord_alert(
        "Digital Sentinel v9.0 – Overlord Decision Report",
        f"Duration {duration:.2f}s\nClusters: {len(clusters['high'])} High, {len(clusters['medium'])} Medium, {len(clusters['low'])} Low"
    )

if __name__ == "__main__":
    while True:
        main_cycle()
        time.sleep(900)  # every 15 minutes
