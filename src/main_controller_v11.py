import time
import random
from datetime import datetime
from src.overlord_commander import simulate_command_cycle
from src.discord_notify import send_discord_report

MAX_RUNTIME = 60 * 20  # 20 minutes internal kill switch

def main_cycle():
    """
    Executes the autonomous orchestration of reconnaissance, detection,
    and reporting subsystems with time-based safety limit.
    """
    start_time = time.time()
    print(f"⚙️ [CYCLE] Neural Dominion Mode — {datetime.utcnow().isoformat()} UTC")

    targets = ["tesla.com", "apple.com", "microsoft.com", "google.com", "amazon.com", "samsung.com"]
    iteration = 0

    while True:
        iteration += 1
        print(f"🔁 Cycle iteration #{iteration}")
        simulate_command_cycle(targets)
        time.sleep(random.randint(3, 6))  # Simulated idle time

        # Time kill-switch (20 min internal)
        if time.time() - start_time > MAX_RUNTIME:
            print("⏳ Sentinel cycle timed out gracefully after 20 minutes.")
            send_discord_report(
                "Neural Cycle Timeout",
                "⏱️ Sentinel main controller ended gracefully after max runtime (20min).",
                color=0xFFA500
            )
            break

    print("✅ Main Controller finished successfully.")


if __name__ == "__main__":
    try:
        main_cycle()
    except KeyboardInterrupt:
        print("🛑 Sentinel main cycle interrupted manually.")
    except Exception as e:
        print(f"💥 Main Controller Exception: {e}")
        send_discord_report("Main Controller Error", str(e), color=0xE74C3C)
