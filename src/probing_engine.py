# ============================================================
# Digital Sentinel - HTTP Probing Engine
# ============================================================

import random

def run_probing(subdomains):
    """
    Simulate HTTP probing to check which subdomains are alive.
    """
    print("[PROBE] Probing discovered subdomains for live hosts...")

    alive = []
    for s in subdomains:
        # Simulate that half of subdomains are alive
        if random.random() > 0.4:
            alive.append(s)

    print(f"[PROBE] {len(alive)} alive hosts detected out of {len(subdomains)}.")
    return alive
