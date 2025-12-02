# --------------------------------------------------------------
# Digital Sentinel v15 – Self-Learning Pattern Engine
# Learns from every scan result to improve future bug discovery.
# --------------------------------------------------------------

import json
import os
from collections import defaultdict

BRAIN_FILE = "data/brain.json"


def load_brain():
    """Load previous learning data."""
    if not os.path.exists(BRAIN_FILE):
        return {
            "patterns": {},
            "company_heat": {},
            "url_signatures": {},
            "technology_hotspots": {},
            "history": []
        }

    with open(BRAIN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_brain(brain):
    """Save updated learning data."""
    with open(BRAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(brain, f, indent=4)


def learn(new_findings):
    """
    new_findings = list of dicts from AI engine
    Each finding carries:
    - target
    - severity
    - url
    - technology
    - category
    """
    brain = load_brain()

    for f in new_findings:
        target = f.get("target", "unknown")
        sev = f.get("severity", "unknown").lower()
        url = f.get("url", "")
        tech = f.get("technology", "")
        cat = f.get("category", "")

        # heat-level (ڕادەی گەرمبوون)
        brain["company_heat"][target] = brain["company_heat"].get(target, 0) + (
            5 if sev == "critical" else 3 if sev == "high" else 1
        )

        # URL signatures
        if url:
            sig = url.split("?")[0].replace("https://", "").replace("http://", "")
            brain["url_signatures"][sig] = brain["url_signatures"].get(sig, 0) + 1

        # technology hotspots
        if tech:
            brain["technology_hotspots"][tech] = brain["technology_hotspots"].get(tech, 0) + 1

        # learning patterns
        if cat:
            brain["patterns"][cat] = brain["patterns"].get(cat, 0) + 1

        # register history
        brain["history"].append({
            "target": target,
            "severity": sev,
            "url": url,
            "category": cat
        })

    save_brain(brain)
    return brain


def suggest_priority_targets(limit=10):
    """Return hottest companies sorted by severity history."""
    brain = load_brain()
    heat = brain.get("company_heat", {})

    # sort by heat descending
    sorted_targets = sorted(heat.items(), key=lambda x: x[1], reverse=True)
    return [t[0] for t in sorted_targets[:limit]]


def suggest_hotspot_signatures(limit=10):
    """Return URLs that frequently appear in vulnerabilities."""
    brain = load_brain()
    sigs = brain.get("url_signatures", {})

    sorted_sigs = sorted(sigs.items(), key=lambda x: x[1], reverse=True)
    return [s[0] for s in sorted_sigs[:limit]]


def suggest_hot_technologies(limit=10):
    """Return technologies that frequently have bugs."""
    brain = load_brain()
    techs = brain.get("technology_hotspots", {})

    sorted_tech = sorted(techs.items(), key=lambda x: x[1], reverse=True)
    return [t[0] for t in sorted_tech[:limit]]
