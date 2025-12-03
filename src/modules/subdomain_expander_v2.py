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
        print(f"🔎 Running {tool} on {domain} ...")

        if tool == "subfinder":
            cmd = ["subfinder", "-d", domain, "-silent"]
        elif tool == "assetfinder":
            cmd = ["assetfinder", domain]
        elif tool == "amass":
            cmd = ["amass", "enum", "-d", domain, "-passive"]
        elif tool == "findomain":
            cmd = ["findomain", "-t", domain, "-q"]
        else:
            return []

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️ Error running {tool}: {result.stderr}")
            return []

        output = result.stdout.splitlines()
        return output

    except Exception as e:
        print(f"❌ Exception in {tool}: {e}")
        return []


def run_expander(domain):
    print(f"🚀 Expanding subdomains for: {domain}")
    
    all_subdomains = []

    for tool in TOOLS:
        found = run_tool(tool, domain)
        all_subdomains.extend(found)

    # remove duplicates
    all_subdomains = list(set(all_subdomains))

    # save result
    outfile = os.path.join(OUTPUT_DIR, f"{domain}.txt")
    with open(outfile, "w") as f:
        for sub in all_subdomains:
            f.write(sub + "\n")

    print(f"✅ Expansion done → {len(all_subdomains)} subdomains found")
    return all_subdomains
