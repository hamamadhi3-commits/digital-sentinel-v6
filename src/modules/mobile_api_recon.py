import subprocess

def mobile_api_recon(domain):

    patterns = [
        f"https://api.{domain}",
        f"https://mobile.{domain}",
        f"https://m.{domain}",
        f"https://app.{domain}",
        f"https://client.{domain}",
        f"https://gateway.{domain}"
    ]

    alive = []

    for url in patterns:
        try:
            out = subprocess.getoutput(f"httpx -silent -status-code -title -url {url}")
            if url in out:
                alive.append(url)
        except:
            pass

    return alive
