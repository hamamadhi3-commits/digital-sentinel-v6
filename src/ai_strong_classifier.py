# =============================
# AI Strong Classifier v1.0
# Digital Sentinel 100× Engine
# =============================

import json
import random

SEVERITY_KEYWORDS = {
    "critical": ["rce", "remote code", "takeover", "admin", "root", "credential leak", "database dump"],
    "high": ["sqli", "xss", "open redirect", "idor", "authentication bypass"],
    "medium": ["csrf", "information disclosure", "header misconfig", "weak token"],
}

def ai_strong_classify(finding):
    """
    Classifies vulnerabilities into CRITICAL / HIGH / MEDIUM
    based on keywords + simulated AI model.
    """

    text = (finding.get("details", "") + " " + finding.get("title", "")).lower()

    # CRITICAL
    for kw in SEVERITY_KEYWORDS["critical"]:
        if kw in text:
            finding["severity"] = "CRITICAL"
            finding["cvss"] = 9.5
            return finding

    # HIGH
    for kw in SEVERITY_KEYWORDS["high"]:
        if kw in text:
            finding["severity"] = "HIGH"
            finding["cvss"] = 7.5
            return finding

    # MEDIUM
    for kw in SEVERITY_KEYWORDS["medium"]:
        if kw in text:
            finding["severity"] = "MEDIUM"
            finding["cvss"] = 5.5
            return finding

    # fallback
    finding["severity"] = "LOW"
    finding["cvss"] = 2.0
    return finding
