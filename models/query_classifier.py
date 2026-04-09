"""
query_classifier.py — Emotion & Intent Detection
──────────────────────────────────────────────────
Classify user queries by emotional state and intent to enable
personalized verse selection.
"""

from dataclasses import dataclass
import re


@dataclass
class QueryClassification:
    """Classification result for a user query."""
    emotion_detected: str       # "confusion", "fear", "guilt", etc.
    intent: str                 # "decision", "understanding", "conflict", etc.
    keywords_matched: list      # Keywords found in query
    confidence: float           # 0.0 to 1.0 confidence


# Define emotion and intent markers
EMOTION_MARKERS = {
    "confusion": [
        "confused", "unsure", "lost", "torn", "unclear", "mixed", "puzzle",
        "bewildered", "perplexed", "undecided", "multiple paths"
    ],
    "fear": [
        "scared", "afraid", "anxiety", "anxious", "nervous", "terrified",
        "worry", "worried", "dread", "apprehensive", "frighten"
    ],
    "guilt": [
        "guilty", "ashamed", "shame", "regret", "remorse", "mistake",
        "failed", "failure", "wrong", "blame", "responsible"
    ],
    "anger": [
        "angry", "furious", "mad", "rage", "raged", "upset", "frustrated",
        "annoy", "offended", "unfair", "injustice", "dishonest"
    ],
    "seeking": [
        "seeking", "searching", "looking for", "advice", "guidance",
        "counsel", "help", "suggest", "wisdom", "teach"
    ],
    "joy": [
        "happy", "blessed", "grateful", "celebrate", "celebration",
        "excited", "joy", "delighted", "blessed", "grateful"
    ],
}

INTENT_MARKERS = {
    "decision": [
        "should", "which", "choose", "decide", "decision", "what to do",
        "way forward", "path", "option", "better", "or", "help me decide"
    ],
    "understanding": [
        "why", "what", "how", "meaning", "understand", "explain",
        "help me understand", "purpose", "reason", "significance"
    ],
    "conflict": [
        "torn", "opposing", "dilemma", "conflict", "both", "stuck",
        "versus", "vs", "between", "caught", "pressure"
    ],
    "gratitude": [
        "thank", "grateful", "appreciate", "appreciation", "thanks",
        "blessing", "blessed"
    ],
    "counsel": [
        "advise", "guide", "guidance", "teach", "teaching", "wisdom",
        "perspective", "view", "opinion"
    ],
}

# Domain detection
DOMAIN_MARKERS = {
    "career": [
        "job", "career", "work", "business", "startup", "company",
        "promotion", "position", "employment", "professional"
    ],
    "relationship": [
        "partner", "spouse", "marriage", "wife", "husband", "relationship",
        "family", "friend", "love", "parent", "mother", "father",
        "colleague", "friend"
    ],
    "ethical": [
        "right", "wrong", "moral", "ethics", "dharma", "truth",
        "dishonest", "cheat", "lie", "injustice", "fair", "honesty"
    ],
    "spiritual": [
        "soul", "spirit", "meditation", "god", "divine", "sacred",
        "yoga", "enlightenment", "consciousness", "spiritual"
    ],
    "personal": [
        "myself", "yourself", "i feel", "self", "personal", "identity",
        "confidence", "self-esteem", "self-worth"
    ],
}


def classify_query(user_query: str) -> QueryClassification:
    """
    Classify user query by emotion and intent.
    
    Uses keyword-based multi-label classification:
    1. Detect primary emotion
    2. Detect primary intent
    3. Detect domain (optional)
    4. Score confidence
    
    Args:
        user_query: User's message text
        
    Returns:
        QueryClassification with emotion, intent, keywords, confidence
    """
    
    query_lower = user_query.lower()
    keywords_matched = []
    
    # ── Emotion Detection ──────────────────────────────────────────────────
    detected_emotion = "neutral"
    max_emotion_matches = 0
    
    for emotion, markers in EMOTION_MARKERS.items():
        matches = sum(1 for m in markers if m in query_lower)
        if matches > max_emotion_matches:
            detected_emotion = emotion
            max_emotion_matches = matches
            keywords_matched.extend([m for m in markers if m in query_lower])
    
    # ── Intent Detection ───────────────────────────────────────────────────
    detected_intent = "counsel"  # Default
    max_intent_matches = 0
    
    for intent, markers in INTENT_MARKERS.items():
        matches = sum(1 for m in markers if m in query_lower)
        if matches > max_intent_matches:
            detected_intent = intent
            max_intent_matches = matches
            keywords_matched.extend([m for m in markers if m in query_lower])
    
    # ── Domain Detection (optional, not used in basic routing) ─────────────
    domain = "personal"
    for dom, markers in DOMAIN_MARKERS.items():
        if any(m in query_lower for m in markers):
            domain = dom
            break
    
    # ── Complexity Classification ──────────────────────────────────────────
    query_length = len(user_query.split())
    if query_length < 5:
        complexity = "casual"
    elif query_length < 20:
        complexity = "moderate"
    else:
        complexity = "profound"
    
    # ── Confidence Scoring ────────────────────────────────────────────────
    # More keyword matches = higher confidence
    unique_keywords = list(set(keywords_matched))
    confidence = min(len(unique_keywords) / 5.0, 1.0)
    
    return QueryClassification(
        emotion_detected=detected_emotion,
        intent=detected_intent,
        keywords_matched=unique_keywords,
        confidence=confidence,
    )


if __name__ == "__main__":
    # Quick test
    test_queries = [
        "I'm torn between my startup dream and supporting my family financially.",
        "I feel lost. What should I do with my life?",
        "How can I handle a dishonest colleague?",
        "Namaste.",
    ]
    
    for query in test_queries:
        result = classify_query(query)
        print(f"\nQuery: {query}")
        print(f"  Emotion: {result.emotion_detected}")
        print(f"  Intent: {result.intent}")
        print(f"  Confidence: {result.confidence:.2f}")
