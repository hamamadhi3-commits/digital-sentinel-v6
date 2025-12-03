import subprocess
import json
import os
import socket
import httpx
import asyncio

OUTPUT_DIR = "data/active_intel/"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_nmap_scan(domain):
    try:
        print(f"🔎 Running Nmap scan on {domain} ...")

        cmd = ["nmap", "-sV", "-T4", "-p-", domain]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output_path = f"{OUTPUT_DIR}/{domain}_nmap.txt"
        with open(output_path, "w") as f:
            f.write(result.stdout)

        return output_path

    except Exception as e:
        print(f"❌ Nmap scan failed: {e}")
        return None


def resolve_dns(domain):
    try:
        print(f"🌐 Resolving DNS → {domain}")
        ip = socket.gethostbyname(domain)
        return {"domain": domain, "ip": ip}
    except:
        return {"domain": domain, "ip": None}


async def check_http(domain):
    url = f"http://{domain}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(url)
            return {"domain": domain, "status": r.status_code}
    except:
        return {"domain": domain, "status": None}


def run_active_intel(domain):
    print(f"\n🚀 ACTIVE INTEL ENGINE → {domain}")

    dns_info = resolve_dns(domain)

    # HTTP check
    try:
        http_result = asyncio.run(check_http(domain))
    except:
        http_result = None

    # Nmap port scan
    nmap_file = run_nmap_scan(domain)

    result = {
        "dns": dns_info,
        "http": http_result,
        "nmap_output": nmap_file
    }

    output_json = f"{OUTPUT_DIR}/{domain}_active_intel.json"
    with open(output_json, "w") as f:
        json.dump(result, f, indent=2)

    print(f"📦 Saved → {output_json}")
    return result
