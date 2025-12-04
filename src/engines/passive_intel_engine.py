import asyncio
import socket
import shodan
import httpx
import subprocess
from bs4 import BeautifulSoup
import tldextract
import os

SHODAN_KEY = os.getenv("SHODAN_API_KEY", "")


class ActiveIntelEngine:
    """
    Active Intelligence Engine
    - Fast Port Scan
    - HTTP Title Fetcher
    - Shodan Info
    - Basic Fingerprinting
    """

    def __init__(self):
        self.engine_name = "Active-Intel"

    # -----------------------------------------------------------
    # 1) FAST PORT SCAN (very lightweight)
    # -----------------------------------------------------------
    def fast_portscan(self, domain):
        open_ports = []
        ports = [80, 443, 8080, 8443, 22, 21, 25, 53]

        for port in ports:
            try:
                sock = socket.socket()
                sock.settimeout(0.7)
                result = sock.connect_ex((domain, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass

        return open_ports

    # -----------------------------------------------------------
    # 2) SHODAN LOOKUP
    # -----------------------------------------------------------
    def shodan_lookup(self, domain):
        if not SHODAN_KEY:
            return {"error": "Missing SHODAN_API_KEY"}

        try:
            api = shodan.Shodan(SHODAN_KEY)
            result = api.search(domain)
            return result
        except Exception as e:
            return {"error": str(e)}

    # -----------------------------------------------------------
    # 3) HTTP TITLE FETCHER
    # -----------------------------------------------------------
    async def fetch_title(self, url):
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                title = soup.title.string if soup.title else "No Title"
                return {"url": url, "title": title}
        except:
            return {"url": url, "title": None}

    # -----------------------------------------------------------
    # MAIN RUN METHOD
    # -----------------------------------------------------------
    def run(self, target):
        extracted = tldextract.extract(target)
        domain = extracted.registered_domain

        results = {
            "engine": self.engine_name,
            "domain": domain,
            "open_ports": self.fast_portscan(domain),
            "shodan": self.shodan_lookup(domain),
        }

        return results
