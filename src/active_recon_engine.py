import subprocess
import json
import httpx
import tldextract
import re
import os

def run_cmd(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        return result
    except:
        return ""

def nmap_scan(target):
    output = run_cmd(f"nmap -sV -Pn -T4 {target}")
    return {"nmap_raw": output}

def get_headers(target):
    try:
        r = httpx.get(f"http://{target}", timeout=5)
        return dict(r.headers)
    except:
        return {}

def extract_js_files(html):
    return re.findall(r'<script.+?src="([^"]+)"', html)

def extract_endpoints(js_code):
    return re.findall(r'/[a-zA-Z0-9/_-]{4,}', js_code)

def fetch_page(target):
    try:
        r = httpx.get(f"http://{target}", timeout=5)
        return r.text
    except:
        return ""

def find_admin_panels(html):
    patterns = ["admin", "cpanel", "dashboard", "manage"]
    found = []
    for p in patterns:
        if p in html.lower():
            found.append(p)
    return found

def active_recon(target):
    result = {}

    html = fetch_page(target)
    result["headers"] = get_headers(target)
    result["admin_hits"] = find_admin_panels(html)

    js_files = extract_js_files(html)
    js_all = ""
    endpoints = []

    for js in js_files:
        try:
            if js.startswith("http"):
                code = httpx.get(js).text
            else:
                code = httpx.get(f"http://{target}/{js}").text
            js_all += code
        except:
            pass

    result["js_endpoints"] = extract_endpoints(js_all)
    result["ports"] = nmap_scan(target)

    return result
