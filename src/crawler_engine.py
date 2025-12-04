# ============================================================
# Digital Sentinel v6 - Crawler Engine
# Author: Themoralhack & Manus AI
# Mission: Collect internal links, JS files, and API endpoints.
# ============================================================

import concurrent.futures
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def crawl_single_target(target_data):
    """Crawls a live target and extracts URLs + scripts."""
    url = target_data.get("live_url")
    if not url or target_data["status"] != "alive":
        return {"target": target_data["target"], "urls": [], "scripts": []}

    found_links, found_scripts = set(), set()

    try:
        response = requests.get(url, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if urlparse(link).netloc == urlparse(url).netloc:
                found_links.add(link)

        for script in soup.find_all("script", src=True):
            s_link = urljoin(url, script["src"])
            found_scripts.add(s_link)

        print(f"[🕸️] Crawled {url} → {len(found_links)} links, {len(found_scripts)} scripts")

    except Exception as e:
        print(f"[⚠️] Crawl failed for {url}: {e}")

    return {
        "target": target_data["target"],
        "urls": list(found_links),
        "scripts": list(found_scripts)
    }


def run_crawling_batch(probing_results):
    """Runs crawling for all live domains."""
    print("[🌍] Starting web crawling phase...")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(crawl_single_target, t) for t in probing_results]
        for f in concurrent.futures.as_completed(futures):
            try:
                results.append(f.result())
            except Exception as e:
                print(f"[⚠️] Crawl thread error: {e}")

    print(f"[✅] Crawling finished: {len(results)} domains processed.")
    return results
