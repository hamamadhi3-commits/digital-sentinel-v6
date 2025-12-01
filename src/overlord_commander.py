import random
import json
from datetime import datetime

MEMORY_FILE = "data/sentinel_memory.json"

def load_memory():
    try:
        return json.load(open(MEMORY_FILE))
    except Exception:
        return {"runs": 0, "failures": 0, "last_targets": []}

def prioritize_targets(targets):
    """Assign a dynamic priority score to each target."""
    prioritized = []
    for t in targets:
        score = random.randint(50, 100)
        if any(x in t.lower() for x in ["bank", "cloud", "api", "login", "admin"]):
            score += 20
        prioritized.append((t, min(score, 100)))
    prioritized.sort(key=lambda x: x[1], reverse=True)
    return prioritized

def allocate_resources(prioritized):
    """Divide targets into 3 dynamic clusters based on risk."""
    top = [t for t, s in prioritized if s > 90]
    medium = [t for t, s in prioritized if 70 < s <= 90]
    low = [t for t, s in prioritized if s <= 70]
    print(f"🔱 Allocated → High:{len(top)} Medium:{len(medium)} Low:{len(low)}")
    return {"high": top, "medium": medium, "low": low}

def generate_overlord_report(prioritized):
    """Summarize the Overlord decision process."""
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": f"Total targets ranked: {len(prioritized)}",
        "top_targets": prioritized[:10],
    }
    json.dump(report, open("data/overlord_decision_log.json", "w"), indent=2)
    print(f"🧠 Overlord Decision Summary generated → {len(prioritized)} targets ranked.")
    return report
