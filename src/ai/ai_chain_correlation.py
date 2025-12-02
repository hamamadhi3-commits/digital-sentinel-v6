# ======================================================================
#  Digital Sentinel - AI Chain Correlation Engine (v1)
#  Zero-day signal detection + multi-scan fusion + threat linking
#  Built exclusively for Themoralhack 🐺🔥
# ======================================================================

import re
from typing import List, Dict


class AIChainCorrelation:

    # ==================================================================
    # 1 — Zero-Day Indicators (AI rules)
    # ==================================================================
    ZERO_DAY_PATTERNS = [
        r"unknown parameter",
        r"unexpected response",
        r"stacktrace",
        r"debug enabled",
        r"exposed dev endpoint",
        r"internal ip leak",
        r"proto mismatch",
        r"weird redirect",
        r"token not required",
        r"authentication skipped",
    ]

    # ==================================================================
    # 2 — High-Value Correlation Rules
    # ==================================================================
    CORRELATIONS = [
        ("idor", "rate limit", "Potential Account Takeover"),
        ("xss", "csrf", "Stored-XSS Worm Propagation"),
        ("sqli", "error leak", "Database Structure Exposure"),
        ("ssrf", "internal ip", "Internal Network Pivoting"),
        ("file upload", "path traversal", "RCE Vector via Upload"),
        ("token leak", "admin panel", "Admin Hijack Through Token"),
        ("misconfig", "debug", "Production Debug Mode Exposure")
    ]

    # ==================================================================
    # 3 — Detect Zero-Day Signals
    # ==================================================================
    def detect_zero_day(self, text: str) -> bool:
        text = text.lower()
        for zd in self.ZERO_DAY_PATTERNS:
            if re.search(zd, text):
                return True
        return False

    # ==================================================================
    # 4 — Run Correlation Rules
    # ==================================================================
    def correlate(self, findings: List[Dict]) -> List[Dict]:
        results = []

        for rule in self.CORRELATIONS:
            a, b, label = rule

            found_a = any(a in f["description"].lower() for f in findings)
            found_b = any(b in f["description"].lower() for f in findings)

            if found_a and found_b:
                results.append({
                    "correlation": label,
                    "matched": [a, b],
                    "severity": "CRITICAL"
                })

        return results

    # ==================================================================
    # 5 — Global Engine: Combine everything
    # ==================================================================
    def process(self, findings: List[Dict]) -> Dict:
        """
        findings = [
            {"target": "...", "description": "...", "type": "..."},
            ...
        ]
        """

        zero_day_hits = []
        correlations = []

        # 1 — Zero-day detection
        for f in findings:
            if self.detect_zero_day(f["description"]):
                zero_day_hits.append({
                    "target": f["target"],
                    "indicator": "Zero-Day Signal",
                    "description": f["description"]
                })

        # 2 — Run correlation engine
        correlations = self.correlate(findings)

        return {
            "zero_day_signals": zero_day_hits,
            "correlated_attacks": correlations
        }


# ======================================================================
# END OF FILE
# ======================================================================
