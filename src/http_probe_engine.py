# src/http_probe_engine.py
# HTTP Probe Engine: checks live hosts and fetches basic metadata
# Tools: httpx (by ProjectDiscovery)
# Author: Digital Sentinel v6

import os
import subprocess
from datetime import datetime

class HTTPProbeEngine:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.results_dir = os.path.join(base_dir, "data", "results", "http_probe")
        os.makedirs(self.results_dir, exist_ok=True)

    def run_probe(self, target):
        input_file = os.path.join(base_dir, "data", "results", "enumeration", f"{target}_merged.txt")
        output_file = os.path.join(self.results_dir, f"{target}_httpx.txt")
        if not os.path.exists(input_file):
            print(f"⚠️ No enumeration file found for {target}")
            return None

        print(f"🌐 Running HTTPX probe on {target} ...")
        cmd = f"httpx -l {input_file} -title -tech-detect -status-code -o {output_file} -silent"
        try:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ HTTP probing complete for {target}")
        except Exception as e:
            print(f"❌ Error running HTTPX: {e}")

        return output_file
