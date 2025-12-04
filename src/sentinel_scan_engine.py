# =====================================================
# Digital Sentinel v11.3 - Autonomous Scan Engine
# =====================================================
import subprocess
import os
from datetime import datetime

class SentinelScanEngine:
    def __init__(self, target, output_dir="data/reports"):
        self.target = target.strip()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _run_tool(self, command, log_name):
        """Run CLI tools and log their outputs."""
        log_path = os.path.join(self.output_dir, log_name)
        with open(log_path, "w") as f:
            process = subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT, shell=True)
            process.communicate()
        print(f"[+] Finished: {log_name}")
        return log_path

    # ----------------------------
    # 1. Subdomain Enumeration
    # ----------------------------
    def enumerate_subdomains(self):
        print(f"[1] Enumerating subdomains for {self.target} ...")
        cmd = f"subfinder -d {self.target} -silent | tee {self.output_dir}/subdomains.txt"
        return self._run_tool(cmd, "enumeration.log")

    # ----------------------------
    # 2. HTTP Probing
    # ----------------------------
    def probe_http(self):
        print(f"[2] Probing HTTP endpoints ...")
        cmd = f"httpx -l {self.output_dir}/subdomains.txt -mc 200,302,403 -silent -o {self.output_dir}/live_hosts.txt"
        return self._run_tool(cmd, "httpx.log")

    # ----------------------------
    # 3. Crawling and JS Parsing
    # ----------------------------
    def crawl_endpoints(self):
        print(f"[3] Crawling live targets with Katana ...")
        cmd = f"katana -list {self.output_dir}/live_hosts.txt -silent -o {self.output_dir}/endpoints.txt"
        return self._run_tool(cmd, "katana.log")

    # ----------------------------
    # 4. Vulnerability Scanning
    # ----------------------------
    def run_nuclei(self):
        print(f"[4] Running Nuclei vulnerability scan ...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        cmd = f"nuclei -l {self.output_dir}/live_hosts.txt -t cves/ -o {self.output_dir}/vulns_{timestamp}.txt"
        return self._run_tool(cmd, f"nuclei_{timestamp}.log")

    # ----------------------------
    # Full Cycle Execution
    # ----------------------------
    def run_full_scan(self):
        print("🚀 Starting full autonomous scan cycle...\n")
        self.enumerate_subdomains()
        self.probe_http()
        self.crawl_endpoints()
        self.run_nuclei()
        print("✅ Scan cycle completed successfully.")
