import json, os

IN_FILE = "data/reports/ai_findings.json"
OUT_FILE = "data/reports/validated_findings.json"
ARCHIVE = "data/reports/archive_seen.json"

def filter_duplicates():
    print("🔁 Checking duplicates vs archive")
    seen = set()
    if os.path.exists(ARCHIVE):
        seen = set(json.load(open(ARCHIVE)))

    new_data = []
    findings = json.load(open(IN_FILE))
    for f in findings:
        key = f"{f['domain']}::{f['type']}"
        if key not in seen:
            new_data.append(f)
            seen.add(key)

    json.dump(new_data, open(OUT_FILE, "w"), indent=2)
    json.dump(list(seen), open(ARCHIVE, "w"), indent=2)
    print(f"✅ {len(new_data)} new unique findings")

if __name__ == "__main__":
    filter_duplicates()
