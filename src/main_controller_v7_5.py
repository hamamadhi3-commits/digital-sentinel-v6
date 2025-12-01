import os, json, time
from datetime import datetime

from src.threat_feed_integrator import fuse_threat_feeds
from src.recon_engine_parallel import run_recon_cycle
from src.ai_vuln_detector import ai_vuln_detector
from src.discord_notify import send_discord_alert

MEMORY_FILE = "data/sentinel_memory.json"
LOG_DIR, REPORT_DIR = "data/logs", "data/reports"

# ==============================================================
#  DIGITAL SENTINEL v7.5 — THREAT FUSION INTELLIGENCE MODE
# ==============================================================

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        base = {"runs": 0, "failures": 0, "avg_time": 0.0}
        json.dump(base, open(MEMORY_FILE,"w"), indent=2)
        return base
    return json.load(open(MEMORY_FILE))

def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE,"w"), indent=2)

def main_cycle():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    mem = load_memory()

    start = datetime.now()
    print(f"\n🚀 [CYCLE {mem['runs']+1}] Sentinel v7.5 Started — {start}")

    # === Threat Fusion Feed ===
    threat_info = fuse_threat_feeds()

    # === Recon Phase ===
    try:
        run_recon_cycle(threat_info.get("bugcrowd_feed", []))
    except Exception as e:
        print(f"[ERROR] Recon failure: {e}")
        mem["failures"] += 1
        send_discord_alert("Recon Failure", str(e))

    # === AI Detection ===
    try:
        ai_vuln_detector()
    except Exception as e:
        print(f"[WARN] AI Detector error: {e}")

    duration = (datetime.now() - start).total_seconds()
    mem["runs"] += 1
    mem["avg_time"] = (mem["avg_time"]*(mem["runs"]-1) + duration)/mem["runs"]
    save_memory(mem)

    send_discord_alert(
        "Digital Sentinel v7.5 Cycle Complete",
        f"Duration {duration:.2f}s\nFeeds Integrated: {threat_info['summary']}"
    )
    print(f"🏁 [CYCLE] Done in {duration:.2f}s — {threat_info['summary']}")

if __name__ == "__main__":
    while True:
        main_cycle()
        time.sleep(600)  # every 10 minutes
