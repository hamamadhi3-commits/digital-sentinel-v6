# src/engines/active_intel_engine.py

import asyncio
import socket
import subprocess
import httpx
from bs4 import BeautifulSoup
import tldextract
import os


class ActiveIntelEngine:

    def __init__(self):
        self.engine_name = "ActiveIntel"

    def fast_portscan(self, domain):
        """
        Simple fast nmap port scan
        """
        try:
            cmd = ["nmap", "-T4", "-F", domain]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"[ERROR] Fast Port Scan Failed: {e}"

    def http_probe(self, domain):
        """
        Simple http probe using httpx
        """
        try:
            url = f"http://{domain}"
            r = httpx.get(url, timeout=5)
            return {"status": r.status_code, "headers": dict(r.headers)}
        except Exception as e:
            return {"error": str(e)}

    def run(self, target):
        """
        Main entry point
        """
        return {
            "target": target,
            "portscan": self.fast_portscan(target),
            "http_probe": self.http_probe(target),
        }
