import concurrent.futures
import os
import time
from sentinel_scan_engine import run_full_scan
from ai_priority import analyze_vulnerability
from chain_detector import detect_exploit_chains
from sentinel_discord_reporter import send_finding_report, send_chain_report

TARGET_FILE = "data/targets/global_500_targets.txt"

def load_targets():
    with open(TARGET_FILE, "r") as f:
        return [l.strip() for l in f if l.strip()]

def worker_job(domain):
    res = run_full_scan(domain)
    if not res:
        return []

    enhanced = [analyze_vulnerability(f, domain) for f in res]

    for f in enhanced:
        if f["cvss"] >= 5:
            send_finding_report(f)

    return enhanced

def parallel_master():
    targets = load_targets()

    chunks = [targets[i::10] for i in range(10)]  # 10 workers
    all_findings = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as exe:
        futures = []
        for part in chunks:
            futures.append(exe.submit(run_batch, part))

        for f in concurrent.futures.as_completed(futures):
            all_findings.extend(f.result())

    chains = detect_exploit_chains(all_findings)
    for c in chains:
        send_chain_report(c)

def run_batch(domains):
    findings = []
    for d in domains:
        findings.extend(worker_job(d))
    return findings
