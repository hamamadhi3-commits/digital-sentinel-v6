def predict_zeroday(vuln_type, response_body):

    resp = response_body.lower()
    vt = vuln_type.lower()

    # SSRF detection
    if "aws" in resp or "169.254" in resp or "metadata" in resp:
        return "CRITICAL", "Possible SSRF → Cloud Takeover"

    # SQLi blind indicators
    if "syntax" in resp or "mysql" in resp or "unexpected" in resp:
        return "HIGH", "Blind SQL Injection Pattern"

    # RCE pattern
    if "uid=" in resp or "root" in resp or "command not found" in resp:
        return "CRITICAL", "Possible Remote Code Execution"

    # OAuth misconfig
    if "oauth" in resp and "redirect" in resp:
        return "HIGH", "OAuth Misconfiguration"

    # CORS Misconfig
    if "access-control-allow-origin" in resp:
        return "MEDIUM", "CORS Misconfiguration"

    return "NONE", "No 0-day Indicators"
