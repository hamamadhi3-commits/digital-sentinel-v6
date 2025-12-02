# ======================================================================
#  Digital Sentinel - AI Severity Mapper (v1)
#  Auto-severity classification + HackerOne VRT Mapping
#  Built for Themoralhack 🐺🔥
# ======================================================================

import re


class SeverityMapper:

    # ==================================================================
    # 1 - Machine-Learned Keyword Patterns
    # ==================================================================
    PATTERNS = {
        "CRITICAL": [
            r"remote code execution",
            r"rce",
            r"full compromise",
            r"unauthorized server access",
            r"database overwrite",
            r"account takeover",
            r"root access",
            r"critical misconfiguration"
        ],
        "HIGH": [
            r"sql injection",
            r"sqli",
            r"idor",
            r"broken access control",
            r"authentication bypass",
            r"password reset flaw",
            r"ssrf",
            r"xxe",
            r"privilege escalation",
        ],
        "MEDIUM": [
            r"xss",
            r"csrf",
            r"token leak",
            r"cors misconfiguration",
            r"directory listing",
            r"error stack leak"
        ],
        "LOW": [
            r"open redirect",
            r"clickjacking",
            r"rate limit",
            r"banner exposure",
            r"server version leak"
        ]
    }

    # ==================================================================
    # 2 - HackerOne VRT Mapping
    # ==================================================================
    VRT_MAP = {
        "rce": "Server-Side Injection → Remote Code Execution",
        "sql injection": "Server-Side Injection → SQL Injection",
        "idor": "Broken Access Control → Insecure Direct Object Reference",
        "ssrf": "Server-Side Request Forgery",
        "xxe": "XML External Entity",
        "xss": "Client-Side → Cross-Site Scripting",
        "csrf": "Client-Side → CSRF",
        "open redirect": "Client-Side → Open Redirect",
        "cors": "Server Misconfiguration → CORS Misconfig",
        "rate limit": "Insufficient Rate Limiting",
        "clickjacking": "UI Redressing → Clickjacking",
        "directory listing": "Information Disclosure → Directory Listing",
        "token leak": "Information Disclosure → Sensitive Token Leak",
        "server version leak": "Information Disclosure → Server Version"
    }

    # ==================================================================
    # 3 - Detect Severity from Description
    # ==================================================================
    def detect_severity(self, text: str) -> str:
        text = text.lower()

        for level, patterns in self.PATTERNS.items():
            for p in patterns:
                if re.search(p, text):
                    return level
        return "LOW"

    # ==================================================================
    # 4 - Auto-map to HackerOne VRT
    # ==================================================================
    def map_vrt(self, text: str) -> str:
        t = text.lower()

        for key, value in self.VRT_MAP.items():
            if key in t:
                return value
        return "General Vulnerability"

    # ==================================================================
    # 5 - Full Analysis Function (Used by Main Controller)
    # ==================================================================
    def analyze(self, description: str) -> dict:
        severity = self.detect_severity(description)
        vrt = self.map_vrt(description)

        return {
            "severity": severity,
            "vrt": vrt
        }


# ======================================================================
# END OF FILE
# ======================================================================
