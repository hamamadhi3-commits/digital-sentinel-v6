import os
import json
import time
import requests
import concurrent.futures
from datetime import datetime

# === CONFIGURATION ===
TARGETS_FILE = "data/targets.txt"      # لیستی کۆمپانیاکان (بیشتر لە 500 تاقی‌کراوە)
REPORT_FILE = "data/reports/last_summary.json"
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

SCAN_TIMEOUT = 10                      # خاڵی ماوەی هر شیکاربەندی
MAX_WORKERS = 10                       # Parallel threads

# === SEVERITY LEVEL MAP ===
SEVERITY_LEVELS = {
    "critical": 5,
    "high": 4,
    "medium": 3,
    "low": 2,
    "info": 1
}

# === BASIC CHECKS ===
def basic_scan(target):
    """Perform lightweight reconnaissance scan on target."""
    try:
        start = time.time()
        resp = requests.get(f"https://{target}", timeout=SCAN_TIMEOUT)
        duration = round(time.time() - start, 2)

        data = {
            "target": target,
            "status_code": resp.status_code,
            "response_time": duration,
            "server": resp.headers.get("Server", "Unknown"),
            "content_length": len(resp.text),
        }

        # === anomaly detector (simplified logic) ===
        vulns = []
        if "x-powered-by" in resp.headers and "php" in resp.headers["x-powered-by"].lower():
            vulns.append({
                "type": "Information Disclosure",
                "severity": "low",
                "description": "Leaking backend technology in response headers."
            })

        if "admin" in resp.text.lower() and "login" in resp.text.lower():
            vulns.append({
                "type": "Potential Admin Portal",
                "severity": "medium",
                "description": "Page contains admin/login keywords."
            })

        if "sql" in resp.text.lower() or "error in your sql syntax" in resp.text.lower():
            vulns.append({
                "type": "SQLi Indicator",
                "severity": "high",
                "description": "SQL syntax error detected in output."
            })

        return {"target": target, "data": data, "vulns": vulns}

    except requests.exceptions.Timeout:
        return {"target": target, "error": "Timeout"}
    except Exception as e:
        return {"target": target, "error": str(e)}


# === PARALLEL EXECUTION ===
def run_parallel_scans(targets):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(basic_scan, t): t for t in targets}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results


# === REPORT GENERATOR ===
def generate_summary(scan_results):
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "targets_scanned": len(scan_results),
        "vulns_found": 0,
        "high_severity": 0,
        "critical_severity": 0,
        "details": []
    }

    for result in scan_results:
        if "vulns" in result:
            for v in result["vulns"]:
                summary["vulns_found"] += 1
                if v["severity"] == "high":
                    summary["high_severity"] += 1
                if v["severity"] == "critical":
                    summary["critical_severity"] += 1

                summary["details"].append({
                    "target": result["target"],
                    "type": v["type"],
                    "severity": v["severity"],
                    "description": v["description"]
                })

    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    print(f"✅ Report saved → {REPORT_FILE}")
    return summary


# === DISCORD NOTIFICATION ===
def send_discord_report(summary):
    if not DISCORD_WEBHOOK:
        print("⚠️ Discord webhook not found.")
        return

    embed = {
        "title": "📊 Digital Sentinel – Autonomous Recon Summary",
        "color": 0x3498DB,
        "timestamp": summary["timestamp"],
        "fields": [
            {"name": "🛰️ Targets Scanned", "value": str(summary["targets_scanned"]), "inline": True},
            {"name": "🧠 Vulns Found", "value": str(summary["vulns_found"]), "inline": True},
            {"name": "🔥 High Severity", "value": str(summary["high_severity"]), "inline": True},
            {"name": "💀 Critical", "value": str(summary["critical_severity"]), "inline": True}
        ],
        "footer": {"text": "Digital Sentinel v11 • Eternal Hunter"}
    }

    payload = {"embeds": [embed]}

    try:
        r = requests.post(DISCORD_WEBHOOK, json=payload)
        if r.status_code in [200, 204]:
            print("📡 Report sent successfully to Discord.")
        else:
            print(f"⚠️ Discord error: {r.status_code} {r.text}")
    except Exception as e:
        print(f"💥 Discord send failed: {e}")


# === MAIN EXECUTION ===
if __name__ == "__main__":
    print("🚀 Launching Sentinel Eternal Hunter v11")
    if not os.path.exists(TARGETS_FILE):
        print(f"❌ No targets file found → {TARGETS_FILE}")
        exit(1)

    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip()]

    print(f"🎯 Loaded {len(targets)} targets.")
    print("🕵️ Starting autonomous scanning...")

    results = run_parallel_scans(targets)
    summary = generate_summary(results)
    send_discord_report(summary)

    print("✅ Hunter cycle completed.")
