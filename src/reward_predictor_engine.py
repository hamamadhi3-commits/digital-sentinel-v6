# =============================================================================
#  Digital Sentinel — Reward Prediction Engine v1.0
#  Predicts reward ranges for CRITICAL/HIGH/MEDIUM vulnerabilities
#  Detects duplicates, impact score, likelihood and confidence
# =============================================================================

import hashlib
import random


class RewardPredictor:

    # =====================================================================
    # Known Reward Ranges Based on Bugcrowd/H1 Data
    # =====================================================================
    REWARD_TABLE = {
        "critical": (1500, 10000),   # واقعی – تێسلا لە 3000–10000
        "high":     (500, 1500),
        "medium":   (150, 500),
        "low":      (0, 150),
        "info":     (0, 0)
    }

    # =====================================================================
    # Fake database to detect duplicates
    # (Your system can connect to real API later)
    # =====================================================================
    DUPLICATE_MEMORY = set()

    # =====================================================================
    # Build unique hash for each vulnerability
    # =====================================================================
    def _hash_finding(self, target, details):
        data = (target + details).encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    # =====================================================================
    # Predict reward range
    # =====================================================================
    def predict_reward(self, severity):
        low, high = self.REWARD_TABLE.get(severity, (0, 0))
        return random.randint(low, high)

    # =====================================================================
    # Impact Score (0–100)
    # =====================================================================
    def impact_score(self, severity, details):
        base = {
            "critical": 90,
            "high": 70,
            "medium": 50,
            "low": 20,
            "info": 10
        }.get(severity, 10)

        # Increase based on technical keywords
        if "admin" in details.lower(): base += 10
        if "bypass" in details.lower(): base += 10
        if "tokens" in details.lower(): base += 10
        if "account takeover" in details.lower(): base += 20
        if "rce" in details.lower(): base = 100

        return min(base, 100)

    # =====================================================================
    # Confidence Score (0–100)
    # =====================================================================
    def confidence_score(self, details):
        score = 20
        if len(details) > 200: score += 30
        if "steps" in details.lower(): score += 20
        if "poc" in details.lower(): score += 20
        if "impact" in details.lower(): score += 10
        return min(score, 100)

    # =====================================================================
    # Main Prediction Function
    # =====================================================================
    def analyze(self, summary, target, severity, details):
        
        fingerprint = self._hash_finding(target, details)

        # ---------------------------------------------------------------
        # Detect duplicates (has someone reported EXACT same bug?)
        # ---------------------------------------------------------------
        if fingerprint in self.DUPLICATE_MEMORY:
            duplicate = True
        else:
            duplicate = False
            self.DUPLICATE_MEMORY.add(fingerprint)

        # ---------------------------------------------------------------
        # Predict Reward
        # ---------------------------------------------------------------
        reward = self.predict_reward(severity)

        # ---------------------------------------------------------------
        # Impact + Confidence
        # ---------------------------------------------------------------
        impact = self.impact_score(severity, details)
        confidence = self.confidence_score(details)

        # ---------------------------------------------------------------
        # Final Output Dictionary
        # ---------------------------------------------------------------
        return {
            "summary": summary,
            "target": target,
            "severity": severity,
            "duplicate": duplicate,
            "predicted_reward": reward,
            "impact_score": impact,
            "confidence": confidence,
        }


# =============================================================================
# END OF FILE
# =============================================================================
