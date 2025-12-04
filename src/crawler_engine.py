# ============================================================
# Digital Sentinel - Web Crawler & JS Parser Engine
# ============================================================

def run_crawler(hosts):
    """
    Simulate crawling URLs and parsing JS endpoints for each live host.
    """
    print("[CRAWLER] Crawling endpoints and extracting URLs...")

    urls = []
    for host in hosts:
        urls.extend([
            f"https://{host}/",
            f"https://{host}/login",
            f"https://{host}/api/v1/info",
            f"https://{host}/dashboard",
            f"https://{host}/assets/js/app.js"
        ])

    print(f"[CRAWLER] Crawled {len(urls)} URLs/endpoints total.")
    return urls
