import time
import json
import traceback
from pathlib import Path

from engines.passive_intel_engine import PassiveIntelEngine
from engines.active_intel_engine import ActiveIntelEngine
from recon.active_recon_engine import ActiveReconEngine
from recon.passive_recon import PassiveRecon
from ai.ai_engine import AIEngine
from report_builder_engine import ReportBuilderEngine

CONFIG_PATH = "../config/sentinel_config.json"
TARGETS_FILE = "../data/targets/global_500_targets.txt"
LOG_DIR = "../data/logs/"
REPORT_DIR = "../data/reports/"

class SentinelMainController:
    def __init__(self):
        self.load_config()
        self.create_dirs()

        self.passive_intel = PassiveIntelEngine()
        self.active_intel = ActiveIntelEngine()
        self.passive_recon = PassiveRecon()
        self.active_recon = ActiveReconEngine()
        self.ai_engine = AIEngine()
        self.reporter = ReportBuilderEngine()

    def load_config(self):
        with open(CONFIG_PATH, "r") as f:
            self.config = json.load(f)

    def create_dirs(self):
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
        Path(REPORT_DIR).mkdir(parents=True, exist_ok=True)

    def load_targets(self):
        with open(TARGETS_FILE, "r") as f:
            return [x.strip() for x in f.readlines() if x.strip()]

    def run_cycle(self):
        targets = self.load_targets()

        print(f"[+] Loaded {len(targets)} targets.")
        cycle = 0

        while True:
            cycle += 1
            print(f"\n========== CYCLE {cycle} STARTED ==========")

            for target in targets:
                try:
                    print(f"\n[+] Processing target: {target}")

                    data1 = self.passive_intel.collect(target)
                    data2 = self.active_intel.collect(target)
                    data3 = self.passive_recon.scan(target)
                    data4 = self.active_recon.scan(target)

                    merged = self.ai_engine.analyze(target, data1, data2, data3, data4)

                    self.reporter.save(target, merged)

                except Exception as e:
                    error_msg = traceback.format_exc()
                    print(f"[ERROR] Failed on {target}: {error_msg}")

            print(f"========== CYCLE {cycle} COMPLETED ==========\n")
            print("[+] Sleeping 10 minutes before next cycle...")
            time.sleep(600)


if __name__ == "__main__":
    s = SentinelMainController()
    s.run_cycle()
