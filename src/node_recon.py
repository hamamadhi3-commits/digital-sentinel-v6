from src.recon_engine_parallel import run_recon_cycle

def run():
    print("[🌐 Recon Node] Scanning top-tier targets...")
    sample_targets = ["tesla.com", "apple.com", "microsoft.com"]
    run_recon_cycle(sample_targets)
