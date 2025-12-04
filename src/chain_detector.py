# =====================================================
# Digital Sentinel v11.3 - Exploit Chain Detector
# =====================================================
from itertools import combinations

def detect_exploit_chains(findings):
    """
    Detects logical chains of vulnerabilities across multiple targets.
    Example: XSS + exposed admin panel + weak token = exploit chain.
    """
    if not findings:
        return []

    chains = []
    high_risk = [f for f in findings if f.get("severity") in ["HIGH", "CRITICAL"]]

    for a, b in combinations(high_risk, 2):
        if _is_chain_linked(a, b):
            chain = {
                "chain_name": f"{a['title']} → {b['title']}",
                "domains": list(set([a["domain"], b["domain"]])),
                "combined_risk": _calculate_chain_score(a, b),
                "elements": [a, b]
            }
            chains.append(chain)

    return sorted(chains, key=lambda c: c["combined_risk"], reverse=True)


def _is_chain_linked(a, b):
    """
    Determines if two findings can be linked logically (basic heuristic).
    """
    domain_match = a["domain"].split(".")[-2:] == b["domain"].split(".")[-2:]
    return domain_match and abs(a["cvss"] - b["cvss"]) < 3


def _calculate_chain_score(a, b):
    """
    Combines two findings’ risk into a single chain score.
    """
    return round((a["cvss"] + b["cvss"]) * (a["exploit_probability"] + b["exploit_probability"]) / 2, 2)
