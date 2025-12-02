# =========================================
#   Digital Sentinel – Bug Bounty Templates
# =========================================

VRT_MAP = {
    "CRITICAL": "Improper Access Control → Authentication → High-Risk Account Compromise",
    "HIGH": "Improper Access Control → IDOR → Sensitive Data Exposure",
    "MEDIUM": "Business Logic → Misconfiguration → Information Disclosure",
    "LOW": "Information Disclosure → Minor Misconfigurations"
}

def build_bugcrowd_template(data):
    return f"""
🧠 **Digital Sentinel – Auto Report (Bugcrowd Format)**

### 1️⃣ Summary Title
**{data['summary']}**

### 2️⃣ Target
**{data['target']}**

### 3️⃣ VRT Category  
**{data['vrt']}**

### 4️⃣ Vulnerability URL
{data['url']}

### 5️⃣ Description
