import json
import time
from modules.subdomain_expander_v2 import run_expander   # ← NEW IMPORT


def perform_subdomain_scan(target):
    print(f"[SCAN] Subdomains → {target}")
    # ئەمە ڕووتینی سەرەتاییەکەتە – ئەگەر فایلی deep scan هەیە ئەوی جێگر بکە
    return ["www." + target, "api." + target]


def perform_full_scan(target):
    print("=" * 50)
    print(f"🚀 Full Scan → {target}")
    print("=" * 50)

    # STEP 1 — Normal subdomain scan
    subdomains = perform_subdomain_scan(target)

    # STEP 2 — Expansion (NEW)
    expanded = run_expander(target)
    subdomains = list(set(subdomains + expanded))

    print(f"🟢 Total Subdomains found for {target}: {len(subdomains)}")

    findings = []

    # هەرچ کۆدی scan یان vuln check که پێشتر بوو، لێرە دابنێ
    # نمونه:
    for sub in subdomains:
        print(f"[SCAN] Checking → {sub}")
        # … security checks …

    return {
        "target": target,
        "subdomains": subdomains,
        "findings": findings
    }


def load_targets():
    with open("data/targets/targets.txt") as f:
        return [x.strip() for x in f.readlines()]


def main():
    print("🚀 Starting Digital Sentinel v11.1 (Autonomous Mode)")
    targets = load_targets()
    print(f"🎯 Loaded {len(targets)} targets.")

    for target in targets:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🔵 Processing target → {target}")
        result = perform_full_scan(target)

        # Save reports
        with open(f"data/reports/{target}.json", "w") as f:
            json.dump(result, f, indent=2)

        print(f"[DONE] Report saved for {target}")

    print("🚀 FINISHED ALL TARGETS")


if __name__ == "__main__":
    main()
