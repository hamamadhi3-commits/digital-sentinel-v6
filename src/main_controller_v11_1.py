# src/main_controller_v11_1.py
# Central coordinator for the Digital Sentinel autonomous scanning cycle

import os
import traceback
from engines.active_intel_engine import ActiveIntelEngine
from engines.passive_intel_engine import PassiveIntelEngine

def main():
    print("🚀 Launching Sentinel Autonomous Controller (v11.1)")
    try:
        targets_file = os.path.join("data", "targets", "targets.txt")
        if not os.path.exists(targets_file):
            print("⚠️ No targets.txt found, creating default one...")
            os.makedirs(os.path.dirname(targets_file), exist_ok=True)
            with open(targets_file, "w") as f:
                f.write("example.com\n")

        with open(targets_file, "r") as f:
            targets = [t.strip() for t in f.readlines() if t.strip()]

        if not targets:
            print("⚠️ No targets to scan. Exiting.")
            return

        passive_engine = PassiveIntelEngine()
        active_engine = ActiveIntelEngine()

        for target in targets:
            print(f"\n===== 🎯 TARGET: {target} =====")
            print("🔹 Passive Recon:")
            passive_engine.run(target)

            print("🔹 Active Recon:")
            active_engine.run(target)

        print("\n✅ Scan completed successfully.")

    except Exception as e:
        print("❌ Controller Error:", str(e))
        traceback.print_exc()

if __name__ == "__main__":
    main()
