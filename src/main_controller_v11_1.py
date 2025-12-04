# src/main_controller_v11_1.py

import json
import time
import os
from engines.active_intel_engine import ActiveIntelEngine
from engines.passive_intel_engine import PassiveIntelEngine


class DigitalSentinelController:

    def __init__(self):
        self.active_engine = ActiveIntelEngine()
        self.passive_engine = PassiveIntelEngine()

    def load_targets(self):
        path = "../data/targets/targets.txt"
        if not os.path.exists(path):
            raise FileNotFoundError("targets.txt NOT FOUND")

        with open(path, "r") as f:
            targets = [x.strip() for x in f.readlines() if x.strip()]

        return targets

    def run(self):
        print("\n[ SENTINEL V6 STARTED ]\n")
        targets = self.load_targets()

        for target in targets:
            print(f"\n=== Processing Target: {target} ===")

            passive = self.passive_engine.run(target)
            active = self.active_engine.run(target)

            result = {
                "target": target,
                "passive": passive,
                "active": active,
                "timestamp": time.time()
            }

            self.save_result(target, result)

        print("\n[ COMPLETED ALL TARGETS ]\n")

    def save_result(self, target, data):
        folder = "../data/results/"
        os.makedirs(folder, exist_ok=True)

        filename = f"{folder}/{target.replace('.', '_')}.json"

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"[ SAVED ] {filename}")


if __name__ == "__main__":
    controller = DigitalSentinelController()
    controller.run()
