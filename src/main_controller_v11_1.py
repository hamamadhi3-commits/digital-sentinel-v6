import os
import time
from datetime import datetime

CYCLE_TIMEOUT = 1200
REPORT_DIR = "data/reports"
LOG_DIR = "data/logs"

print("🚀 Digital Sentinel v11.1 – Main Controller Starting...")

# 🧠 FIX: remove file if it's blocking folder creation
for d in [REPORT_DIR, LOG_DIR]:
    if os.path.exists(d) and not os.path.isdir(d):
        os.remove(d)
    os.makedirs(d, exist_ok=True)

cycle_counter = 0
start_time = datetime.now()

while True:
    cycle_counter += 1
    print(f"\n🌀 Cycle iteration #{cycle_counter}")
    print("🚀 Initiating Overlord Neural Command Cycle...")

    high_priority = cycle_counter % 3
    medium_priority = (cycle_counter + 1) % 4
    low_priority = (cycle_counter + 2) % 5

    print(f"🔹 {high_priority} high-priority targets allocated.")
    print(f"🔸 {medium_priority} medium-priority targets allocated.")
    print(f"⚪ {low_priority} low-priority targets ignored.")

    log_file = os.path.join(LOG_DIR, f"cycle_{cycle_counter}.log")
    with open(log_file, "w") as f:
        f.write(f"[{datetime.now()}] Cycle {cycle_counter} finished successfully.\n")

    print("✅ Overlord cycle finished successfully.")

    if (datetime.now() - start_time).total_seconds() > CYCLE_TIMEOUT:
        print("⏳ Sentinel cycle timed out gracefully after 20 minutes.")
        break

    time.sleep(3)

print("✅ Main Controller finished successfully.")
