def classify_severity(vuln_type, response):

    vuln_type = vuln_type.lower()

    if "rce" in vuln_type:
        return "CRITICAL", "Server-Side Remote Code Execution"

    if "sql" in vuln_type:
        return "HIGH", "SQL Injection"

    if "xss" in vuln_type:
        if "cookie" in response or "session" in response:
            return "HIGH", "Stored/Reflected XSS"
        return "MEDIUM", "Reflected XSS"

    if "open redirect" in vuln_type:
        return "MEDIUM", "Open Redirect"

    if "idor" in vuln_type or "insecure direct" in vuln_type:
        return "HIGH", "IDOR"

    if "csrf" in vuln_type:
        return "MEDIUM", "CSRF"

    return "LOW", "General Misconfiguration"
