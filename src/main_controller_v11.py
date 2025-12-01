import time
from datetime import datetime
from src.overlord_commander import allocate_resources
from src.neural_node_manager import run_neural_dominion
from src.genesis_engine import run_genesis_cycle
from src.discord_notify import send_discord_alert

# ===============================================================
# DIGITAL SENTINEL v11.0 — NEURAL DOMINION MODE
# ===============================================================

def main_cycle():
    start = datetime.now()
    print(f"\n⚙️ [CYCLE] Neural Dominion Mode — {start}")

    # Phase 1: Allocate resources across distributed nodes
    allocate_resources(["Recon", "Detection", "Reporting", "Observation"])

    # Phase 2: Spawn Neural Nodes in parallel
    run_neural_dominion()

    # Phase 3: Adaptive self-learning cycle
    run_genesis_cycle()

    duration = (datetime.now() - start).total_seconds()
    send_discord_alert(
        "Digital Sentinel v11.0 — Neural Dominion Cycle",
        f"Cycle Duration: {duration:.2f}s\nDominion Active: All Nodes Synced."
    )
    print(f"🏁 Cycle completed in {duration:.2f}s\n")

if __name__ == "__main__":
    while True:
        main_cycle()
        time.sleep(900)
