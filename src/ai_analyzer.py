# ============================================================
# Digital Sentinel v6 - AI Analyzer Engine
# Author: Themoralhack & Manus AI
# Mission: Summarize vulnerability results into actionable insights.
# ============================================================

from collections import Counter
from datetime import datetime

def run_ai_analysis_batch(vuln_results):
    """Aggregate and summarize vulnerability findings."""
    print("[🧠] Running AI-style analysis phase...")

    summary = Counter()
    details = []

    for item in vuln_results:
        if item["findings"]:
            for f in item["findings"]:
                summary[f] += 1
            details.append(item)

    total_urls = len(vuln_results)
    affected_urls = len(details)
    most_common = summary.most_common(3)

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_urls_scanned": total_urls,
        "affected_urls": affected_urls,
        "vulnerability_summary": dict(summary),
        "top_vuln_types": [v for v, _ in most_common],
        "details": details,
        "analysis_comment": generate_analysis_comment(summary)
    }

    print(f"[📊] AI analysis complete → {affected_urls}/{total_urls} URLs affected.")
    return report


def generate_analysis_comment(summary):
    """Generate readable summary text."""
    if not summary:
        return "✅ No critical findings detected. All systems appear secure."
    text = "🚨 Detected potential risks: "
    parts = [f"{v}× {k.upper()}" for k, v in summary.items()]
    return text + ", ".join(parts)
