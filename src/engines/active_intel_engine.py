import asyncio
import socket
import shodan
import httpx
import subprocess
from bs4 import BeautifulSoup
import tldextract
import os

SHODAN_KEY = os.getenv("SHODAN_API_KEY", "").strip()

# -----------------------------------------------------
# 1) FAST PORT SCAN (nmap)
# -----------------------------------------------------
def fast_portscan(domain):
    try:
        result = subprocess.check_output(
            ["nmap", "-Pn", "-T4", "--top-ports", "50", domain],
            stderr=subprocess.DEVNULL
        ).decode()
        return result
    except:
        return "nmap_failed"


# -----------------------------------------------------
# 2) SHODAN LOOKUP
# -----------------------------------------------------
def shodan_lookup(ip):
    if not SHODAN_KEY:
        return {"shodan": "no_api_key"}

    try:
        api = shodan.Shodan(SHODAN_KEY)
        res = api.host(ip)
        return res
    except:
        return {"shodan": "lookup_failed"}


# -----------------------------------------------------
# 3) HTTPX URL PROBE
# -----------------------------------------------------
async def probe_url(url):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url)
            return {
                "url": url,
                "status": r.status_code,
                "title": BeautifulSoup(r.text, "lxml").title.string if r.text else ""
            }
    except:
        return {"url": url, "status": "failed"}


# -----------------------------------------------------
# 4) Extract Root + build URLs
# -----------------------------------------------------
def build_urls(domain):
    schema = ["http://", "https://"]
    paths = ["", "/login", "/admin", "/portal", "/dashboard"]
    urls = []

    for s in schema:
        for p in paths:
            urls.append(s + domain + p)

    return urls


# -----------------------------------------------------
# 5) ACTIVE INTEL ENGINE (Main)
# -----------------------------------------------------
async def active_intel(domain):
    print(f"[ACTIVE] Running active intel for {domain}")

    # Resolve IP
    try:
        ip = socket.gethostbyname(domain)
    except:
        ip = "resolve_failed"

    # Portscan
    ports = fast_portscan(domain)

    # Shodan
    shodan_res = shodan_lookup(ip)

    # URL Probing
    urls = build_urls(domain)
    probed = await asyncio.gather(*(probe_url(u) for u in urls))

    return {
        "domain": domain,
        "ip": ip,
        "ports": ports,
        "shodan": shodan_res,
        "urls": probed
    }
