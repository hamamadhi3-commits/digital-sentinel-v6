import os
import json
import time
import threading
from datetime import datetime
from .queue_manager import TaskQueue
from .checkpoint import CheckpointManager

class DigitalSentinelEngine:

    def __init__(self, targets, output_dir="results"):
        self.targets = targets
        self.output_dir = output_dir
        self.queue = TaskQueue(max_workers=40)
        self.checkpoint = CheckpointManager("sentinel_checkpoint.json")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # ===============================
    # Auto Resume System
    # ===============================
    def load_resume_state(self):
        saved = self.checkpoint.load()
        if saved:
            print("[+] Resuming from last checkpoint...")
            return saved
        return {}

    # ===============================
    # Main Start
    # ===============================
    def start(self):

        print("\n🔥 Starting Digital Sentinel Engine v12\n")

        resume_state = self.load_resume_state()

        for target in self.targets:
            if target in resume_state.get("completed", []):
                print(f"[+] Skipping {target}, already completed in previous scan.")
                continue

            print(f"[+] Adding tasks for: {target}")
            self.queue.add_task(lambda t=target: self.scan_target(t))

        self.queue.wait_completion()
        print("\n🏁 Scan Finished.")

    # ===============================
    # Scanner Logic
    # ===============================
    def scan_target(self, target):

        print(f"🔍 Scanning Target: {target}")

        from ..modules.passive_recon import passive_recon
        from ..modules.active_recon import active_recon
        from ..modules.shadow_recon import shadow_recon
        from ..modules.vuln_probe import vuln_probe

        # 1. Passive Recon
        subdomains = passive_recon(target)

        # 2. Active Recon
        alive = active_recon(subdomains)

        # 3. Shadow Recon Mode
        shadow = shadow_recon(target)

        # 4. Vulnerability Probing
        vulns = vuln_probe(alive + shadow)

        # Save
        result_path = os.path.join(self.output_dir, f"{target}.json")
        with open(result_path, "w") as f:
            json.dump({
                "target": target,
                "alive": alive,
                "shadow": shadow,
                "vulns": vulns,
                "timestamp": str(datetime.utcnow())
            }, f, indent=4)

        # Update checkpoint
        self.checkpoint.update_completed(target)

        print(f"[✓] Saved: {result_path}")
