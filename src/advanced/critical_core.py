# ==========================================================
#  Digital Sentinel – Critical Core Engine (v1)
#  Master Foundation Layer for Autonomous Vulnerability Hunting
#  Built for Themoralhack 🐺🔥
# ==========================================================

import os
import json
import time
import hashlib
import threading
from datetime import datetime

CORE_DB = "data/logs/core_state.json"


class CriticalCore:
    """
    The lowest-level foundation engine.
    - Tracks where the system stopped
    - Stores last processed target
    - Maintains stable resume-from-checkpoint capability
    - Ensures ZERO loss scanning even if GitHub Actions stops
    """

    def __init__(self):
        self.state = self.load_state()

    def load_state(self):
        """Load system last-known state."""
        if not os.path.exists(CORE_DB):
            return {
                "last_target": None,
                "last_module": None,
                "last_vuln": None,
                "timestamp": None
            }
        try:
            with open(CORE_DB, "r") as f:
                return json.load(f)
        except:
            return {
                "last_target": None,
                "last_module": None,
                "last_vuln": None,
                "timestamp": None
            }

    def save_state(self):
        """Save system progress."""
        os.makedirs(os.path.dirname(CORE_DB), exist_ok=True)
        with open(CORE_DB, "w") as f:
            json.dump(self.state, f, indent=4)

    def update(self, key, value):
        """Update state key."""
        self.state[key] = value
        self.state["timestamp"] = str(datetime.utcnow())
        self.save_state()

    def record_target(self, target):
        """Record last processed target."""
        self.update("last_target", target)

    def record_module(self, module):
        """Record last running module."""
        self.update("last_module", module)

    def record_vuln(self, vuln):
        """Record last vulnerability processed."""
        self.update("last_vuln", vuln)

    def get_resume_info(self):
        """Return restart information for auto-resume."""
        return {
            "last_target": self.state.get("last_target"),
            "last_module": self.state.get("last_module"),
            "last_vuln": self.state.get("last_vuln"),
            "timestamp": self.state.get("timestamp")
        }


# ==========================================================
# Utility functions
# ==========================================================

def fast_hash(text):
    """Ultra-fast hash to detect duplicates and track changes."""
    return hashlib.md5(text.encode()).hexdigest()


def safe_log(path, content):
    """Safe append logging."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(content + "\n")


def timestamp():
    return str(datetime.utcnow())


# ==========================================================
# AUTO-RESUME ENGINE
# ==========================================================

class AutoResumeEngine:
    """
    This module ensures:
    - GitHub Actions time-limit safe checkpointing
    - Resume EXACTLY from where it stopped last time
    - No reprocessing targets/modules/vulns
    """

    def __init__(self, core: CriticalCore):
        self.core = core

    def should_skip(self, target, module):
        """
        Decide if this run already passed this stage.
        Used to skip old progress.
        """
        resume = self.core.get_resume_info()

        if resume["last_target"] is None:
            return False  # fresh run

        # If we already passed this target+module, skip
        if target == resume["last_target"] and module == resume["last_module"]:
            return False  # This is EXACT point of resume → DO NOT SKIP

        # If target < last_target alphabetically → skip
        if target < resume["last_target"]:
            return True

        # If same target but module < last_module → skip
        if target == resume["last_target"] and module < resume["last_module"]:
            return True

        return False


# ==========================================================
# SYSTEM HEARTBEAT
# ==========================================================

def sentinel_heartbeat():
    """
    Runs in background & writes heartbeat.
    Helps detect freeze, crash, or stalling.
    GitHub watchers can monitor this.
    """
    while True:
        safe_log("data/logs/heartbeat.log", f"Heartbeat: {timestamp()}")
        time.sleep(30)  # every 30 seconds


# ==========================================================
# Start background monitoring thread
# ==========================================================

def start_background_monitors():
    t = threading.Thread(target=sentinel_heartbeat)
    t.daemon = True
    t.start()


# ==========================================================
# END OF FILE
# ==========================================================
