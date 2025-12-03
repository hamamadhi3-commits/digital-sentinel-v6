import subprocess
import json
import os

OUTPUT_DIR = "data/subdomains/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TOOLS = [
    "subfinder",
    "assetfinder",
    "amass",
    "findomain"
]

def run_tool(tool, domain):
    try:
        print(f"🔍 Running {tool} on {domain} ...")

        if tool == "subfinder":
            cmd = ["subfinder", "-d", domain, "-silent"]
        elif tool == "assetfinder":
            cmd = ["assetfinder", "--subs-only", domain]
        elif tool == "amass":
            cmd = ["amass", "enum", "-d", domain, "-silent"]
        elif tool == "findomain":
            cmd = ["findomain", "--target", domain, "-q"]
        else:
            return []

        result = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
        subs = list(set(line.strip() for line in result.split("\n") if line.strip()))
        return subs

    except Exception as e:
        print(f"⚠️ Error in {tool}: {e}")
        return []


def expand_subdomains(domain):
    all_results = set()

    for tool in TOOLS:
        subs = run_tool(tool, domain)
        all_results.update(subs)

    save_path = os.path.join(OUTPUT_DIR, f"{domain}.txt")
    with open(save_path, "w", encoding="utf-8") as f:
        for s in sorted(all_results):
            f.write(s + "\n")

    print(f"📁 Saved {len(all_results)} subdomains → {save_path}")
    return list(all_results)
