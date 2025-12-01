import os, json, requests

WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/EXAMPLE")
REPORT_DIR = "data/reports/ready_to_send"

def send_discord():
    print("📡 Sending findings to Discord…")
    for f in os.listdir(REPORT_DIR):
        report = json.load(open(f"{REPORT_DIR}/{f}"))
        embed = {
            "username": "Digital Sentinel v6.0",
            "embeds": [{
                "title": report["Submission title"],
                "description": (
                    f"**Target:** {report['Target']}\n"
                    f"**Type:** {report['VRT Category']}\n"
                    f"**URL:** {report['URL/Location']}\n"
                    f"**Description:**\n{report['Description']}"
                ),
                "color": 15844367
            }]
        }
        try:
            requests.post(WEBHOOK, json=embed)
        except Exception as e:
            print("❌ Discord error:", e)
    print("✅ Discord notifications sent")

if __name__ == "__main__":
    send_discord()
