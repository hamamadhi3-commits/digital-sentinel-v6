def build_poc_report(target, vuln_type, endpoint, evidence, payload, vrt, severity):

    report = f"""
==========================
🥷 DIGITAL SENTINEL REPORT
==========================

🎯 Target:
{target}

📌 VRT Category:
{vrt}

🚨 Severity:
{severity}

🧩 Vulnerability Type:
{vuln_type}

🔗 Affected Endpoint:
{endpoint}

🧪 Proof of Exploit (POC):
