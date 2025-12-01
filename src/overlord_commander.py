import json
import random
from datetime import datetime
from src.discord_notify import send_discord_report

def allocate_resources(prioritized):
    """
    Allocates computational or network resources based on score thresholds.
    prioritised: list of tuples or lists [(target, score, ...), ...]
    """
    try:
        # Safe unpacking even if tuples have >2 elements
        top = [item[0] for item in prioritized if item[1] > 90]
        mid = [item[0] for item in prioritized if 70 < item[1] <= 90]
        low = [item[0] for item in prioritized if item[1] <= 70]

        print(f"🔹 {len(top)} high-priority targets allocated.")
        print(f"🔸 {len(mid)} medium-priority targets allocated.")
        print(f"⚪ {len(low)} low-priority targets ignored.")

        send_discord_report(
            "Overlord Commander Allocation",
            f"🧠 Resource allocation completed at {datetime.utcnow().isoformat()} UTC.\n"
            f"Top: {len(top)} | Mid: {len(mid)} | Low: {len(low)}",
            color=0x00BFFF
        )
        return {"top": top, "mid": mid, "low": low}

    except Exception as e:
        print(f"💥 Allocation Error: {e}")
        send_discord_report("Overlord Commander Failure", f"💥 Error: {e}", color=0xE74C3C)
        return {"top": [], "mid": [], "low": []}


def simulate_command_cycle(targets):
    """
    Simulate one autonomous command cycle.
    """
    print("🚀 Initiating Overlord Neural Command Cycle...")
    prioritized = [(t, random.randint(50, 100), random.random()) for t in targets]
    allocations = allocate_resources(prioritized)
    print("✅ Overlord cycle finished successfully.")
    return allocations


if __name__ == "__main__":
    sample_targets = ["tesla.com", "apple.com", "microsoft.com", "google.com"]
    simulate_command_cycle(sample_targets)
