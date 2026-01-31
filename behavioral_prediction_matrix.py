from __future__ import annotations

from typing import Any, Dict, List
from collections import Counter


class BehaviorPredictor:
    async def predict_user_needs(
        self,
        query: str,
        user_profile: Any,
        temporal_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        text = (query or "").lower()
        candidates: List[str] = []
        if any(k in text for k in ("help", "how", "guide")):
            candidates.append("seek_guidance")
        if any(k in text for k in ("buy", "price", "cost")):
            candidates.append("purchase_intent")
        if any(k in text for k in ("error", "issue", "bug")):
            candidates.append("troubleshoot")
        if not candidates:
            candidates.append("general_inquiry")

        scores = {c: 0.5 for c in candidates}
        # boost if user historically asked similar things
        hist = getattr(user_profile, "interaction_history", []) or []
        words = []
        for h in hist[-50:]:
            msg = (h.get("message") or h.get("query") or "").lower()
            words.extend(w for w in msg.split() if len(w) > 3)
        freq = Counter(words)
        if freq:
            for c in scores:
                if c in ("seek_guidance", "troubleshoot") and sum(freq[w] for w in ("help", "error", "issue") if w in freq):
                    scores[c] += 0.2

        if isinstance(temporal_context, dict) and temporal_context.get("recent_activity", 0) < 3600:
            # very recent activity -> higher intent
            for c in scores:
                scores[c] += 0.1

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return {
            "predicted_needs": [{"intent": k, "score": round(v, 3)} for k, v in ranked],
            "signals": {
                "history_count": len(hist),
                "recent_activity_s": temporal_context.get("recent_activity") if isinstance(temporal_context, dict) else None,
            },
        }

    async def deep_pattern_analysis(self, user_profile: Any) -> Dict[str, Any]:
        hist = getattr(user_profile, "interaction_history", []) or []
        topic_counts = Counter()
        for h in hist[-200:]:
            msg = (h.get("message") or h.get("query") or "").lower()
            if any(k in msg for k in ("buy", "price", "cost")):
                topic_counts["commerce"] += 1
            if any(k in msg for k in ("error", "issue", "bug")):
                topic_counts["support"] += 1
            if any(k in msg for k in ("how", "help", "learn")):
                topic_counts["learning"] += 1
        total = sum(topic_counts.values()) or 1
        distribution = {k: v / total for k, v in topic_counts.items()}
        return {
            "topics": dict(topic_counts),
            "distribution": distribution,
            "engagement_level": min(1.0, len(hist) / 100.0),
        }
