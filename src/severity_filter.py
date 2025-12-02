# -----------------------------------------------------------
# Digital Sentinel v14 – Critical/High Filter Engine
# Filters AI findings and only keeps:
#   - CRITICAL
#   - HIGH
#
# Everything else is ignored.
# -----------------------------------------------------------

VALID = ["critical", "high", "severity_critical", "severity_high"]


def is_severe(finding):
    """
    finding example:
    {
        "severity": "high",
        "summary": "...",
        "target": "...",
        ...
    }
    """
    if not finding:
        return False

    sev = str(finding.get("severity", "")).lower().strip()

    return sev in VALID


def filter_findings(findings):
    """
    Remove MEDIUM / LOW / INFO
    Return only HIGH + CRITICAL
    """
    final = []
    for f in findings:
        if is_severe(f):
            final.append(f)

    return final
