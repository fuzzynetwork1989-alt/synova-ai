from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class EthicsResult:
    approved: bool
    reason: str = ""


class EthicsGuardian:
    def __init__(self, level: str = "standard"):
        self.level = level
        self._banned_keywords = {
            "standard": {"harm", "illegal", "malware", "violence"},
            "advanced": {"harm", "illegal", "malware", "violence", "exploit", "terror"},
        }

    async def validate_query(self, query: str, context: Optional[Dict] = None) -> EthicsResult:
        text = (query or "").lower()
        banned = self._banned_keywords.get(self.level, self._banned_keywords["standard"])  # type: ignore[index]
        for word in banned:
            if word in text:
                return EthicsResult(approved=False, reason=f"Contains prohibited content: {word}")
        return EthicsResult(approved=True, reason="")
