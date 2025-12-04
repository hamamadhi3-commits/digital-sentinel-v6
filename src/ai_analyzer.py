# ============================================================
# Digital Sentinel - AI Analysis & Prioritization Engine
# ============================================================

def run_ai_analysis(findings):
    """
    Simulate AI-based severity classification and prioritization.
    """
    print(f"[AI] Analyzing {len(findings)} findings for severity patterns...")

    # Apply simple heuristic AI prioritization
    for f in findings:
        url = f.get("url", "")
        desc = f.get("description", "").lower()

        if "login" in url or "auth" in url:
            f["severity"] = "critical"
            f["ai_note"] = "High risk: authentication-related endpoint."
        elif "api" in url:
            f["severity"] = "high"
            f["ai_note"] = "API endpoint exposure may leak sensitive data."
        elif "staging" in url or "test" in url:
            f["severity"] = "medium"
            f["ai_note"] = "Testing environment vulnerability."
        else:
            f["severity"] = "low"
            f["ai_note"] = "General or low-impact finding."

    print(f"[AI] Prioritization complete. {len(findings)} findings analyzed.")
    return findings
