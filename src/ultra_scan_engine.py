import httpx
import asyncio
import socket
import tldextract
import json
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# -------------------------------------------------
# Ultra Scan Engine — 10× Faster Vulnerability Radar
# -------------------------------------------------

async def fetch(url):
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=8) as client:
            r = await client.get(url)
            return r.text, r.status_code
    except:
        return None, None


def port_scan(host):
    open_ports = []
    common_ports = [80, 443, 22, 21, 25, 53, 8080, 8443, 3306]

    for p in common_ports:
        try:
            s = socket.socket()
            s.settimeout(0.4)
            s.connect((host, p))
            open_ports.append(p)
            s.close()
        except:
            pass

    return open_ports


def extract_js_urls(html, domain):
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    urls = []

    for tag in soup.find_all("script"):
        src = tag.get("src")
        if src and domain in src:
            urls.append(src)

    return urls


async def ultra_scan(domain):
    results = []

    # 1) Normalize
    extracted = tldextract.extract(domain)
    root = f"{extracted.domain}.{extracted.suffix}"

    targets = [
        f"http://{domain}",
        f"https://{domain}",
        f"http://www.{root}",
        f"https://www.{root}",
    ]

    # 2) Fetch Pages
    for url in targets:
        html, status = await fetch(url)
        if not status:
            continue

        entry = {
            "target": domain,
            "url": url,
            "status": status,
            "js_urls": extract_js_urls(html, domain),
            "possible_vulns": []
        }

        # Very simple signatures
        if "password" in html.lower():
            entry["possible_vulns"].append("Login Form Detected")

        if "api_key" in html.lower() or "token" in html.lower():
            entry["possible_vulns"].append("Secret Key Exposure")

        if "<script>" in html.lower() and "innerHTML" in html:
            entry["possible_vulns"].append("Possible XSS")

        results.append(entry)

    # 3) Port Scan
    host = extracted.registered_domain
    try:
        ip = socket.gethostbyname(domain)
        open_ports = port_scan(ip)

        results.append({
            "target": domain,
            "ip": ip,
            "open_ports": open_ports,
            "type": "portscan"
        })
    except:
        pass

    return results
