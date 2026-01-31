from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime
import statistics


class TemporalEngine:
    async def analyze_temporal_patterns(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        interaction_history: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        now = datetime.utcnow()
        history = interaction_history or []

        timestamps = []
        msg_lengths = []
        for h in history:
            ts = h.get("timestamp")
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                except Exception:
                    ts = None
            if isinstance(ts, datetime):
                timestamps.append(ts)
            msg = h.get("message") or h.get("query") or ""
            if isinstance(msg, str):
                msg_lengths.append(len(msg))

        gaps = []
        if len(timestamps) > 1:
            ordered = sorted(timestamps)
            for i in range(1, len(ordered)):
                gaps.append((ordered[i] - ordered[i - 1]).total_seconds())

        avg_gap = statistics.fmean(gaps) if gaps else None
        avg_len = statistics.fmean(msg_lengths) if msg_lengths else None

        return {
            "timestamp": now.isoformat(),
            "history_count": len(history),
            "avg_interaction_gap_s": avg_gap,
            "avg_message_length": avg_len,
            "recent_activity": (now - (max(timestamps) if timestamps else now)).total_seconds(),
            "query_length": len(query or ""),
        }
