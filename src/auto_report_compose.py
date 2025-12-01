import json, os, datetime

VALIDATED = "data/reports/validated_findings.json"
REPORT_DIR = "data/reports/ready_to_send"

def compose_reports():
    print("🧩 Composing Bugcrowd style reports…")
    os.makedirs(REPORT_DIR, exist_ok=True)
    findings = json.load(open(VALIDATED))

    for i, f in enumerate(findings):
        report = {
            "Submission title": f"[Auto] {f['type']} detected on {f['domain']}",
            "Target": f["domain"],
            "VRT Category": f["type"],
            "URL/Location": f"https://{f['domain']}",
            "Description": (
                f"Automated recon identified {f['type']} pattern on {f['domain']}.\n"
                "Evidence snippet:\n" + f['evidence']
            ),
            "Timestamp": datetime.datetime.utcnow().isoformat()
        }
        path = f"{REPORT_DIR}/report_{i}.json"
        json.dump(report, open(path, "w"), indent=2)
    print(f"✅ Composed {len(findings)} reports")

if __name__ == "__main__":
    compose_reports()
