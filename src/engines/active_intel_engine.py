# src/engines/active_intel_engine.py
# Active intelligence engine: performs fast port scanning, banner grabbing, and HTTP title fetching.

import asyncio
import socket
import httpx
from bs4 import BeautifulSoup
import tldextract
import os


class ActiveIntelEngine:
    def __init__(self):
        self.engine_name = "ActiveIntelEngine"

    async def fast_portscan(self, domain):
        """Perform asynchronous TCP port scan on common ports."""
        common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 8080]
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
        """Grab banner from open TCP port."""
        try:
            reader, writer = await asyncio.open_connection(domain, port)
            writer.write(b"HEAD / HTTP/1.0\r\n\r\n")
            await writer.drain()
            data = await reader.read(128)
            writer.close()
            await writer.wait_closed()
            return data.decode(errors="ignore").strip()
        except Exception:
            return None

    def fetch_http_title(self, domain):
        """Fetch website title via HTTP."""
        try:
            url = f"http://{domain}"
            r = httpx.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.title.string.strip() if soup.title else "No Title"
            return title
        except Exception as e:
            return f"HTTP fetch error: {e}"

    def run(self, target):
        """Run all active intelligence modules."""
        print(f"\n[🔎] Running {self.engine_name} on target: {target}")
        try:
            loop = asyncio.get_event_loop()
            ports = loop.run_until_complete(self.fast_portscan(target))
            open_ports = [p for p, s in ports.items() if s == "open"]

            print(f"🧩 Port Scan Results: {ports}")
            for port in open_ports:
                banner = loop.run_until_complete(self.grab_banner(target, port))
                if banner:
                    print(f"  📡 Port {port} Banner: {banner[:80]}")

            title = self.fetch_http_title(target)
            print(f"🌐 HTTP Title: {title}")

        except Exception as e:
            print(f"❌ ActiveIntelEngine error: {e}")
