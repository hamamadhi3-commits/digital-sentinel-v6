# =========================================
#   Digital Sentinel – Bug Bounty Templates
# =========================================

# Auto-mapping severity → VRT taxonomy category
VRT_MAP = {
    "CRITICAL": "Improper Access Control → Authentication → High-Risk Account Compromise",
    "HIGH": "Improper Access Control → IDOR → Sensitive Data Exposure",
    "MEDIUM": "Business Logic → Misconfiguration → Information Disclosure",
    "LOW": "Information Disclosure → Minor Misconfigurations"
}


# =====================================================
#   Bugcrowd Template Builder
# =====================================================
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
```
{data['description']}
```

### 6️⃣ Attachments (Auto-Generated)
{data.get('attachments', 'None')}
"""


# =====================================================
#   HackerOne Template Builder
# =====================================================
def build_hackerone_template(data):
    return f"""
🧠 **Digital Sentinel – Auto Report (HackerOne Format)**

**Summary:**  
{data['summary']}

**Target:**  
{data['target']}

**VRT Category:**  
{data['vrt']}

**Vulnerability URL:**  
{data['url']}

**Description:**  
```
{data['description']}
```

**Attachments:**  
{data.get('attachments', 'None')}
"""
