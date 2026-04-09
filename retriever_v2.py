"""
retriever_v2.py — Unified Retriever with Semantic + TF-IDF Fusion
──────────────────────────────────────────────────────────────────
Combines three layers:
1. Semantic intent mapping (emotion → verses)
2. TF-IDF keyword matching
3. VSD validation

Result: Relevant, verified verses guaranteed.
"""

import json
from pathlib import Path
from typing import List, Tuple, Dict
import math
import re

from models.vsd import ScriptureEntry, ConfidenceLevel
from models.query_classifier import classify_query
from models.verse_index import get_semantic_verses


class TFIDFRetriever:
    """Pure TF-IDF retrieval from scripture passages."""
    
    def __init__(self):
        self.passages: List[ScriptureEntry] = []
        self._token_cache: Dict[str, dict] = {}
    
    def build_corpus(self, entries: List[ScriptureEntry]):
        """Build searchable corpus from entries."""
        self.passages = entries
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize and clean text."""
        stop_words = {
            "a", "an", "the", "is", "it", "in", "of", "to", "and", "or", "for",
            "with", "that", "this", "as", "be", "by", "at", "from", "on", "are",
            "was", "were", "not", "but", "have", "has", "had", "do", "does", "did",
            "i", "you", "he", "she", "we", "they", "me", "him", "her", "us", "them",
            "my", "your", "his", "our", "their", "what", "how", "when", "where",
            "who", "which", "one", "if", "so", "all", "will", "can", "would", "could",
            "should", "also", "more", "very", "just", "said", "say", "see", "know",
            "get", "go", "come", "make", "take", "give", "well", "even", "after",
            "into", "dharma", "the", "your", "by",
        }
        
        words = re.findall(r"[a-z']+", text.lower())
        return [w for w in words if w not in stop_words and len(w) > 2]
    
    def _tfidf_scores(self, query_tokens: List[str]) -> List[float]:
        """Calculate TF-IDF score for each passage."""
        N = len(self.passages)
        if N == 0:
            return []
        
        # Build IDF
        df: Dict[str, int] = {}
        for passage in self.passages:
            search_text = (passage.translation + " " + passage.verse_id).lower()
            passage_tokens = set(self._tokenize(search_text))
            for token in passage_tokens:
                df[token] = df.get(token, 0) + 1
        
        # Calculate IDF for query tokens
        idf = {t: math.log((N + 1) / (df.get(t, 0) + 1)) for t in set(query_tokens)}
        
        # Score each passage
        scores = []
        for passage in self.passages:
            score = 0.0
            search_text = (passage.translation + " " + passage.verse_id).lower()
            passage_tokens = self._tokenize(search_text)
            token_counts = {}
            for t in passage_tokens:
                token_counts[t] = token_counts.get(t, 0) + 1
            
            for token in query_tokens:
                if token in token_counts:
                    tf = 1 + math.log(token_counts[token])
                    score += tf * idf.get(token, 0)
            
            scores.append(score)
        
        return scores
    
    def search(self, query: str, top_k: int = 4) -> List[Tuple[str, float]]:
        """Search corpus via TF-IDF."""
        if not self.passages:
            return []
        
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        
        scores = self._tfidf_scores(query_tokens)
        
        # Rank passages
        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Return top-k as (verse_id, score) tuples
        result = []
        for idx, score in ranked[:top_k]:
            if idx < len(self.passages) and score > 0:
                result.append((self.passages[idx].verse_id, score))
        
        return result


class UnifiedRetriever:
    """
    Unified retriever combining semantic + TF-IDF + VSD validation.
    """
    
    def __init__(self, vsd_path: str):
        self.vsd: Dict[str, ScriptureEntry] = {}
        self.tfidf = TFIDFRetriever()
        self._load_vsd(vsd_path)
        self.tfidf.build_corpus(list(self.vsd.values()))
    
    def _load_vsd(self, vsd_path: str):
        """Load VSD from JSON file."""
        vsd_file = Path(vsd_path)
        
        if not vsd_file.exists():
            print(f"⚠ VSD not found at {vsd_path}. Run scripts/build_vsd.py first.")
            return
        
        with open(vsd_file, encoding="utf-8") as f:
            vsd_json = json.load(f)
        
        for entry_data in vsd_json.get("entries", []):
            entry = ScriptureEntry.from_dict(entry_data)
            self.vsd[entry.verse_id] = entry
        
        print(f"✓ Loaded {len(self.vsd)} verses into VSD")
    
    def retrieve(self, user_query: str, top_k: int = 5) -> List[ScriptureEntry]:
        """
        Main retrieval pipeline: Semantic + TF-IDF + Validation.
        
        Args:
            user_query: User's original question
            top_k: Number of top verses to return
        
        Returns:
            List of verified ScriptureEntry objects
        """
        
        if not self.vsd:
            print("⚠ VSD is empty. Cannot retrieve.")
            return []
        
        # Step 1: Classify query
        classification = classify_query(user_query)
        
        # Step 2: Get semantic verses based on emotion+intent
        semantic_verses = get_semantic_verses(
            emotion=classification.emotion_detected,
            intent=classification.intent if classification.intent != "counsel" else None,
            top_k=3
        )
        
        # Step 3: Get TF-IDF matches
        tfidf_verses = self.tfidf.search(user_query, top_k=4)
        
        # Step 4: Fuse candidates
        candidates: Dict[str, float] = {}
        
        # Add semantic verses (weight: 1.0 — highest priority)
        for verse_id, sem_score in semantic_verses:
            if verse_id in self.vsd:
                candidates[verse_id] = sem_score * 1.0
        
        # Add TF-IDF verses (weight: 0.3 — lower priority but still useful)
        for verse_id, tfidf_score in tfidf_verses:
            if verse_id in self.vsd:
                if verse_id in candidates:
                    candidates[verse_id] += tfidf_score * 0.3
                else:
                    candidates[verse_id] = tfidf_score * 0.3
        
        # Step 5: Validate against VSD (only use usable entries)
        validated: List[Tuple[str, float]] = [
            (vid, score)
            for vid, score in candidates.items()
            if self.vsd[vid].is_usable()
        ]
        
        # Step 6: Sort by score and return top-k
        validated.sort(key=lambda x: x[1], reverse=True)
        
        result_entries = [self.vsd[vid] for vid, score in validated[:top_k]]
        
        return result_entries
    
    def get_verse(self, verse_id: str) -> ScriptureEntry | None:
        """Get a specific verse by ID."""
        return self.vsd.get(verse_id)


# Singleton retriever instance
_retriever_instance: UnifiedRetriever | None = None


def init_retriever(vsd_path: str = "data/vsd.json") -> UnifiedRetriever:
    """Initialize the global retriever instance."""
    global _retriever_instance
    _retriever_instance = UnifiedRetriever(vsd_path)
    return _retriever_instance


def get_retriever() -> UnifiedRetriever | None:
    """Get the global retriever instance."""
    return _retriever_instance


if __name__ == "__main__":
    # Test retrieval
    print("Testing Unified Retriever...")
    
    retriever = init_retriever("data/vsd.json")
    
    test_queries = [
        "I'm torn between my startup dream and supporting my family financially.",
        "I feel confused about which path to follow.",
        "How should I handle a dishonest colleague?",
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        results = retriever.retrieve(query, top_k=3)
        
        if results:
            for i, entry in enumerate(results, 1):
                print(f"  {i}. [{entry.verse_id}] {entry.source} — {entry.chapter_or_story}")
                print(f"     Confidence: {entry.confidence_level.value}")
        else:
            print("  ✗ No results (VSD may not be built)")
