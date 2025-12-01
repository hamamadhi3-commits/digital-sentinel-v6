"""
Digital Sentinel v6.0 – Recon Engine (Parallel)
Purpose: Executes vulnerability scans and subdomain reconnaissance
"""

import subprocess
import json
import os
from datetime import datetime

def run_recon_parallel(target):
    """Run recon & vuln scan for a single target domain."""
    print(f"[SCAN] Starting analysis for: {target}")

    log_path = f"data/logs/{target.replace('.', '_')}.log"
    result = {
        "target": target,
        "status": "unknown",
        "timestamp": str(datetime.now())
    }

    try:
        # Subdomain enumeration
        subfinder = subprocess.run(
            ["subfinder", "-d", target, "-silent"],
            capture_output=True, text=True
        )
        subs = subfinder.stdout.splitlines()
        result["subdomains"] = subs

        # HTTP probing
        httprobe = subprocess.run(
            ["httpx", "-l", "-", "-silent"],
            input="\n".join(subs),
            capture_output=True, text=True
        )
        result["live_hosts"] = httprobe.stdout.splitlines()

        # Vulnerability scanning example (dummy PoC)
        result["vulns"] = []
        for host in result["live_hosts"]:
            if "admin" in host:
                result["vulns"].append({"host": host, "issue": "Possible Admin Panel"})

        # Save log
        os.makedirs("data/logs", exist_ok=True)
        with open(log_path, "w") as lf:
            json.dump(result, lf, indent=2)

        print(f"[OK] Recon complete for {target} → {len(result['live_hosts'])} live hosts found")
        result["status"] = "success"
    except Exception as e:
        print(f"[ERR] {target} failed → {e}")
        result["status"] = "failed"

    return result
