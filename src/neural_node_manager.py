import concurrent.futures, importlib, time
from datetime import datetime

NODE_MAP = {
    "recon": "src.node_recon",
    "detector": "src.node_detector",
    "reporter": "src.node_reporter",
    "observer": "src.node_observer"
}

def load_module(path):
    return importlib.import_module(path)

def run_node(name, func="run"):
    mod = load_module(NODE_MAP[name])
    if hasattr(mod, func):
        print(f"[🧩 Node] {name} node starting...")
        getattr(mod, func)()
    else:
        print(f"[⚠️ Node] {name} node missing function {func}")

def run_neural_dominion():
    print(f"\n🧠 [NEURAL DOMINION] Activated at {datetime.utcnow().isoformat()}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as exe:
        for node in NODE_MAP.keys():
            exe.submit(run_node, node)
    time.sleep(2)
    print("[✅] All nodes synchronized and running in parallel.")
