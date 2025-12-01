import os
import json
import time
import socket
import requests
import subprocess
import concurrent.futures
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# ============================================
# 🛰️ CONFIGURATION
# ============================================
TARGETS_FILE = "data/targets.txt"
RECON_REPORT = "data/reports/recon_summary.json"
MAX_WORKERS = 10
SUBDOMAIN_LIMIT = 100
HTTP_TIMEOUT = 7
PORT_SCAN_LIMIT = [80, 443, 8080, 8443, 22, 21, 25, 3306, 5432]

# ============================================
# ⚙️ UTILITY FUNCTIONS
# ============================================
def log(msg):
    print(f"[🛰️] {msg}")

def discord_notify(title, message, color=0x3498DB):
    if not DISCORD_WEBHOOK:
        return
    payload = {
        "embeds": [{
            "title": title,
            "description": message,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {"text": "Digital Sentinel v11 • Eternal Hunter"}
        }]
    }
    try:
        requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception as e:
        print(f"⚠️ Discord Error: {e}")

# ============================================
# 🔎 SUBDOMAIN DISCOVERY
# ============================================
def find_subdomains(domain):
    """Try to enumerate subdomains using public sources."""
    log(f"Scanning subdomains for {domain}")
    subdomains = set()

    # Passive APIs (can expand later)
    sources = [
        f"https://crt.sh/?q=%25.{domain}&output=json",
        f"https://dns.bufferover.run/dns?q=. {domain}",
    ]

    for src in sources:
        try:
            resp = requests.get(src, timeout=HTTP_TIMEOUT, headers={"User-Agent": "EternalHunter/1.0"})
            if resp.status_code == 200 and "json" in resp.headers.get("Content-Type", ""):
                data = resp.json()
                for item in data:
                    if isinstance(item, dict) and "name_value" in item:
                        subdomains.add(item["name_value"].strip())
        except Exception:
            continue

    # fallback pattern guesses
    common = ["dev", "api", "staging", "test", "mail", "portal", "vpn", "admin", "beta"]
    for sub in common:
        subdomains.add(f"{sub}.{domain}")

    return list(subdomains)[:SUBDOMAIN_LIMIT]

# ============================================
# 🌐 HTTP PROBE
# ============================================
def probe_http(url):
    """Check if a subdomain is live via HTTP(S)."""
    schemes = ["https://", "http://"]
    for scheme in schemes:
        try:
            resp = requests.get(scheme + url, timeout=HTTP_TIMEOUT)
            if resp.status_code < 500:
                return {"url": scheme + url, "status": resp.status_code, "server": resp.headers.get("Server", "unknown")}
        except Exception:
            pass
    return None

# ============================================
# 🔓 PORT SCANNING
# ============================================
def scan_ports(target):
    open_ports = []
    for port in PORT_SCAN_LIMIT:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            pass
    return open_ports

# ============================================
# ⚡ PARALLEL EXECUTION ENGINE
# ============================================
def recon_target(domain):
    log(f"Starting recon for {domain}")
    try:
        subdomains = find_subdomains(domain)
        live_hosts = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(probe_http, sub): sub for sub in subdomains}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    live_hosts.append(result)

        open_ports = scan_ports(domain)

        return {
            "domain": domain,
            "subdomains_found": len(subdomains),
            "live_hosts": live_hosts,
            "open_ports": open_ports
        }

    except Exception as e:
        return {"domain": domain, "error": str(e)}

# ============================================
# 🧠 MAIN CONTROLLER
# ============================================
def main():
    if not os.path.exists(TARGETS_FILE):
        print("❌ No targets file found.")
        return

    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip()]

    log(f"Loaded {len(targets)} targets.")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(recon_target, t): t for t in targets}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    # Save results
    os.makedirs(os.path.dirname(RECON_REPORT), exist_ok=True)
    with open(RECON_REPORT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    # Send Discord summary
    total_subs = sum(len(r.get("live_hosts", [])) for r in results)
    discord_notify(
        "🛰️ Recon Cycle Completed",
        f"Scanned {len(results)} targets • Found {total_subs} live subdomains",
        color=0x2ECC71
    )

    log("✅ Recon summary written successfully.")

if __name__ == "__main__":
    print("🚀 Starting Eternal Recon Engine ...")
    main()
