# ---------------------------------------------------------
# Digital Sentinel Quantum — Main Controller v11.2 (DEBUG)
# ---------------------------------------------------------
# ✅ Purpose:
# Safe, one-cycle execution of the entire quantum + AI chain
# with debug visibility and live output flushing for GitHub Actions.
# ---------------------------------------------------------

import sys
import time
import traceback
from ai_chain_orchestrator import AIChainOrchestrator
from quantum_awareness_engine import QuantumAwarenessEngine

# ---------------------------------------------------------
# 🔧 Global stdout flush settings for live logs
# ---------------------------------------------------------
sys.stdout.reconfigure(line_buffering=True)

# ---------------------------------------------------------
# 🧩 Logging helper
# ---------------------------------------------------------
def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"[MAIN-CONTROLLER {timestamp}] {msg}", flush=True)

# ---------------------------------------------------------
# 🚀 Main Controller
# ---------------------------------------------------------
def run_main_controller():
    log("🚀 Sentinel Quantum Main Controller started (v11.2-debug).")
    start_time = time.time()

    try:
        # STEP 1: Initialize Quantum Awareness Engine
        log("🌌 STEP 1: Initializing Quantum Awareness Engine...")
        quantum = QuantumAwarenessEngine(max_agents=5)
        log("🌌 STEP 1.1: Running quantum cycle...")
        quantum.run_quantum_cycle()
        log("✅ STEP 1 complete: Quantum awareness phase done.")

        # STEP 2: Launch AI Chain Orchestrator for higher intelligence
        log("🧠 STEP 2: Launching AI Chain Orchestrator (single cycle mode)...")
        orchestrator = AIChainOrchestrator(quantum_agents=5, scan_interval=60)
        orchestrator.run_cycle()
        log("✅ STEP 2 complete: AI Chain Orchestrator finished one cycle.")

        # STEP 3: Wrap-up and save results
        log("🗂 STEP 3: Final wrap-up and data persistence.")
        duration = round(time.time() - start_time, 2)
        log(f"⏱ Execution time: {duration} seconds.")
        log("✅ Sentinel Quantum Main Controller completed successfully.")

    except Exception as e:
        log(f"❌ CRITICAL ERROR in Main Controller: {e}")
        traceback.print_exc()
        sys.exit(1)

    finally:
        log("🧩 Debug session finished. Exiting cleanly.")
        sys.exit(0)


# ---------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------
if __name__ == "__main__":
    run_main_controller()
