# =====================================================
# Digital Sentinel v11.3 - Discord Reporter
# =====================================================
import requests
import json
import os
from datetime import datetime

class DiscordReporter:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")

    def send_message(self, title, description, color=0x00ffcc):
        if not self.webhook_url:
            print("[!] Discord webhook not configured. Skipping notification.")
            return

        payload = {
            "embeds": [{
                "title": f"🛰️ {title}",
                "description": description,
                "color": color,
                "footer": {"text": f"Digital Sentinel • {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"}
            }]
        }

        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 204:
                print("[+] Discord notification sent successfully.")
            else:
                print(f"[!] Discord response: {response.status_code}")
        except Exception as e:
            print(f"[!] Discord send error: {e}")

    def send_report_summary(self, report_file):
        """Send the content of a generated report to Discord."""
        if not os.path.exists(report_file):
            print(f"[!] Report file not found: {report_file}")
            return
        with open(report_file, "r", encoding="utf-8") as f:
            content = f.read()[:1900]  # Discord limit 2000 chars
        self.send_message("Scan Report Summary", f"```\n{content}\n```")
