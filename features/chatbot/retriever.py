"""
retriever.py — Knowledge-base RAG for Nyay Mitra AI
─────────────────────────────────────────────────────
Loads all four sacred-text datasets into memory at startup.
retrieve(query, top_k) returns the most relevant passages via TF-IDF cosine
similarity so we never fabricate verses.
"""

import json
import math
import re
from pathlib import Path
from functools import lru_cache

DATA_DIR = Path(__file__).parent / "data"

# ── Passage data class ─────────────────────────────────────────────────────────

class Passage:
    __slots__ = ("source", "ref", "sanskrit", "transliteration", "text", "_tokens", "chapter_number", "verse_number")

    def __init__(self, source, ref, text, sanskrit="", transliteration="", chapter_number=None, verse_number=None):
        self.source = source          # "Bhagavad Gita" | "Hitopadesha" | …
        self.ref = ref                # "Chapter 2, Verse 47" | "Story: Tiger…"
        self.text = text              # English translation / teaching
        self.sanskrit = sanskrit
        self.transliteration = transliteration
        self.chapter_number = chapter_number  # For Gita: chapter number
        self.verse_number = verse_number      # For Gita: verse number
        self._tokens: dict = {}

    def search_text(self) -> str:
        return (self.text + " " + self.ref).lower()


# ── Tokeniser ──────────────────────────────────────────────────────────────────

_STOP = {
    "a","an","the","is","it","in","of","to","and","or","for","with","that",
    "this","as","be","by","at","from","on","are","was","were","not","but",
    "have","has","had","do","does","did","i","you","he","she","we","they",
    "me","him","her","us","them","my","your","his","our","their","what","how",
    "when","where","who","which","one","if","so","all","will","can","would",
    "could","should","also","more","very","just","said","say","see","know",
    "get","go","come","make","take","give","well","even","after","into"
}

def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z']+", text.lower())
    return [w for w in words if w not in _STOP and len(w) > 2]


def _tfidf_scores(query_tokens: list[str], corpus: list[Passage]) -> list[float]:
    """Return a cosine-like TF-IDF score for each passage against the query."""
    N = len(corpus)
    if N == 0:
        return []

    # Build IDF (document frequency)
    df: dict[str, int] = {}
    for p in corpus:
        if not p._tokens:
            p._tokens = {}
            tokens = _tokenize(p.search_text())
            for t in set(tokens):
                p._tokens[t] = tokens.count(t)
        for t in p._tokens:
            df[t] = df.get(t, 0) + 1

    idf = {t: math.log((N + 1) / (df.get(t, 0) + 1)) for t in set(query_tokens)}

    scores = []
    for p in corpus:
        score = 0.0
        for t in query_tokens:
            tf = p._tokens.get(t, 0)
            if tf:
                score += (1 + math.log(tf)) * idf.get(t, 0)
        scores.append(score)
    return scores


# ── Loaders ────────────────────────────────────────────────────────────────────

def _load_gita_csv(path: Path) -> list[Passage]:
    """Load Bhagavad Gita from CSV file with chapter, verse, Sanskrit shloka"""
    passages = []
    import csv
    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    chapter = row.get("Chapter", "").strip()
                    verse = row.get("Verse", "").strip()
                    shloka = row.get("Shloka", "").strip()
                    eng_meaning = row.get("EngMeaning", "").strip()
                    word_meaning = row.get("WordMeaning", "").strip()
                    transliteration = row.get("Transliteration", "").strip()
                    
                    if not eng_meaning or len(eng_meaning) < 30:
                        continue
                    
                    # Use EngMeaning as primary text, add WordMeaning as context
                    text = eng_meaning
                    if word_meaning and len(word_meaning) > 40:
                        text += " " + word_meaning[:300]
                    
                    ref = f"Bhagavad Gita Chapter {chapter}, Verse {verse}"
                    passages.append(Passage(
                        source="Bhagavad Gita",
                        ref=ref,
                        text=text[:500],
                        sanskrit=shloka,
                        transliteration=transliteration,
                        chapter_number=chapter,
                        verse_number=verse,
                    ))
                except Exception as e:
                    continue
    except Exception as e:
        print(f"Error loading Gita CSV: {e}")
    
    return passages


def _load_hitopadesha(path: Path) -> list[Passage]:
    passages = []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        
        for r in records:
            # Extract story information
            story_title = r.get("story_title", "").strip()
            story_id = r.get("story_id", "")
            verses = r.get("verses", [])
            
            # Collect verse translations
            verse_texts = []
            sanskrit_texts = []
            for v in verses:
                trans = v.get("translation", "").strip()
                sanskrits = v.get("sanskrit", "").strip()
                if trans:
                    verse_texts.append(trans)
                if sanskrits:
                    sanskrit_texts.append(sanskrits)
            
            if not verse_texts:
                continue
            
            # Combine all verses into one passage
            full_text = " ".join(verse_texts).strip()
            if len(full_text) < 80:
                continue
            
            # Use first Sanskrit verse as main shloka if available
            main_sanskrit = sanskrit_texts[0] if sanskrit_texts else ""
            
            ref = f"Hitopadesha: {story_title}" if story_title else f"Hitopadesha {story_id}"
            passages.append(Passage(
                source="Hitopadesha",
                ref=ref,
                text=full_text[:500],
                sanskrit=main_sanskrit,
            ))
    except Exception as e:
        print(f"Error loading Hitopadesha JSON: {e}")
    
    return passages


def _load_vidura(path: Path) -> list[Passage]:
    passages = []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        
        for r in records:
            # Extract verse information from actual JSON structure
            verse_id = r.get("verse_id", "")
            sequence = r.get("sequence_number", "")
            sanskrit_shloka = r.get("sanskrit_shloka", "").strip()
            translation = r.get("translation", "").strip()
            context = r.get("context", "").strip()
            
            # Use translation as the main content
            text = translation if translation else context
            
            if not text or len(text) < 80:
                continue
            
            # Extract only Devanagari Sanskrit from shloka if available
            sanskrit_only = _extract_devanagari_only(sanskrit_shloka) if sanskrit_shloka else ""
            
            ref = f"Vidura Niti {verse_id}" if verse_id else "Vidura Niti"
            passages.append(Passage(
                source="Vidura Niti",
                ref=ref,
                text=text[:500],
                sanskrit=sanskrit_only,
            ))
    except Exception as e:
        print(f"Error loading Vidura Niti JSON: {e}")
    
    return passages


def _load_chanakya(path: Path) -> list[Passage]:
    passages = []
    try:
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        
        for r in records:
            chapter = r.get("chapter", "")
            verse = r.get("verse", "")
            shloka = r.get("shloka", "").strip()
            meaning = r.get("meaning", "").strip()
            
            if not meaning or len(meaning) < 80:
                continue
            
            # Extract only the Devanagari Sanskrit part (filter out transliteration)
            sanskrit_only = _extract_devanagari_only(shloka) if shloka else ""
            
            # Use meaning as primary text
            text = meaning
            
            ref = f"Chanakya Niti Chapter {chapter}, Verse {verse}" if chapter and verse else "Chanakya Niti"
            passages.append(Passage(
                source="Chanakya Niti",
                ref=ref,
                text=text[:500],
                sanskrit=sanskrit_only if sanskrit_only else "",
            ))
    except Exception as e:
        print(f"Error loading Chanakya Niti JSON: {e}")
    
    return passages


# ── Corpus singleton ───────────────────────────────────────────────────────────

_corpus: list[Passage] = []


def _build_corpus():
    global _corpus
    if _corpus:
        return
    
    # Load from new data files
    _corpus += _load_gita_csv(DATA_DIR / "Bhagwad_Gita.csv")
    _corpus += _load_hitopadesha(DATA_DIR / "hitopadesha.json")
    _corpus += _load_vidura(DATA_DIR / "vidura_niti.json")
    _corpus += _load_chanakya(DATA_DIR / "chanakya.json")
    
    print(f"✅ Corpus loaded: {len(_corpus)} passages from all sources")


# ── Public API ─────────────────────────────────────────────────────────────────

def retrieve(query: str, top_k: int = 6) -> list[Passage]:
    """Return up to `top_k` passages most relevant to the query."""
    _build_corpus()
    tokens = _tokenize(query)
    print(f"[DEBUG retrieve] Query: '{query}' -> Tokens: {tokens}", flush=True)
    if not tokens:
        print(f"[DEBUG retrieve] No tokens extracted, returning empty", flush=True)
        return []
    scores = _tfidf_scores(tokens, _corpus)
    print(f"[DEBUG retrieve] Got {len(scores)} scores, non-zero: {sum(1 for s in scores if s > 0)}", flush=True)
    if scores:
        print(f"[DEBUG retrieve] Score range: min={min(scores):.4f}, max={max(scores):.4f}", flush=True)

    # Apply 2x boost for passages with proper Devanagari Sanskrit so they
    # consistently outrank raw passages that have no verse text.
    boosted = [
        (score * (2.0 if _has_devanagari(p.sanskrit) else 1.0), p)
        for score, p in zip(scores, _corpus)
    ]
    ranked = sorted(boosted, key=lambda x: x[0], reverse=True)

    # Ensure we draw from at least 2 different sources when possible
    seen_sources: dict[str, int] = {}
    results: list[Passage] = []
    
    # First pass - try to get results with score > 0
    for score, passage in ranked:
        if score <= 0:
            continue  # Skip zero scores but don't break
        src_count = seen_sources.get(passage.source, 0)
        if src_count >= 2:
            continue  # cap per-source at 2 to keep diversity
        seen_sources[passage.source] = src_count + 1
        results.append(passage)
        if len(results) >= top_k:
            break
    
    # If we got no results (rare edge case), return top passages anyway
    if not results:
        print(f"[DEBUG] No score-matched passages, returning top passages anyway", flush=True)
        seen_sources = {}
        for score, passage in ranked[:top_k * 3]:  # Look at more candidates
            src_count = seen_sources.get(passage.source, 0)
            if src_count >= 2:
                continue
            seen_sources[passage.source] = src_count + 1
            results.append(passage)
            if len(results) >= top_k:
                break

    print(f"[DEBUG retrieve] Returning {len(results)} results", flush=True)

    # Guarantee at least one Sanskrit-bearing passage is present.
    # If none made it in, swap in the highest-scoring Sanskrit passage.
    if results and not any(_has_devanagari(p.sanskrit) for p in results):
        for score, passage in ranked:
            if _has_devanagari(passage.sanskrit):
                results[-1] = passage  # replace lowest-ranked slot
                break

    return results


def _extract_devanagari_only(text: str) -> str:
    """Extract only the Devanagari Sanskrit part from mixed Sanskrit+Transliteration text.
    
    Chanakya/Vidura shlokas typically have format:
    [Devanagari Sanskrit lines]
    [possibly blank line or spaces]
    [Latin transliteration lines with lowercase latin + diacritics]
    
    This function returns only the Devanagari part.
    """
    if not text:
        return ""
    
    lines = text.split("\n")
    devanagari_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:  # Skip empty lines
            continue
        
        # Check if line starts with lowercase Latin letter (indicating transliteration)
        # OR if it's mostly Latin characters (transliteration)
        first_char = stripped[0] if stripped else ''
        
        # If it starts with lowercase letter OR contains mostly Latin chars, it's transliteration
        if first_char.islower():
            # This is likely the start of transliteration, stop here
            break
        
        # Count Devanagari characters
        devanagari_count = sum(1 for c in line if '\u0900' <= c <= '\u097F')
        
        # If line has significant Devanagari content, include it
        if devanagari_count > 0:
            devanagari_lines.append(stripped)
    
    return "\n".join(devanagari_lines) if devanagari_lines else text


def _has_devanagari(text: str) -> bool:
    """Return True if text contains at least one Unicode Devanagari character."""
    return any('\u0900' <= c <= '\u097F' for c in text)


def format_passages_for_prompt(passages: list[Passage]) -> str:
    """Format retrieved passages as structured context for the LLM prompt.
    
    STRICT FORMATTING RULES (DO NOT DEVIATE):
    
    **FOR BHAGAVAD GITA ONLY:**
    - MUST show: Chapter X, Verse Y with Sanskrit Shloka
    - MUST include the transliteration if available
    - Format: "Bhagavad Gita | Chapter X, Verse Y"
    
    **FOR ALL OTHER TEXTS (Chanakya Niti, Vidura Niti, Hitopadesha):**
    - Show ONLY the source name and Sanskrit shloka (if available in Devanagari)
    - NEVER show chapter/verse numbers for non-Gita texts
    - NEVER show English meaning or teaching for non-Gita texts
   - ONLY show Sanskrit if it contains actual Devanagari characters
    - Format: "[Source Name]: Sanskrit text"
    """
    if not passages:
        return ""
    
    lines = ["=== RETRIEVED KNOWLEDGE BASE PASSAGES ===\n"]
    
    for i, p in enumerate(passages, 1):
        if p.source == "Bhagavad Gita":
            # ─── BHAGAVAD GITA FORMAT ───
            # ALWAYS include Chapter and Verse
            if p.chapter_number and p.verse_number:
                lines.append(f"[{i}] Bhagavad Gita | Chapter {p.chapter_number}, Verse {p.verse_number}")
            else:
                lines.append(f"[{i}] {p.ref}")
            
            # ALWAYS include Sanskrit/Shloka
            if p.sanskrit and _has_devanagari(p.sanskrit):
                lines.append(f"    Sanskrit Shloka: {p.sanskrit}")
            
            # Include transliteration if available
            if p.transliteration and p.transliteration.strip():
                lines.append(f"    Transliteration: {p.transliteration}")
            
            # Include teaching/meaning
            if p.text:
                lines.append(f"    Teaching: {p.text[:300]}")
        
        else:
            # ─── NON-GITA TEXT FORMAT (Chanakya, Vidura, Hitopadesha) ───
            # ONLY show source name and Sanskrit
            lines.append(f"[{i}] {p.source}")
            
            # ONLY include Sanskrit if it contains Devanagari - otherwise skip
            if p.sanskrit and _has_devanagari(p.sanskrit):
                lines.append(f"    {p.sanskrit}")
            # If no Devanagari, don't show Sanskrit at all
        
        lines.append("")
    
    lines.append("=== END OF KNOWLEDGE BASE ===\n")
    lines.append("📌 FORMATTING RULES FOR RESPONSE:\n")
    lines.append("• Bhagavad Gita: ALWAYS cite Chapter X, Verse Y with Sanskrit Shloka\n")
    lines.append("• Other Texts: Show ONLY source name and Sanskrit (if available in Devanagari)\n")
    lines.append("• NEVER fabricate verses not present in the knowledge base\n")
    
    return "\n".join(lines)


# Quick self-test
if __name__ == "__main__":
    results = retrieve("I feel depressed and lost in life", top_k=6)
    print(f"Got {len(results)} passages:")
    for p in results:
        print(f"  [{p.source}] {p.ref}: {p.text[:80]}…")
