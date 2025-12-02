import subprocess

COMMON_SHADOW = [
    "admin", "dashboard", "internal", "portal",
    "dev", "staging", "test", "beta",
    "login", "auth", "api", "backend",
]

def shadow_recon(domain):
    results = []

    for prefix in COMMON_SHADOW:
        sub = f"{prefix}.{domain}"
        try:
            out = subprocess.getoutput(f"httpx -silent -timeout 4 -no-color -title -status-code -url https://{sub}")
            if sub in out:
                results.append(sub)
        except:
            pass

    return results
