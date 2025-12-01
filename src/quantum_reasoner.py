import json
import random
from datetime import datetime

THREAT_FEED = "data/sentinel_threat_feed.json"
MEMORY_FILE = "data/sentinel_memory.json"

def load_json(path):
    try:
        return json.load(open(path))
    except Exception:
        return {}

def correlate_threats(threat_feed, last_targets):
    """Reason over feed & targets to produce cognitive risk predictions."""
    correlations = []
    for t in last_targets:
        matched = []
        for cve in threat_feed.get("cve_feed", []):
            if any(x in t.lower() for x in ["api", "auth", "login", "cloud", "admin"]) and cve["cvss"] >= 7:
                matched.append(cve)
        if matched:
            correlations.append({
                "target": t,
                "related_cves": [m["id"] for m in matched],
                "risk_score": round(sum([m["cvss"] for m in matched])/len(matched), 2)
            })
    return correlations

def generate_reasoning_summary(correlations):
    """Simulate quantum cognitive analysis narrative."""
    now = datetime.utcnow().isoformat()
    summary = {
        "timestamp": now,
        "cycle_thoughts": []
    }
    for item in correlations:
        thought = (
            f"Target {item['target']} shows correlation with {len(item['related_cves'])} high-CVSS CVEs. "
            f"Average risk score {item['risk_score']}. Recommend priority scan depth increase."
        )
        summary["cycle_thoughts"].append(thought)
    json.dump(summary, open("data/quantum_reasoning_log.json", "w"), indent=2)
    return summary

def run_quantum_reasoning():
    """Main reasoning engine entrypoint."""
    feed = load_json(THREAT_FEED)
    mem = load_json(MEMORY_FILE)
    last_targets = mem.get("last_targets", [])
    cor = correlate_threats(feed, last_targets)
    result = generate_reasoning_summary(cor)
    print(f"[🧠 Quantum Reasoning] Generated {len(result['cycle_thoughts'])} reasoning entries.")
    return result
