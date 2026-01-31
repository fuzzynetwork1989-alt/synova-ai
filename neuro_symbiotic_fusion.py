from __future__ import annotations

from typing import Any, Dict, Optional
import hashlib


class NeuroSymbolicEngine:
    async def reason(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        text = (query or "").strip()
        ctx_keys = sorted(list((context or {}).keys()))
        signature = hashlib.sha256((text + "|" + ",".join(ctx_keys)).encode("utf-8")).hexdigest()[:12]
        return {
            "symbolic_insights": {
                "keywords_detected": [w for w in text.lower().split()[:5]],
                "context_keys": ctx_keys,
            },
            "confidence": 0.8,
            "signature": signature,
        }
