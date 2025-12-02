import subprocess

def active_recon(domain):

    data = {}

    # port scan
    try:
        ports = subprocess.getoutput(f"naabu -host {domain} -silent -top-ports 100")
        data["ports"] = ports
    except:
        data["ports"] = "error"

    # http probing
    try:
        httpx_res = subprocess.getoutput(f"httpx -silent -status-code -title -tech-detect -url https://{domain}")
        data["httpx"] = httpx_res
    except:
        data["httpx"] = "error"

    return data
