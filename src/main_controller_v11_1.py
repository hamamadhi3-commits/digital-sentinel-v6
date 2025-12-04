import json
import os
import time
from engines.active_intel_engine import ActiveIntelEngine
from engines.passive_intel_engine import PassiveIntelEngine


CONFIG_PATH = "config/sentinel_config.json"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def load_targets():
    path = "data/targets/global_500_targets.txt"
    with open(path, "r") as f:
        return [x.strip() for x in f.readlines() if x.strip()]


def save_result(target, data):
    os.makedirs("data/results", exist_ok=True)
    outfile = f"data/results/{target.replace('.', '_')}.json"
    with open(outfile, "w") as f:
        json.dump(data, f, indent=4)


def main():
    print("\n🚀 DIGITAL SENTINEL V6 — Autonomous Cycle Started\n")

    config = load_config()
    targets = load_targets()

    active_engine = ActiveIntelEngine()
    passive_engine = PassiveIntelEngine()

    for target in targets:
        print(f"\n🔍 Scanning: {target}")
        result = {"target": target, "active": {}, "passive": {}}

        # ------------------------------------------
        # RUN PASSIVE ENGINE
        # ------------------------------------------
        try:
            result["passive"] = passive_engine.run(target)
            print("    ✔ Passive Engine OK")
        except Exception as e:
            result["passive"] = {"error": str(e)}
            print("    ❌ Passive Engine Failed")

        # ------------------------------------------
        # RUN ACTIVE ENGINE
        # ------------------------------------------
        try:
            result["active"] = active_engine.run(target)
            print("    ✔ Active Engine OK")
        except Exception as e:
            result["active"] = {"error": str(e)}
            print("    ❌ Active Engine Failed")

        # ------------------------------------------
        # SAVE OUTPUT
        # ------------------------------------------
        save_result(target, result)
        print(f"    💾 Saved results → data/results/{target.replace('.', '_')}.json")

        time.sleep(1)

    print("\n🎉 ALL TASKS COMPLETED — Sentinel Autonomous Cycle Finished!\n")


if __name__ == "__main__":
    main()
