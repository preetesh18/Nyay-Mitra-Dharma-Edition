"""
vsd.py — Verified Scripture Database Models
────────────────────────────────────────────
Data classes for scripture entries and confidence levels.
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class ConfidenceLevel(Enum):
    """Scripture source confidence classification."""
    VERIFIED = "verified"      # Direct from authoritative scholarly source
    HIGH = "high"              # Standard translation, well-documented
    MODERATE = "moderate"      # Interpreted / paraphrased but sourced
    LOW = "low"                # Commentary or secondary interpretation
    EXCLUDED = "excluded"      # Not to be cited directly


@dataclass
class ScriptureEntry:
    """Unified scripture entry for all texts."""
    
    verse_id: str              # "BG-3.35", "CN-1-5", "HP-1-1", "VN-42"
    source: str                # "Bhagavad Gita", "Chanakya Niti", "Hitopadesha", "Vidura Niti"
    chapter_or_story: str      # "Chapter 3" / "Story 1: Tiger and Traveller"
    verse_num: str             # "35" / "1.5" / "42"
    
    # Original text
    sanskrit: str              # Devanagari, VERBATIM
    transliteration: str       # IAST or standard Roman transliteration
    translation: str           # Direct English translation
    
    # Metadata
    confidence_level: ConfidenceLevel
    source_attribution: str    # "Prabhupada", "Radhakrishnan", "KM Ganguli", "Murad Ali Baig"
    is_frequently_cited: bool = False
    
    # Usage flags
    allowed_in_advisory: bool = True
    allowed_in_verdict: bool = True
    
    tags: list = None          # ["decision", "fear", "duty", "karma"]
    note: str = ""             # Additional context
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
    
    def is_usable(self) -> bool:
        """Check if entry can be cited in responses."""
        return self.confidence_level in [
            ConfidenceLevel.VERIFIED,
            ConfidenceLevel.HIGH
        ]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "verse_id": self.verse_id,
            "source": self.source,
            "chapter_or_story": self.chapter_or_story,
            "verse_num": self.verse_num,
            "sanskrit": self.sanskrit,
            "transliteration": self.transliteration,
            "translation": self.translation,
            "confidence_level": self.confidence_level.value,
            "source_attribution": self.source_attribution,
            "is_frequently_cited": self.is_frequently_cited,
            "allowed_in_advisory": self.allowed_in_advisory,
            "allowed_in_verdict": self.allowed_in_verdict,
            "tags": self.tags,
            "note": self.note,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ScriptureEntry":
        """Create entry from dictionary."""
        return cls(
            verse_id=data["verse_id"],
            source=data["source"],
            chapter_or_story=data["chapter_or_story"],
            verse_num=data["verse_num"],
            sanskrit=data.get("sanskrit", ""),
            transliteration=data.get("transliteration", ""),
            translation=data.get("translation", ""),
            confidence_level=ConfidenceLevel(data["confidence_level"]),
            source_attribution=data.get("source_attribution", ""),
            is_frequently_cited=data.get("is_frequently_cited", False),
            allowed_in_advisory=data.get("allowed_in_advisory", True),
            allowed_in_verdict=data.get("allowed_in_verdict", True),
            tags=data.get("tags", []),
            note=data.get("note", ""),
        )
