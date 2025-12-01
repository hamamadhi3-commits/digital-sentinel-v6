import time, random

def run():
    print("[👁️ Observer Node] Monitoring node health and cycle stability...")
    metrics = {"uptime": 0, "failures": 0}
    for i in range(3):
        time.sleep(1)
        metrics["uptime"] += 1
        if random.random() < 0.1:
            metrics["failures"] += 1
            print("[⚠️ Observer] Node instability detected.")
    print(f"[✅ Observer] Health metrics: {metrics}")
