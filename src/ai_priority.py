# =====================================================
# Digital Sentinel v11.3 - AI Prioritization Engine
# =====================================================
import random

def analyze_vulnerability(vuln_data, domain):
    """
    Enhances the raw vulnerability data with AI-based severity prediction,
    exploit likelihood estimation, and impact assessment.
    """
    title = vuln_data.get("title", "Unknown Issue")
    description = vuln_data.get("description", "")
    url = vuln_data.get("url", f"https://{domain}")
    evidence = vuln_data.get("evidence", "")

    # Fake AI-based probability models (for demonstration)
    severity_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    chosen_severity = random.choices(severity_levels, weights=[2, 3, 3, 2])[0]

    exploit_probability = round(random.uniform(0.2, 0.95), 2)
    impact_score = round(random.uniform(2.0, 9.8), 1)
    cvss_estimate = round((impact_score + (exploit_probability * 10)) / 2, 1)

    return {
        "domain": domain,
        "title": title,
        "description": description,
        "url": url,
        "severity": chosen_severity,
        "cvss": cvss_estimate,
        "impact_score": impact_score,
        "exploit_probability": exploit_probability,
        "evidence": evidence,
        "ai_analysis": f"Predicted severity {chosen_severity} with exploit chance {exploit_probability * 100:.0f}%"
    }
