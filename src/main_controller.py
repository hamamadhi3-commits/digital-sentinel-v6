import os
import json
import time
from datetime import datetime
from src.recon_engine_parallel import run_recon_parallel
from src.duplication_checker import check_duplicates
from src.auto_report_compose import compose_report
from src.discord_notify import send_discord_message

# ==============================================================
#  DIGITAL SENTINEL v6.1 — SELF-HEALING EDITION
#  by Themoralhack & Manus
# ==============================================================

CONFIG_PATH = "data/targets/config.json"
TARGET_PATH = "data/targets/global_500_targets.txt"
LOG_DIR = "data/logs"
REPORT_DIR = "data/reports"

def safe_mkdir(path):
    """Create directory safely without crashing if it exists."""
    try:
        os.makedirs(path, exist_ok=True)
    except FileExistsError:
        pass
    except Exception as e:
        print(f"[WARN] Could not create directory {path}: {e}")

def safe_load_json(path, default={}):
    """Load JSON safely or return default if file missing."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[WARN] Missing {path}, generating default config.")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(default, f, indent=2)
        return default
    except Exception as e:
        print(f"[ERROR] Failed to read {path}: {e}")
        return default

def main_cycle():
    # === Self-Healing Startup ===
    print(f"🧠 Digital Sentinel v6.1 – Self-Healing Autonomous Mode started at {datetime.now()}")

    safe_mkdir("data")
    safe_mkdir("data/targets")
    safe_mkdir(LOG_DIR)
    safe_mkdir(REPORT_DIR)

    cfg = safe_load_json(CONFIG_PATH, default={"mode": "autonomous", "max_parallel": 5})

    # === Load Targets ===
    targets = []
    try:
        with open(TARGET_PATH, "r") as f:
            targets = [t.strip() for t in f.readlines() if t.strip()]
        print(f"[INFO] Loaded {len(targets)} targets from {TARGET_PATH}")
    except FileNotFoundError:
        print(f"[ERROR] Target file not found: {TARGET_PATH}")
        return
    except Exception as e:
        print(f"[ERROR] Could not load targets: {e}")
        return

    # === Recon Phase ===
    try:
        run_recon_parallel(targets)
    except Exception as e:
        print(f"[ERROR] Recon failed: {e}")

    # === Duplication Check ===
    try:
        check_duplicates()
    except Exception as e:
        print(f"[WARN] Duplication checker error: {e}")

    # === Auto Report Compose ===
    try:
        compose_report()
    except Exception as e:
        print(f"[WARN] Report compose error: {e}")

    # === Discord Notify ===
    try:
        send_discord_message("✅ Digital Sentinel v6.1 cycle completed successfully!")
    except Exception as e:
        print(f"[WARN] Discord notification failed: {e}")

    print(f"🧩 Cycle completed at {datetime.now()}")

if __name__ == "__main__":
    main_cycle()
