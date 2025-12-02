# -------------------------------------------------
# Digital Sentinel v8.0 — AI Priority & CVSS Engine
# -------------------------------------------------

import math
import random

# ------------------------------
#  CVSS BASE METRIC CALCULATOR
# ------------------------------

def calculate_cvss(finding):
    """
    Make rough CVSS score automatically based on attributes of the finding.
    """

    impact = finding.get("impact", "medium")
    attack_vector = finding.get("vector", "network")
    ease = finding.get("ease", "medium")

    # Score impact
    if impact == "critical":
        impact_score = 9.5
    elif impact == "high":
        impact_score = 7.5
    elif impact == "medium":
        impact_score = 5.5
    else:
        impact_score = 3.0

    # Score attack vector
    if attack_vector == "network":
        vector_score = 1.0
    elif attack_vector == "adjacent":
        vector_score = 0.8
    elif attack_vector == "local":
        vector_score = 0.6
    else:
        vector_score = 0.4

    # Score exploitation ease
    if ease == "easy":
        exploit_score = 1.0
    elif ease == "medium":
        exploit_score = 0.7
    else:
        exploit_score = 0.4

    # Combine
    cvss = (impact_score * vector_score) * exploit_score

    # Normalize to 0 - 10
    cvss = max(0, min(cvss, 10))
    return round(cvss, 1)


# ------------------------------
# VRT CATEGORY (Bugcrowd VRT)
# ------------------------------
def classify_vrt(finding):
    """
    Auto classify into Bugcrowd VRT category
    """

    title = finding.get("summary", "").lower()

    if "rce" in title or "remote code" in title:
        return "Server-Side Injection → RCE"
    if "sql" in title:
        return "Server-Side Injection → SQLi"
    if "xss" in title:
        return "Client-Side Injection → XSS"
    if "auth" in title or "login" in title or "bypass" in title:
        return "Broken Authentication"
    if "id" in title or "oid" in title or "user id" in title:
        return "IDOR → Broken Access Control"
    if "csrf" in title:
        return "CSRF"
    if "upload" in title:
        return "File Upload → Arbitrary File Write"
    if "config" in title:
        return "Misconfiguration → Sensitive Data"

    return "Uncategorized / Needs Review"


# ------------------------------
# REWARD PREDICTION
# ------------------------------
def predict_reward(cvss):
    """
    Estimate reward based on typical Bugcrowd / HackerOne payouts.
    """

    if cvss >= 9:
        return "$2,500 – $10,000"
    if cvss >= 7:
        return "$750 – $2,500"
    if cvss >= 5:
        return "$150 – $750"
    if cvss >= 3:
        return "$50 – $150"
    return "$0 – $50"


# ------------------------------
# PRIORITY SCORE (0–100)
# ------------------------------
def priority_score(cvss, vrt_category):
    base = cvss * 8

    if "RCE" in vrt_category:
        base += 25
    elif "SQL" in vrt_category:
        base += 15
    elif "XSS" in vrt_category:
        base += 10
    elif "Authentication" in vrt_category:
        base += 12

    return min(100, base)


# ------------------------------
# FULL AI ANALYSIS
# ------------------------------

def analyze_vulnerability(finding, domain):
    cvss = calculate_cvss(finding)
    vrt = classify_vrt(finding)
    reward = predict_reward(cvss)
    prio = priority_score(cvss, vrt)

    return {
        "domain": domain,
        "summary": finding.get("summary", "Untitled"),
        "cvss": cvss,
        "vrt": vrt,
        "reward_prediction": reward,
        "priority_score": prio
    }
