#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Sentinel v11 – Discord Report Subsystem
Auto-sends beautiful embedded summaries to Discord.
"""

import os
import json
import requests
from datetime import datetime


def send_discord_summary():
    """Reads the Eternal Hunter report and sends an embedded Discord message."""
    webhook_url = os.getenv("DISCORD_WEBHOOK")

    if not webhook_url:
        print("⚠️ No Discord webhook configured. Skipping report dispatch.")
        return

    report_path = "data/reports/eternal_hunter_summary.json"
    if not os.path.exists(report_path):
        print(f"⚠️ Report file not found at: {report_path}")
        return

    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    # Extract key metrics
    total_targets = report.get("total_targets", 0)
    vulns = report.get("vulnerabilities_detected", 0)
    latency = report.get("average_latency_ms", 0)
    timestamp = report.get("report_time", datetime.utcnow().isoformat())

    # Choose color dynamically (green if low vulns, red if many)
    color = 0x00FF00 if vulns == 0 else (0xFFA500 if vulns < 5 else 0xFF0000)

    embed = {
        "title": "🧠 Digital Sentinel v11 — Eternal Hunter Summary",
        "description": (
            f"**🕒 Report Time:** {timestamp}\n"
            f"**🎯 Targets Scanned:** {total_targets}\n"
            f"**⚔️ Vulnerabilities Found:** {vulns}\n"
            f"**⏱️ Avg Latency:** {latency} ms\n\n"
            "📦 *Artifact: digital-sentinel-v11-reports*"
        ),
        "color": color,
        "footer": {"text": "Digital Sentinel Autonomous System v11"},
        "timestamp": datetime.utcnow().isoformat(),
        "fields": []
    }

    # Add top 3 targets as examples if available
    results = report.get("results", [])
    for r in results[:3]:
        embed["fields"].append({
            "name": f"🔹 {r['target']}",
            "value": f"Latency: {r['response_time_ms']}ms | Vulns: {r['vulnerabilities_found']}",
            "inline": False
        })

    payload = {"embeds": [embed]}

    try:
        resp = requests.post(webhook_url, json=payload)
        if resp.status_code in (200, 204):
            print("✅ Discord summary successfully delivered.")
        else:
            print(f"❌ Discord webhook failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"❌ Discord reporting error: {e}")


if __name__ == "__main__":
    send_discord_summary()
