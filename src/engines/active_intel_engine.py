# src/engines/active_intel_engine.py
# Engine responsible for active intelligence gathering (ports, services, banners)

import asyncio
import socket
import httpx
import subprocess
from bs4 import BeautifulSoup
import tldextract
import os

class ActiveIntelEngine:
    def __init__(self):
        self.engine_name = "ActiveIntelEngine"

    async def fast_portscan(self, domain):
        """Perform async TCP scan on common ports"""
        common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 3306, 8080]
        results = {}
        for port in common_ports:
            try:
                conn = asyncio.open_connection(domain, port)
                reader, writer = await asyncio.wait_for(conn, timeout=1.5)
                results[port] = "open"
                writer.close()
                await writer.wait_closed()
            except:
                results[port] = "closed"
        return results

    async def grab_banner(self, domain, port):
        """Grab service banner from an open port"""
        try:
            reader, writer = await asyncio.open_connection(domain, port)
            writer.write(b'HEAD / HTTP/1.0\r\n\r\n')
            await writer.drain()
            data = await reader.read(128)
            writer.close()
            await writer.wait_closed()
            return data.decode(errors='ignore')
        except:
            return None

    def fetch_http_title(self, url):
        """Get the title of a webpage"""
        try:
            r = httpx.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.title.string if soup.title else "No Title"
            return title.strip()
        except Exception as e:
            return f"HTTP error: {str(e)}"

    def run(self, target):
        """Main execution"""
        print(f"[+] Running {self.engine_name} on {target}")
        try:
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(self.fast_portscan(target))
            print(f"Port Scan Results for {target}: {results}")

            open_ports = [p for p, s in results.items() if s == "open"]
            for p in open_ports:
                banner = loop.run_until_complete(self.grab_banner(target, p))
                if banner:
                    print(f"[{p}] Banner: {banner.strip()[:80]}")

            http_url = f"http://{target}"
            title = self.fetch_http_title(http_url)
            print(f"Website Title: {title}")
        except Exception as e:
            print(f"❌ ActiveIntelEngine Error: {e}")
