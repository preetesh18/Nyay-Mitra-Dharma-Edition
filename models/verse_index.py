"""
verse_index.py — Semantic Verse Mapping
─────────────────────────────────────────
Maps emotional states and intents to relevant scripture verses.
This layer ensures that key verses like BG 3.35 (passion vs duty)
are always retrieved for matching queries.
"""

from typing import List, Tuple


class SemanticVerseIndexLookup:
    """
    Semantic verse index for intent-driven retrieval.
    
    Maps (emotion, intent) → [(verse_id, relevance_score), ...]
    """
    
    # Complete semantic verse index
    # Format: emotion/intent key → list of (verse_id, score, reason)
    SEMANTIC_INDEX = {
        # Emotional state: CONFUSION
        "confusion": [
            ("BG-2.7", 0.95, "Arjuna expresses confusion, surrenders for guidance"),
            ("BG-3.2", 0.88, "Krishna: Why are you troubled?"),
            ("BG-18.63", 0.80, "Confused about dharma path"),
        ],
        
        # Emotional state: FEAR
        "fear": [
            ("BG-2.47", 0.95, "Detachment from results reduces fear"),
            ("BG-3.30", 0.90, "Surrender fear to me (Krishna)"),
            ("BG-4.10", 0.88, "Those freed from fear find peace"),
            ("BG-15.5", 0.82, "Humility and fearlessness"),
        ],
        
        # Emotional state: GUILT / REGRET
        "guilt": [
            ("BG-4.36", 0.95, "Fire of knowledge burns all karma"),
            ("BG-9.30", 0.92, "Even sinners find redemption through devotion"),
            ("BG-18.66", 0.90, "Surrender all to me and be freed of all sin"),
            ("BG-3.31", 0.85, "Those who follow my teaching are freed from karma"),
        ],
        
        # Emotional state: ANGER
        "anger": [
            ("BG-2.56", 0.95, "Equipoise in pleasure and pain"),
            ("BG-16.21", 0.92, "Control of anger and ego"),
            ("BG-3.39", 0.88, "Lust and anger cloud judgment"),
            ("BG-5.26", 0.85, "Equanimity toward gain and loss"),
        ],
        
        # Intent: DECISION-MAKING (Passion vs Duty)
        "decision_passion_vs_duty": [
            ("BG-3.35", 0.99, "CRITICAL: Better own dharma imperfectly than another's perfectly"),
            ("BG-18.48", 0.96, "Engage in your nature-born duty"),
            ("BG-3.25", 0.92, "Act according to your nature"),
            ("BG-2.31", 0.88, "Svadharma (own duty) is glorious"),
        ],
        
        # Intent: DECISION-MAKING (Fear of Failure)
        "decision_fear_of_failure": [
            ("BG-2.47", 0.97, "Not entitled to fruits; attachment causes fear"),
            ("BG-3.21", 0.94, "Lead by example; your actions set standard"),
            ("BG-4.23", 0.91, "Act without attachment to results"),
            ("BG-2.38", 0.89, "Equipoise in victory and defeat"),
        ],
        
        # Intent: UNDERSTANDING (General Purpose)
        "understanding": [
            ("BG-2.2", 0.90, "Understanding true nature of self"),
            ("BG-7.1", 0.88, "Knowledge and realization"),
            ("BG-13.1", 0.85, "Understanding the field and the knower"),
        ],
        
        # Intent: CONFLICT-RESOLUTION
        "conflict": [
            ("BG-3.21", 0.95, "Your actions set example for others"),
            ("BG-5.25", 0.90, "Peace through control of senses"),
            ("BG-6.9", 0.87, "Friend is higher than stranger"),
            ("BG-2.11", 0.85, "Grieve not the inevitable"),
        ],
        
        # Intent: RELATIONSHIP / FAMILY
        "relationship": [
            ("BG-3.21", 0.93, "Your conduct sets standard"),
            ("BG-12.18-19", 0.90, "Same to friend and foe; dharmic relationships"),
            ("BG-2.11", 0.85, "Accept loss and separation as natural"),
            ("BG-6.9", 0.82, "Higher duty to self sometimes requires distance"),
        ],
        
        # Intent: CAREER / WORK
        "career": [
            ("BG-3.35", 0.96, "Follow your nature in work"),
            ("BG-18.47-49", 0.94, "Work aligned with one's nature"),
            ("BG-3.21", 0.90, "Excellence in work leads by example"),
            ("BG-2.47", 0.88, "Do duty without attachment to results"),
        ],
        
        # Intent: RESPONSIBILITY / DUTY
        "responsibility": [
            ("BG-3.21", 0.95, "Your actions influence others"),
            ("BG-2.47", 0.92, "Right to action, not to fruits"),
            ("BG-18.42-44", 0.90, "Duty according to birth/nature"),
            ("BG-9.23", 0.85, "Those who worship with devotion serve all"),
        ],
        
        # Intent: SELF-WORTH / CONFIDENCE
        "self_worth": [
            ("BG-15.10", 0.93, "All beings contain me (divine)"),
            ("BG-10.8", 0.91, "I am source of all creation"),
            ("BG-13.3", 0.88, "Know thyself as eternal"),
            ("BG-2.22", 0.85, "Soul unborn, eternal, changeless"),
        ],
        
        # Chanakya Niti: WISDOM / LEADERSHIP
        "chanakya_wisdom": [
            ("CN-1-5", 0.90, "Avoid wicked wife, crooked friends, saucy servants"),
            ("CN-1-6", 0.88, "Save money for hard times; save soul above all"),
            ("CN-1-1", 0.85, "Wisdom from all scriptures"),
        ],
    }
    
    def get_verses(self, emotion: str = None, intent: str = None, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Retrieve top verses for given emotion/intent combination.
        
        Args:
            emotion: Detected emotion ("confusion", "fear", "guilt", etc.)
            intent: Detected intent ("decision", "understanding", etc.)
            top_k: Number of top verses to return
        
        Returns:
            List of (verse_id, relevance_score) tuples, sorted by score
        """
        
        candidates = {}
        
        # Always check for specific combined keys first
        if emotion and intent:
            combined_key = f"{emotion}_{intent}"
            if combined_key in self.SEMANTIC_INDEX:
                for verse_id, score, reason in self.SEMANTIC_INDEX[combined_key]:
                    candidates[verse_id] = score * 1.2  # Boost combined matches
        
        # Then add individual emotion matches (weight: 1.0)
        if emotion and emotion in self.SEMANTIC_INDEX:
            for verse_id, score, reason in self.SEMANTIC_INDEX[emotion]:
                candidates[verse_id] = max(candidates.get(verse_id, 0), score)
        
        # Then add individual intent matches (weight: 1.0)
        if intent and intent in self.SEMANTIC_INDEX:
            for verse_id, score, reason in self.SEMANTIC_INDEX[intent]:
                candidates[verse_id] = max(candidates.get(verse_id, 0), score)
        
        # Sort by score and return top-k
        ranked = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
    
    def lookup_verse_reason(self, verse_id: str) -> str:
        """Get the reason why a verse is relevant (for debugging/explanation)."""
        for verses_in_category in self.SEMANTIC_INDEX.values():
            for vid, score, reason in verses_in_category:
                if vid == verse_id:
                    return reason
        return "Verse matched via TF-IDF fallback"


# Singleton instance
_semantic_index = SemanticVerseIndexLookup()


def get_semantic_verses(emotion: str = None, intent: str = None, top_k: int = 3) -> List[Tuple[str, float]]:
    """Convenience function to access semantic index."""
    return _semantic_index.get_verses(emotion=emotion, intent=intent, top_k=top_k)


if __name__ == "__main__":
    # Test semantic lookup
    print("Testing Semantic Verse Index...")
    print("\n1. Passion vs Duty (intention-based):")
    verses = get_semantic_verses(emotion="confusion", intent="decision_passion_vs_duty", top_k=3)
    for verse_id, score in verses:
        print(f"  {verse_id}: {score:.2f}")
    
    print("\n2. Fear (emotion-based):")
    verses = get_semantic_verses(emotion="fear", top_k=3)
    for verse_id, score in verses:
        print(f"  {verse_id}: {score:.2f}")
    
    print("\n3. Fear of Failure (combined):")
    verses = get_semantic_verses(emotion="fear", intent="decision_fear_of_failure", top_k=3)
    for verse_id, score in verses:
        print(f"  {verse_id}: {score:.2f}")
