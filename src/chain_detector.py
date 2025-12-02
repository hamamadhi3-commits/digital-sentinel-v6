# Digital Sentinel v9 – Chain Detector Bridge
# -------------------------------------------

from chain_correlation_v9 import analyze_chains

def detect_exploit_chains(findings):
    """
    findings = list of vulnerabilities already passed through:
       - ai_priority.py
       - main_controller
    """
    return analyze_chains(findings)
