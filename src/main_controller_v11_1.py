# src/main_controller_v11_1.py
# Central coordinator for the Digital Sentinel Autonomous System (v11.1)
# ✅ Includes: PassiveIntelEngine + ActiveIntelEngine + Auto Logging

import os
import traceback
import datetime
from contextlib import redirect_stdout

from engines.active_intel_engine import ActiveIntelEngine
from engines.passive_intel_engine import PassiveIntelEngine


def setup_logging():
    """Create /data/logs/ folder and return an open log file."""
    log_dir = os.path.join("data", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"scan_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    print(f"🧾 Log file created: {log_file}")
    return open(log_file, "w", encoding="utf-8")


def main():
    print("🚀 Launching Sentinel Autonomous Controller (v11.1)")
    try:
        targets_file = os.path.join("data", "targets.txt")

        # Create targets file if not exists
        if not os.path.exists(targets_file):
            print("⚠️ No targets.txt found, creating default one...")
            os.makedirs(os.path.dirname(targets_file), exist_ok=True)
            with open(targets_file, "w") as f:
                f.write("example.com\n")

        # Read targets
        with open(targets_file, "r") as f:
            targets = [t.strip() for t in f.readlines() if t.strip()]

        if not targets:
            print("⚠️ No targets to scan.")
            return

        for target in targets:
            print(f"\n===== 🎯 TARGET: {target} =====")
            print("◆ Passive Recon:")
            passive = PassiveIntelEngine()
            passive.run(target)

            print("◆ Active Recon:")
            active = ActiveIntelEngine()
            active.run(target)

        print("\n✅ Scan completed successfully.\n")

    except Exception as e:
        print(f"❌ Error in main controller: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    # Redirect stdout to log file automatically
    with setup_logging() as log:
        with redirect_stdout(log):
            main()
