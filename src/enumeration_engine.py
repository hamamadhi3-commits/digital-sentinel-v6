# src/enumeration_engine.py
# Enumeration Engine: discovers subdomains for each target
# Tools: Subfinder, Amass, Assetfinder
# Author: Digital Sentinel v6 System

import os
import subprocess
from datetime import datetime

class EnumerationEngine:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.results_dir = os.path.join(base_dir, "data", "results", "enumeration")
        os.makedirs(self.results_dir, exist_ok=True)

    def run_tool(self, tool, target):
        """Helper to run a single enumeration tool."""
        output_file = os.path.join(self.results_dir, f"{target}_{tool}.txt")
        try:
            print(f"⚙️ Running {tool} on {target} ...")
            cmd = f"{tool} -d {target} -silent -o {output_file}"
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {tool} finished for {target}")
        except Exception as e:
            print(f"❌ Error running {tool} on {target}: {e}")

    def merge_results(self, target):
        """Combine all results from the three tools."""
        merged_file = os.path.join(self.results_dir, f"{target}_merged.txt")
        seen = set()
        with open(merged_file, "w") as out:
            for tool in ["subfinder", "amass", "assetfinder"]:
                path = os.path.join(self.results_dir, f"{target}_{tool}.txt")
                if os.path.exists(path):
                    with open(path, "r") as f:
                        for line in f:
                            domain = line.strip()
                            if domain and domain not in seen:
                                out.write(domain + "\n")
                                seen.add(domain)
        print(f"📄 Merged subdomains saved: {merged_file}")
        return merged_file

    def run(self, target):
        print(f"\n🌐 Starting Enumeration for {target}")
        for tool in ["subfinder", "amass", "assetfinder"]:
            self.run_tool(tool, target)
        merged = self.merge_results(target)
        print(f"🔍 Enumeration complete for {target}\n")
        return merged
