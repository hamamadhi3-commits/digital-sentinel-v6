import concurrent.futures, os, json, subprocess

INPUT = "data/targets/active_scopes.json"
OUTPUT_DIR = "data/reports/recon_raw"

def probe(domain):
    print(f"🌐 Probing {domain}")
    try:
        res = subprocess.run(["curl", "-I", "--max-time", "5", f"https://{domain}"],
                             capture_output=True, text=True)
        return {"domain": domain, "headers": res.stdout}
    except Exception as e:
        return {"domain": domain, "error": str(e)}

def run_recon():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    scopes = json.load(open(INPUT))
    targets = [d for s in scopes for d in s["domains"]]

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        results = list(ex.map(probe, targets))

    json.dump(results, open(f"{OUTPUT_DIR}/recon_result.json", "w"), indent=2)
    print(f"✅ Recon completed for {len(results)} domains")

if __name__ == "__main__":
    run_recon()
