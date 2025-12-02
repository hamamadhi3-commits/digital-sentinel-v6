# ---------------------------------------------------------
# Digital Sentinel v11.1 – Scan Engine (Core)
# This module performs:
# - Subdomain scan
# - Live host detection
# - URL crawling
# - Basic vuln testing (placeholder)
# Result → list of findings for controller
# ---------------------------------------------------------

import subprocess
import json
import os
import tempfile


def run_cmd(cmd):
    """Run terminal command and return output safely."""
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
        return out.decode(errors="ignore").splitlines()
    except:
        return []


# ---------------------------------------------------------
# Step 1 — Subdomain Enumeration
# ---------------------------------------------------------

def subdomain_scan(domain):
    print(f"[SCAN] Subdomains → {domain}")
    cmd = f"subfinder -silent -d {domain}"
    return run_cmd(cmd)


# ---------------------------------------------------------
# Step 2 — Live Host Scan
# ---------------------------------------------------------

def live_scan(subs):
    print("[SCAN] Checking live hosts...")
    if not subs:
        return []

    with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
        for s in subs:
            f.write(s + "\n")
        path = f.name

    cmd = f"httpx -silent -list {path}"
    return run_cmd(cmd)


# ---------------------------------------------------------
# Step 3 — URL Crawler
# ---------------------------------------------------------

def crawl_urls(live_hosts):
    print("[SCAN] Crawling URLs…")
    urls = []

    for host in live_hosts:
        cmd = f"katana -silent -u {host}"
        out = run_cmd(cmd)
        urls.extend(out)

    return list(set(urls))


# ---------------------------------------------------------
# Step 4 — Basic Vulnerability Pattern Scan
# (This will be enriched by AI Priority Engine)
# ---------------------------------------------------------

def scan_vulns(urls):
    print("[SCAN] Basic vulnerability checks…")

    findings = []

    for u in urls:
        low = u.lower()

        # === Detect XSS pattern ===
        if "q=" in low or "search=" in low:
            findings.append({
                "summary": "Possible XSS injection point",
                "url": u,
                "impact": "medium",
                "vector": "network",
                "ease": "easy"
            })

        # === Detect IDOR patterns ===
        if "id=" in low and any(x in low for x in ["user", "uid", "profile"]):
            findings.append({
                "summary": "Potential IDOR parameter exposure",
                "url": u,
                "impact": "high",
                "vector": "network",
                "ease": "medium"
            })

        # === SQLi pattern ===
        if "id=" in low and "'" in low:
            findings.append({
                "summary": "Possible SQL Injection",
                "url": u,
                "impact": "high",
                "vector": "network",
                "ease": "easy"
            })

    return findings


# ---------------------------------------------------------
# Complete Scan Flow
# ---------------------------------------------------------

def run_full_scan(domain):
    print(f"\n====================")
    print(f"🚀 Full Scan → {domain}")
    print("====================")

    # 1) Subdomains
    subs = subdomain_scan(domain)

    # 2) Live hosts
    live = live_scan(subs)

    # 3) Crawl URLs
    urls = crawl_urls(live)

    # 4) Basic Vuln Scan
    findings = scan_vulns(urls)

    print(f"[DONE] {len(findings)} findings for {domain}")

    return findings
