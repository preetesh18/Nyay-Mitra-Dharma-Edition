"""
test_retriever_v2.py — Unit Tests for Unified Retriever v2.0
──────────────────────────────────────────────────────────────
"""

import pytest
import json
import tempfile
from pathlib import Path

from models.vsd import ScriptureEntry, ConfidenceLevel
from models.query_classifier import classify_query, QueryClassification
from models.verse_index import get_semantic_verses
from retriever_v2 import UnifiedRetriever, TFIDFRetriever


# ── Test QueryClassifier ───────────────────────────────────────────────────

class TestQueryClassifier:
    """Test emotion and intent detection."""
    
    def test_confusion_detection(self):
        """Test confusion emotion detection."""
        query = "I'm so confused about which path to follow in life."
        result = classify_query(query)
        assert result.emotion_detected == "confusion"
        assert isinstance(result, QueryClassification)
        assert result.confidence > 0
    
    def test_fear_detection(self):
        """Test fear emotion detection."""
        query = "I'm really scared of failing my startup."
        result = classify_query(query)
        assert result.emotion_detected == "fear"
    
    def test_guilt_detection(self):
        """Test guilt emotion detection."""
        query = "I feel guilty and ashamed about my mistakes."
        result = classify_query(query)
        assert result.emotion_detected == "guilt"
    
    def test_decision_intent(self):
        """Test decision intent detection."""
        query = "Should I take this job or start my own business?"
        result = classify_query(query)
        assert "decision" in result.intent.lower()
    
    def test_understanding_intent(self):
        """Test understanding intent detection."""
        query = "Why do people suffer? What is the meaning of life?"
        result = classify_query(query)
        assert result.intent == "understanding"
    
    def test_casual_greeting(self):
        """Test neutral classification for casual greeting."""
        query = "Hello, how are you?"
        result = classify_query(query)
        assert result.emotion_detected == "neutral"


# ── Test Semantic Verse Index ──────────────────────────────────────────────

class TestSemanticVerseIndex:
    """Test semantic verse mapping."""
    
    def test_confusion_verses(self):
        """Verify confusion maps to relevant verses."""
        verses = get_semantic_verses(emotion="confusion", top_k=2)
        verse_ids = [v[0] for v in verses]
        assert any("BG" in vid for vid in verse_ids)
        assert len(verses) > 0
    
    def test_fear_verses(self):
        """Verify fear maps to relevant verses."""
        verses = get_semantic_verses(emotion="fear", top_k=2)
        verse_ids = [v[0] for v in verses]
        # Should include BG 2.47 (detachment from results)
        assert any("2.47" in vid for vid in verse_ids), "BG 2.47 should be in fear verses"
    
    def test_passion_vs_duty_verses(self):
        """Verify passion vs duty maps to BG 3.35 (CRITICAL TEST)."""
        verses = get_semantic_verses(
            emotion="confusion",
            intent="decision_passion_vs_duty",
            top_k=3
        )
        verse_ids = [v[0] for v in verses]
        # CRITICAL: BG 3.35 MUST be included
        assert "BG-3.35" in verse_ids, "BG-3.35 (own dharma) must be in passion vs duty queries"


# ── Test Scripture Entry ───────────────────────────────────────────────────

class TestScriptureEntry:
    """Test VSD entry structure."""
    
    def test_entry_creation(self):
        """Test creating a scripture entry."""
        entry = ScriptureEntry(
            verse_id="BG-2.47",
            source="Bhagavad Gita",
            chapter_or_story="Chapter 2",
            verse_num="47",
            sanskrit="कर्मण्येवाधिकारस्ते...",
            transliteration="karmaṇy-evādhikāras te...",
            translation="You have a right to perform...",
            confidence_level=ConfidenceLevel.VERIFIED,
            source_attribution="Prabhupada",
        )
        
        assert entry.verse_id == "BG-2.47"
        assert entry.is_usable() == True
        assert entry.allowed_in_advisory == True
    
    def test_chanakya_moderate_confidence(self):
        """Test that Chanakya entries are marked as MODERATE, not VERIFIED."""
        entry = ScriptureEntry(
            verse_id="CN-1-5",
            source="Chanakya Niti",
            chapter_or_story="Chapter 1",
            verse_num="5",
            sanskrit="",  # Usually not available
            transliteration="",
            translation="A wicked wife, crooked friend...",
            confidence_level=ConfidenceLevel.MODERATE,  # KEY: Not VERIFIED
            source_attribution="Chanakya Niti (Interpreted)",
            allowed_in_verdict=False,  # Too interpretive for formal verdict
        )
        
        assert entry.confidence_level == ConfidenceLevel.MODERATE
        assert entry.is_usable() == True  # MODERATE is still usable
        assert entry.allowed_in_verdict == False
    
    def test_entry_serialization(self):
        """Test entry to/from dict."""
        entry = ScriptureEntry(
            verse_id="BG-3.35",
            source="Bhagavad Gita",
            chapter_or_story="Chapter 3",
            verse_num="35",
            sanskrit="श्रेयान्स्वधर्मो...",
            transliteration="śreyān svadharmo...",
            translation="Better own dharma...",
            confidence_level=ConfidenceLevel.VERIFIED,
            source_attribution="Prabhupada",
        )
        
        # Convert to dict
        data = entry.to_dict()
        assert data["verse_id"] == "BG-3.35"
        assert data["confidence_level"] == "verified"
        
        # Convert back
        reconstructed = ScriptureEntry.from_dict(data)
        assert reconstructed.verse_id == entry.verse_id
        assert reconstructed.confidence_level == entry.confidence_level


# ── Test TF-IDF Retriever ──────────────────────────────────────────────────

class TestTFIDFRetriever:
    """Test TF-IDF search functionality."""
    
    def test_tfidf_search(self):
        """Test TF-IDF search."""
        tfidf = TFIDFRetriever()
        
        # Create test corpus
        entries = [
            ScriptureEntry(
                verse_id="BG-1.1",
                source="Bhagavad Gita",
                chapter_or_story="Chapter 1",
                verse_num="1",
                sanskrit="",
                transliteration="",
                translation="The Kuru field is the field of dharma",
                confidence_level=ConfidenceLevel.VERIFIED,
                source_attribution="Test",
            ),
            ScriptureEntry(
                verse_id="BG-2.47",
                source="Bhagavad Gita",
                chapter_or_story="Chapter 2",
                verse_num="47",
                sanskrit="",
                transliteration="",
                translation="You have a right to action but never to results",
                confidence_level=ConfidenceLevel.VERIFIED,
                source_attribution="Test",
            ),
        ]
        
        tfidf.build_corpus(entries)
        
        # Search for "results"
        results = tfidf.search("action results", top_k=1)
        assert len(results) > 0
        # BG 2.47 should rank higher (contains "results")
        top_verse = results[0][0]
        assert top_verse == "BG-2.47"
    
    def test_tokenization(self):
        """Test text tokenization."""
        tfidf = TFIDFRetriever()
        
        text = "The wise and the foolish are different in the Bhagavad Gita"
        tokens = tfidf._tokenize(text)
        
        # Should filter stop words
        assert "the" not in tokens
        assert "and" not in tokens
        # Should keep meaningful words
        assert "wise" in tokens
        assert "foolish" in tokens


# ── Test Unified Retriever ────────────────────────────────────────────────

class TestUnifiedRetriever:
    """Test unified retriever with semantic + TF-IDF fusion."""
    
    @pytest.fixture
    def vsd_file(self):
        """Create a temporary VSD file for testing."""
        vsd_data = {
            "entries": [
                {
                    "verse_id": "BG-2.7",
                    "source": "Bhagavad Gita",
                    "chapter_or_story": "Chapter 2",
                    "verse_num": "7",
                    "sanskrit": "कार्पण्यदोषोपहतस्वभाव:",
                    "transliteration": "karpanya-dosa-upahatah",
                    "translation": "I am confused about my duty",
                    "confidence_level": "verified",
                    "source_attribution": "Prabhupada",
                    "allowed_in_advisory": True,
                    "allowed_in_verdict": True,
                    "tags": ["confusion", "decision"],
                },
                {
                    "verse_id": "BG-3.35",
                    "source": "Bhagavad Gita",
                    "chapter_or_story": "Chapter 3",
                    "verse_num": "35",
                    "sanskrit": "श्रेयान्स्वधर्मो विगुणः",
                    "transliteration": "sreyān svadharmo vigunaḥ",
                    "translation": "Better own dharma imperfectly than another's perfectly",
                    "confidence_level": "verified",
                    "source_attribution": "Prabhupada",
                    "allowed_in_advisory": True,
                    "allowed_in_verdict": True,
                    "tags": ["duty", "passion", "decision"],
                },
                {
                    "verse_id": "CN-1-5",
                    "source": "Chanakya Niti",
                    "chapter_or_story": "Chapter 1",
                    "verse_num": "5",
                    "sanskrit": "",
                    "transliteration": "",
                    "translation": "Avoid wicked wife, crooked friend, and snake in house",
                    "confidence_level": "moderate",
                    "source_attribution": "Chanakya (Interpreted)",
                    "allowed_in_advisory": True,
                    "allowed_in_verdict": False,
                    "tags": ["wisdom", "chanakya"],
                },
            ],
            "metadata": {"version": "2.0", "total_entries": 3}
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(vsd_data, f)
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        Path(temp_path).unlink()
    
    def test_retriever_loads_vsd(self, vsd_file):
        """Test that retriever loads VSD correctly."""
        retriever = UnifiedRetriever(vsd_file)
        assert len(retriever.vsd) == 3
        assert "BG-3.35" in retriever.vsd
    
    def test_retriever_retrieves_confusion_verses(self, vsd_file):
        """Test retriever finds confusion-related verses."""
        retriever = UnifiedRetriever(vsd_file)
        
        query = "I'm confused about which path to follow"
        results = retriever.retrieve(query, top_k=2)
        
        assert len(results) > 0
        # Semantic should prioritize BG-2.7 (confusion) or BG-3.35 (decision)
        result_ids = [r.verse_id for r in results]
        assert any(vid in result_ids for vid in ["BG-2.7", "BG-3.35"])
    
    def test_retriever_retrieves_passion_vs_duty(self, vsd_file):
        """Test retriever handles passion vs duty queries (CRITICAL TEST)."""
        retriever = UnifiedRetriever(vsd_file)
        
        query = "Should I follow my passion or my parents' expectations?"
        results = retriever.retrieve(query, top_k=3)
        
        result_ids = [r.verse_id for r in results]
        # CRITICAL: BG-3.35 MUST be retrieved for this query
        assert "BG-3.35" in result_ids, f"BG-3.35 not found. Got: {result_ids}"
    
    def test_chanakya_marked_moderate(self, vsd_file):
        """Test that Chanakya entries show MODERATE confidence."""
        retriever = UnifiedRetriever(vsd_file)
        
        chanakya_entry = retriever.get_verse("CN-1-5")
        assert chanakya_entry is not None
        assert chanakya_entry.confidence_level == ConfidenceLevel.MODERATE
        assert chanakya_entry.is_usable() == True  # Still usable
        assert chanakya_entry.allowed_in_verdict == False


# ── Integration Tests ──────────────────────────────────────────────────────

class TestIntegration:
    """End-to-end integration tests."""
    
    def test_query_to_retrieval_flow(self, vsd_file):
        """Test full flow from query to retrieval."""
        retriever = UnifiedRetriever(vsd_file)
        
        # User query
        query = "I'm torn between my dream and my family's expectations"
        
        # 1. Classify
        classification = classify_query(query)
        assert classification.emotion_detected in ["confusion", "fear"]
        
        # 2. Get semantic verses
        semantic = get_semantic_verses(
            emotion=classification.emotion_detected,
            intent=classification.intent
        )
        assert len(semantic) > 0
        
        # 3. Retrieve
        results = retriever.retrieve(query, top_k=3)
        assert len(results) > 0
        
        # 4. Verify all results are usable
        for entry in results:
            assert entry.is_usable() == True
            assert entry.confidence_level in [
                ConfidenceLevel.VERIFIED,
                ConfidenceLevel.HIGH,
                ConfidenceLevel.MODERATE,
            ]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
