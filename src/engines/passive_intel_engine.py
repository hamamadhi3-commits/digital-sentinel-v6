import requests
import json
import socket
import tldextract
import dns.resolver

SHODAN_KEY = ""
WAYBACK_URL = "http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&collapse=urlkey"


def whois_lookup(domain):
    try:
        import whois
        data = whois.whois(domain)
        return {"whois": str(data)}
    except:
        return {"whois": "error or rate-limited"}


def dns_records(domain):
    records = {}
    types = ["A", "AAAA", "MX", "NS", "TXT"]

    for t in types:
        try:
            answers = dns.resolver.resolve(domain, t)
            records[t] = [str(r) for r in answers]
        except:
            records[t] = []

    return {"dns": records}


def ip_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {"ip": ip}
    except:
        return {"ip": None}


def subdomain_passive(domain):
    try:
        url = f"https://jldc.me/anubis/subdomains/{domain}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return {"subdomains": r.json()}
    except:
        pass

    return {"subdomains": []}


def shodan_passive(ip):
    if not SHODAN_KEY or not ip:
        return {"shodan": []}

    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_KEY}"
        r = requests.get(url)
        if r.status_code == 200:
            return {"shodan": r.json()}
    except:
        return {"shodan": []}

    return {"shodan": []}


def wayback_urls(domain):
    try:
        r = requests.get(WAYBACK_URL.format(domain=domain), timeout=10)
        data = r.json()[1:50]  # only top 50
        urls = [x[2] for x in data]
        return {"wayback": urls}
    except:
        return {"wayback": []}


def run_passive_intel(domain):
    ext = tldextract.extract(domain)
    full_domain = f"{ext.domain}.{ext.suffix}"

    result = {}
    result.update(whois_lookup(full_domain))
    result.update(dns_records(full_domain))
    result.update(ip_lookup(full_domain))
    result.update(subdomain_passive(full_domain))
    result.update(wayback_urls(full_domain))

    ip = result.get("ip", None)
    result.update(shodan_passive(ip))

    return result
