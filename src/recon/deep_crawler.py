import subprocess

def deep_crawl(domain):

    urls = []

    try:
        output = subprocess.getoutput(f"katana -u https://{domain} -silent -depth 3")
        urls = output.split("\n")
    except:
        pass

    return urls
