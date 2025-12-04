# ============================================================
# Digital Sentinel v6 - Probing Engine
# Author: Themoralhack & Manus AI
# Mission: Validate live domains, collect headers and responses
# ============================================================

import concurrent.futures
import requests
import time

def probe_single_target(target):
    """Probes a single target via HTTP(S) and returns status info."""
    protocols = ["https://", "http://"]
    result = {
        "target": target,
        "status": "dead",
        "live_url": None,
        "response_time": None,
        "code": None,
    }

    for proto in protocols:
        url = f"{proto}{target}"
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            elapsed = round(time.time() - start, 2)

            result.update({
                "status": "alive",
                "live_url": url,
                "code": response.status_code,
                "response_time": elapsed
            })
            return result
        except Exception:
            continue
    return result


def run_probing_batch(targets):
    """Runs concurrent HTTP probing across all targets."""
    print(f"[🌐] Starting HTTP probing for {len(targets)} targets...")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_target = {executor.submit(probe_single_target, t): t for t in targets}

        for future in concurrent.futures.as_completed(future_to_target):
            target = future_to_target[future]
            try:
                data = future.result()
                results.append(data)
                status = "✅" if data["status"] == "alive" else "❌"
                print(f"{status} {target}")
            except Exception as e:
                print(f"[⚠️] Probing error for {target}: {e}")

    print(f"[🔎] Probing completed. {len([r for r in results if r['status']=='alive'])} live targets found.")
    return results
