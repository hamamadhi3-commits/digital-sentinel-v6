import os

OUTPUT_PATH = "data/targets.txt"

authorized_targets = [
    "tesla.com","apple.com","microsoft.com","google.com",
    "hackerone.com","bugcrowd.com","intigriti.com","yeswehack.com",
    "paypal.com","meta.com","amazon.com","cloudflare.com","openai.com",
    "discord.com","zoom.us","reddit.com","github.com","gitlab.com",
    "oracle.com","ibm.com","nvidia.com","intel.com","bitdefender.com",
    "kaspersky.com","sophos.com","cybersecurity.att.com","cisa.gov",
    "nist.gov","mitre.org","owasp.org","tryhackme.com","hackthebox.com"
]

def main():
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        for target in authorized_targets:
            f.write(f"{target}\n")
    print(f"🌐 {len(authorized_targets)} authorized targets written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
