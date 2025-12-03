import subprocess
import json
import httpx
import tldextract


def run_cmd(cmd):
    """Run shell commands safely and return output lines."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.splitlines()
    except Exception:
        return []


def http_probe(domain):
    """Probe HTTP/HTTPS and detect status codes + technologies."""
    results = []

    urls = [
        f"http://{domain}",
        f"https://{domain}"
    ]

    for url in urls:
        try:
            r = httpx.get(url, timeout=5, follow_redirects=True)
            tech = detect_technologies(r)

            results.append({
                "url": url,
                "status": r.status_code,
                "headers": dict(r.headers),
                "technologies": tech
            })
        except:
            pass

    return results


def detect_technologies(response):
    """Simple tech detection from headers + HTML."""
    tech = []

    headers = {k.lower(): v.lower() for k, v in response.headers.items()}
    body = response.text.lower()

    # --- HEADER BASED TECHS ---
    if "cloudflare" in str(headers):
        tech.append("Cloudflare")
    if "nginx" in str(headers):
        tech.append("Nginx")
    if "apache" in str(headers):
        tech.append("Apache")
    if "powered-by" in str(headers):
        tech.append(headers.get("x-powered-by", ""))

    # --- BODY BASED ---
    if "wp-content" in body:
        tech.append("WordPress")
    if "shopify" in body:
        tech.append("Shopify")
    if "drupal" in body:
        tech.append("Drupal")
    if "react" in body:
        tech.append("ReactJS")
    if "vue" in body:
        tech.append("VueJS")

    return list(set(tech))


def port_scan(domain):
    """Very fast top-ports scan using nmap (already in requirements)."""
    cmd = f"nmap -T4 --top-ports 50 -oG - {domain}"
    lines = run_cmd(cmd)

    ports = []
    for line in lines:
        if "/open/" in line:
            parts = line.split()
            for p in parts:
                if "/open/" in p:
                    ports.append(p)

    return ports


def run_active_engine(domain):
    """Main Execution Function"""
    print(f"🔎 [ACTIVE] Scanning → {domain}")

    result = {
        "domain": domain,
        "ports": port_scan(domain),
        "http_probe": http_probe(domain)
    }

    return result
