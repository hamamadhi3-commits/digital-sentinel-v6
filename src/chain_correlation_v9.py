# Digital Sentinel v9 – Multi-Finding Exploit Chain Correlator
# -------------------------------------------------------------

def group_findings_by_domain(findings):
    """Group findings per domain."""
    grouped = {}
    for f in findings:
        dom = f.get("domain", "unknown")
        grouped.setdefault(dom, []).append(f)
    return grouped


def detect_chain(findings_for_domain):
    """
    Detect if multiple findings combine into a stronger exploit-chain.
    Example:
      - XSS + Path Disclosure + Debug Endpoint → Account Takeover
      - SQLi + File Upload → RCE
      - IDOR + Admin Panel Exposure → Privilege Escalation
    """

    titles = " ".join([f["summary"].lower() for f in findings_for_domain])

    chain = {
        "has_chain": False,
        "type": None,
        "severity": None,
        "score": None,
        "reward": None,
        "steps": []
    }

    # -----------------------
    # 1) XSS → Session Steal → Account Takeover
    # -----------------------
    if "xss" in titles and "cookie" in titles:
        chain["has_chain"] = True
        chain["type"] = "Account Takeover Chain"
        chain["severity"] = "HIGH"
        chain["score"] = 8.7
        chain["reward"] = "$1,000 – $5,000"
        chain["steps"] = [
            "Inject malicious JS (XSS)",
            "Steal user cookies",
            "Reuse stolen cookie",
            "Log in as victim (Account Takeover)"
        ]
        return chain

    # -----------------------
    # 2) SQLi + File Upload → Remote Code Execution (RCE)
    # -----------------------
    if "sql" in titles and "upload" in titles:
        chain["has_chain"] = True
        chain["type"] = "SQL Injection → File Upload → RCE"
        chain["severity"] = "CRITICAL"
        chain["score"] = 9.8
        chain["reward"] = "$3,000 – $20,000"
        chain["steps"] = [
            "Exploit SQLi to enumerate system paths",
            "Upload malicious payload",
            "Execute payload → Achieve RCE"
        ]
        return chain

    # -----------------------
    # 3) IDOR + Admin Panel = Privilege Escalation
    # -----------------------
    if "idor" in titles and "admin" in titles:
        chain["has_chain"] = True
        chain["type"] = "IDOR + Admin Panel Exposure"
        chain["severity"] = "HIGH"
        chain["score"] = 8.5
        chain["reward"] = "$1,500 – $6,000"
        chain["steps"] = [
            "Exploit IDOR",
            "Access admin resources",
            "Modify or elevate role",
            "Full account takeover"
        ]
        return chain

    return chain


def analyze_chains(all_findings):
    """Take all findings → return list of valid exploit chains."""
    results = []
    grouped = group_findings_by_domain(all_findings)

    for domain, fs in grouped.items():
        chain = detect_chain(fs)
        if chain["has_chain"]:
            results.append({"domain": domain, **chain})

    return results
