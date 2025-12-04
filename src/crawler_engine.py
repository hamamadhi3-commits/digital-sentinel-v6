# src/crawler_engine.py
# Crawler & JS Parser Engine
# Uses Katana to crawl URLs and extract endpoints from target
# Author: Digital Sentinel v6

import os
import subprocess

class CrawlerEngine:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.input_dir = os.path.join(base_dir, "data", "results", "http_probe")
        self.results_dir = os.path.join(base_dir, "data", "results", "crawler")
        os.makedirs(self.results_dir, exist_ok=True)

    def run_crawler(self, target):
        input_file = os.path.join(self.input_dir, f"{target}_httpx.txt")
        output_file = os.path.join(self.results_dir, f"{target}_katana.txt")

        if not os.path.exists(input_file):
            print(f"⚠️ No HTTPX results found for {target}")
            return None

        print(f"🕷️ Running Katana crawler for {target} ...")
        cmd = f"katana -list {input_file} -silent -o {output_file} -d 2 -jc -kf -aff"
        # -d 2 → crawl depth
        # -jc → JS crawling enabled
        # -kf → keep forms
        # -aff → automatic form filling

        try:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ Katana crawling complete for {target}")
        except Exception as e:
            print(f"❌ Error running Katana: {e}")

        return output_file
