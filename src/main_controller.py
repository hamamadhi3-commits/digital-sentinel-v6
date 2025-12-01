import time, os, subprocess, json

MODULES = [
    "scope_fetcher.py",
    "recon_engine_parallel.py",
    "ai_vuln_detector.py",
    "duplication_checker.py",
    "auto_report_compose.py",
    "discord_notify.py"
]

def run_cycle():
    print("🚀 Digital Sentinel v6.0 – Autonomous Cycle Started")
    for module in MODULES:
        print(f"▶️ Running {module}")
        subprocess.run(["python3", f"src/{module}"])
    print("✅ Cycle Completed – Sleeping before next run")

if __name__ == "__main__":
    while True:
        run_cycle()
        time.sleep(600)   # 10 daqiqe interval
