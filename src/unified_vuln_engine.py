import json, os, time
from datetime import datetime

from recon.passive_recon import passive_recon
from recon.deep_crawler import deep_crawl
from recon.active_recon import active_recon
from recon.fingerprint import fingerprint
from modules.shadow_recon import shadow_recon
from modules.mobile_api_recon import mobile_api_recon
from modules.auto_chain_exploit import chain_exploit
from ai.zeroday_predictor import predict_zeroday

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

DISCORD = os.getenv("DISCORD_WEBHOOK_URL")
TARGET_FILE = "data/targets/global_500_targets.txt"
SAVE_FILE = "data/state/resume.json"
REPORT_DIR = "data/reports"
LOG = "data/logs/unified.log"

os.makedirs("data/state", exist_ok=True)
os.makedirs("data/logs", exist_ok=True)
os.makedirs("data/reports", exist_ok=True)

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------

def log(x):
    t = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a") as f:
        f.write(f"[{t}] {x}\n")
    print(x)

def save_progress(idx):
    with open(SAVE_FILE, "w") as f:
        json.dump({"idx": idx}, f)

def load_progress():
    if not os.path.exists(SAVE_FILE):
        return 0
    try:
        return json.load(open(SAVE_FILE))["idx"]
    except:
        return 0

def send_discord(msg):
    if not DISCORD:
        return
    import requests
    try:
        requests.post(DISCORD, json={"content": msg}, timeout=10)
    except:
        pass

# ---------------------------------------------------
# MAIN ENGINE
# ---------------------------------------------------

def scan_target(domain):

    log(f"🔍 SCANNING → {domain}")

    output = {
        "domain": domain,
        "time": datetime.utcnow().isoformat(),
        "findings": []
    }

    # Passive
    p = passive_recon(domain)
    output["passive"] = p

    # Active
    a = active_recon(domain)
    output["active"] = a

    # Crawler
    urls = deep_crawl(domain)
    output["urls"] = urls

    # Shadow
    shadow = shadow_recon(domain)
    output["shadow"] = shadow

    # Mobile
    mobile = mobile_api_recon(domain)
    output["mobile"] = mobile

    # Fingerprint
    fp = fingerprint(a.get("httpx", ""))

    # Simulated nuclei
    findings = []
    for u in urls[:40]:
        if "admin" in u or "login" in u:
            findings.append({
                "url": u,
                "type": "auth-bypass",
                "severity": "HIGH",
                "raw": "login page possible bypass"
            })
        if "api" in u:
            findings.append({
                "url": u,
                "type": "idor",
                "severity": "MEDIUM",
                "raw": "parameter exposure"
            })

    # AI Zero-day predictor
    for f in findings:
        sev, desc = predict_zeroday(f["type"], f["raw"])
        if sev != "NONE":
            f["ai_severity"] = sev
            f["ai_note"] = desc

    # Chain exploit
    c = chain_exploit(findings)
    if c["chain"]:
        findings.append({
            "url": domain,
            "type": "exploit-chain",
            "severity": c["severity"],
            "details": c["description"]
        })

    # Filter CRITICAL / HIGH / MEDIUM
    filtered = [f for f in findings if f["severity"] in ["CRITICAL", "HIGH", "MEDIUM"]]

    output["findings"] = filtered

    # Save report
    fname = f"{REPORT_DIR}/{domain.replace('.', '_')}.json"
    json.dump(output, open(fname, "w"), indent=2)

    # Discord summary
    if len(filtered) > 0:
        send_discord(f"🚨 Vulnerabilities found in **{domain}** → {len(filtered)}")
    else:
        send_discord(f"✅ No high-value vulns in {domain}")

    return True

# ---------------------------------------------------
# LOOP
# ---------------------------------------------------

def main():

    domains = [x.strip() for x in open(TARGET_FILE) if x.strip()]
    start = load_progress()

    log(f"▶ Resuming from index {start}...")
    for idx in range(start, len(domains)):
        save_progress(idx)
        scan_target(domains[idx])
        time.sleep(1)

    # after finishing → restart stronger
    os.remove(SAVE_FILE)
    send_discord("♻ All targets scanned — restarting cycle stronger.")
    main()


if __name__ == "__main__":
    main()
