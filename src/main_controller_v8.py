import os, json, time
from datetime import datetime

from src.threat_feed_integrator import fuse_threat_feeds
from src.recon_engine_parallel import run_recon_cycle
from src.ai_vuln_detector import ai_vuln_detector
from src.quantum_reasoner import run_quantum_reasoning
from src.discord_notify import send_discord_alert

MEMORY_FILE = "data/sentinel_memory.json"
LOG_DIR, REPORT_DIR = "data/logs", "data/reports"

# ==============================================================
#  DIGITAL SENTINEL v8.0 — QUANTUM COGNITION MODE
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

    print(f"\n🚀 [CYCLE {mem['runs']+1}] Quantum Cognition Mode started — {start}")

    # === Threat Fusion ===
    feed = fuse_threat_feeds()

    # === Recon & AI Detection ===
    try:
        targets = [p["url"] for p in feed.get("bugcrowd_feed", [])[:50]]
        mem["last_targets"] = targets
        run_recon_cycle(targets)
        ai_vuln_detector()
    except Exception as e:
        print(f"[ERROR] Core cycle failure: {e}")
        mem["failures"] += 1

    # === Quantum Reasoning Phase ===
    reasoning = run_quantum_reasoning()

    # === Finalization ===
    duration = (datetime.now() - start).total_seconds()
    mem["runs"] += 1
    mem["avg_time"] = (mem["avg_time"]*(mem["runs"]-1) + duration)/mem["runs"]
    save_memory(mem)

    print(f"🏁 Cycle finished in {duration:.2f}s with {len(reasoning['cycle_thoughts'])} insights.")
    send_discord_alert(
        "Digital Sentinel v8.0 Cognitive Cycle",
        f"Duration {duration:.2f}s — {len(reasoning['cycle_thoughts'])} reasoning insights generated."
    )

if __name__ == "__main__":
    while True:
        main_cycle()
        time.sleep(900)  # every 15 minutes
