# =============================================================================
#  Digital Sentinel — Automated Report Builder v1.0
#  Creates professional CRITICAL/HIGH/MEDIUM reports with 6 sections
#  Designed especially for Themoralhack 👑
# =============================================================================

import uuid
from datetime import datetime


class ReportBuilderEngine:

    # =====================================================================
    # 1 — Bugcrowd/HackerOne severity mapping
    # =====================================================================
    SEVERITY_MAP = {
        "critical": "🔥 CRITICAL",
        "high": "🔴 HIGH",
        "medium": "🟠 MEDIUM",
        "low": "🟡 LOW",
        "info": "🔵 INFO"
    }

    # =====================================================================
    # 2 — Six-section report template
    # =====================================================================
    REPORT_TEMPLATE = """
🚨 **{severity} Vulnerability Report**  
📌 Report ID: `{report_id}`
⏱ Date: {timestamp}

---

### 1️⃣ **Summary Title**
{summary}

---

### 2️⃣ **Affected Target**
`{target}`

---

### 3️⃣ **VRT Category**
{category}

---

### 4️⃣ **Technical Vulnerability Details**
```
{details}
```

---

### 5️⃣ **Plain Language Description**
{description}

---

### 6️⃣ **Attachments (PoC / Proof of Exploit)**
{attachments}

---
🔗 *Generated automatically by Digital Sentinel v6.0 for Themoralhack*
"""

    # =====================================================================
    # 3 — Build report
    # =====================================================================
    def build_report(self, summary, target, category, details, description, attachments, severity):
        
        report_id = str(uuid.uuid4())[:8]
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        severity_label = self.SEVERITY_MAP.get(severity.lower(), "🔵 INFO")

        return self.REPORT_TEMPLATE.format(
            severity=severity_label,
            report_id=report_id,
            timestamp=timestamp,
            summary=summary.strip(),
            target=target.strip(),
            category=category.strip(),
            details=details.strip(),
            description=description.strip(),
            attachments=attachments.strip(),
        )

    # =====================================================================
    # 4 — classify severity automatically
    # =====================================================================
    def classify_severity(self, data: str) -> str:
        d = data.lower()

        if any(i in d for i in ["rce", "remote code", "ssrf", "critical", "takeover"]):
            return "critical"

        if any(i in d for i in ["idor", "no rate limit", "sqli", "admin", "token leak"]):
            return "high"

        if any(i in d for i in ["xss", "csrf", "path", "misconfig"]):
            return "medium"

        return "info"

    # =====================================================================
    # 5 — wrapper for full automated mode (AI → Report)
    # =====================================================================
    def automated_from_finding(self, finding: dict) -> str:
        """
        finding = {
            "target": "...",
            "description": "...",
            "technical": "...",
            "category": "...",
            "poc": "...",
        }
        """

        severity = self.classify_severity(
            finding["description"] + finding["technical"]
        )

        return self.build_report(
            summary=finding["description"],
            target=finding["target"],
            category=finding["category"],
            details=finding["technical"],
            description=finding["description"],
            attachments=finding.get("poc", "No PoC provided"),
            severity=severity
        )


# =============================================================================
# END OF FILE
# =============================================================================
