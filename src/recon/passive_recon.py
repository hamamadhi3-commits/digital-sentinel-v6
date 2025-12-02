import subprocess

def passive_recon(domain):

    results = {}

    # 1) crt.sh subdomain enumeration
    try:
        crt = subprocess.getoutput(f'curl -s "https://crt.sh/?q=%25.{domain}&output=json"')
        results["crt"] = crt
    except:
        results["crt"] = "error"

    # 2) Censys-like lookup (passive)
    try:
        censys = subprocess.getoutput(f"httpx -silent -no-color -title -status-code -cdn -probe -host {domain}")
        results["censys"] = censys
    except:
        results["censys"] = "error"

    # 3) SSL scan
    try:
        ssl = subprocess.getoutput(f"sslscan {domain} 2>/dev/null")
        results["ssl"] = ssl
    except:
        results["ssl"] = "error"

    return results
