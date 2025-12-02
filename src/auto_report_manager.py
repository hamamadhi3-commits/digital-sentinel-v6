import json
import datetime
from report_templates import VRT_MAP, build_bugcrowd_template
from discord_auto_reporter import send_report_to_discord

class AutoReportManager:

    def prepare_report(self, finding):
        severity = finding.get("severity", "MEDIUM")
        target = finding.get("target", "Unknown Target")
        vuln = finding.get("vuln", "Potential vulnerability")
        url = finding.get("url", "Unknown URL")

        # Summary title
        summary = f"[{severity}] {vuln} – {target}"

        # VRT auto map
        vrt = VRT_MAP.get(severity, "General Misconfiguration")

        # Description building
        description = (
            f"Digital Sentinel detected a {severity} vulnerability on {target}.\n\n"
            f"Details:\n{vuln}\n\n"
            f"Impact:\n"
            f"- Potential security risk depending on configuration\n"
            f"- Needs manual triage\n\n"
            f"Timestamp: {datetime.datetime.utcnow()} UTC"
        )

        data = {
            "summary": summary,
            "target": target,
            "vrt": vrt,
            "url": url,
            "description": description,
            "attachments": "Auto-generated logs included"
        }

        return data

    def process_and_send(self, finding):
        report_data = self.prepare_report(finding)
        formatted = build_bugcrowd_template(report_data)
        send_report_to_discord(formatted)
        return formatted
