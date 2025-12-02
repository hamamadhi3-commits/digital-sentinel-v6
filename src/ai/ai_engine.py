import hashlib
from .severity_classifier import classify_severity
from ..poc.poc_builder import build_poc_report

ALREADY_REPORTED_DB = "data/reported_hashes.txt"

def load_reported():
    if not os.path.exists(ALREADY_REPORTED_DB):
        return set()
    with open(ALREADY_REPORTED_DB, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_report_hash(h):
    with open(ALREADY_REPORTED_DB, "a") as f:
        f.write(h + "\n")

def generate_vuln_hash(target, vuln_data):
    base = target + str(vuln_data)
    return hashlib.sha256(base.encode()).hexdigest()

def ai_analyze_vulnerability(target, vuln_data):
    """
    vuln_data = {
        'endpoint': ...,
        'payload': ...,
        'evidence': ...,
        'response': ...,
        'type': ...
    }
    """

    # 1) HASH → Check duplicates
    hashv = generate_vuln_hash(target, vuln_data)
    reported = load_reported()

    if hashv in reported:
        return {
            "duplicate": True,
            "severity": "NONE",
            "report": None
        }

    # 2) CLASSIFY severity
    severity, vrt_category = classify_severity(vuln_data["type"], vuln_data["response"])

    # 3) Build full 6-section report
    full_report = build_poc_report(
        target=target,
        vuln_type=vuln_data["type"],
        endpoint=vuln_data["endpoint"],
        evidence=vuln_data["evidence"],
        payload=vuln_data["payload"],
        vrt=vrt_category,
        severity=severity
    )

    # 4) Save hash
    save_report_hash(hashv)

    return {
        "duplicate": False,
        "severity": severity,
        "vrt": vrt_category,
        "report": full_report
    }
