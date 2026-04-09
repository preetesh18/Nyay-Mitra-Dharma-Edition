"""
build_vsd.py — Build Verified Scripture Database from Existing Data
────────────────────────────────────────────────────────────────────
Converts existing CSV/JSON data into VSD (Verified Scripture Database) format.
Run this script once to populate data/vsd.json
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from models.vsd import ScriptureEntry, ConfidenceLevel


def build_vsd_from_existing_data(source_dir: str = "features/chatbot/data", output_path: str = "data/vsd.json"):
    """
    Build VSD from existing data files.
    
    Processes:
    - Bhagavad_Gita.csv → ConfidenceLevel.VERIFIED
    - chanakya.json → ConfidenceLevel.MODERATE (interpreted)
    - hitopadesha.json → ConfidenceLevel.HIGH
    - vidura_niti.json → ConfidenceLevel.HIGH
    """
    
    source_dir = Path(source_dir)
    entries = []
    
    # ────────────────────────────────────────────────────────────────────
    # 1. Bhagavad Gita from CSV
    # ────────────────────────────────────────────────────────────────────
    print("Processing Bhagavad Gita CSV...")
    gita_csv = source_dir / "Bhagwad_Gita.csv"
    
    if gita_csv.exists():
        with open(gita_csv, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    chapter = row.get("Chapter", "?").strip()
                    verse = row.get("Verse", "?").strip()
                    verse_id = f"BG-{chapter}.{verse}"
                    
                    entry = ScriptureEntry(
                        verse_id=verse_id,
                        source="Bhagavad Gita",
                        chapter_or_story=f"Chapter {chapter}",
                        verse_num=verse,
                        sanskrit=row.get("Shloka", "").strip(),
                        transliteration=row.get("Transliteration", "").strip(),
                        translation=row.get("EngMeaning", "").strip(),
                        confidence_level=ConfidenceLevel.VERIFIED,
                        source_attribution="Prabhupada/Standard Translation",
                        is_frequently_cited=False,
                        allowed_in_advisory=True,
                        allowed_in_verdict=True,
                        tags=["gita", "verse"],
                        note="Bhagavad Gita CSV - Prabhupada aligned translation",
                    )
                    entries.append(entry)
                except Exception as e:
                    print(f"  ⚠ Skipped BG {chapter}.{verse}: {str(e)}")
    
    print(f"  ✓ Loaded {len([e for e in entries if 'gita' in e.tags])} Gita verses")
    
    # ────────────────────────────────────────────────────────────────────
    # 2. Chanakya Niti from JSON (mark as MODERATE - interpreted)
    # ────────────────────────────────────────────────────────────────────
    print("Processing Chanakya Niti JSON...")
    chanakya_json = source_dir / "chanakya.json"
    
    if chanakya_json.exists():
        try:
            with open(chanakya_json, encoding="utf-8") as f:
                chanakya_data = json.load(f)
            
            for item in chanakya_data:
                try:
                    chapter = item.get("chapter", "?")
                    verse = item.get("verse", "?")
                    verse_id = f"CN-{chapter}-{verse}"
                    
                    entry = ScriptureEntry(
                        verse_id=verse_id,
                        source="Chanakya Niti",
                        chapter_or_story=f"Chapter {chapter}",
                        verse_num=str(verse),
                        sanskrit=item.get("shloka", "").strip(),
                        transliteration="",  # Usually not available
                        translation=item.get("meaning", "").strip(),
                        confidence_level=ConfidenceLevel.MODERATE,  # ← KEY: Interpreted
                        source_attribution="Chanakya Niti (Interpreted Wisdom)",
                        is_frequently_cited=False,
                        allowed_in_advisory=True,
                        allowed_in_verdict=False,  # Too interpretive for formal verdict
                        tags=["chanakya", "wisdom", "niti"],
                        note="This entry is modern interpretation. Confidence: MODERATE",
                    )
                    entries.append(entry)
                except Exception as e:
                    print(f"  ⚠ Skipped Chanakya {chapter}-{verse}: {str(e)}")
            
            print(f"  ✓ Loaded {len([e for e in entries if 'chanakya' in e.tags and e.verse_id.startswith('CN-')])} Chanakya entries")
        
        except json.JSONDecodeError as e:
            print(f"  ✗ Failed to parse Chanakya JSON: {e}")
    
    # ────────────────────────────────────────────────────────────────────
    # 3. Hitopadesha from JSON
    # ────────────────────────────────────────────────────────────────────
    print("Processing Hitopadesha JSON...")
    hitopadesha_json = source_dir / "hitopadesha.json"
    
    if hitopadesha_json.exists():
        try:
            with open(hitopadesha_json, encoding="utf-8") as f:
                hitopadesha_data = json.load(f)
            
            for item in hitopadesha_data:
                try:
                    story_id = item.get("story_id", f"H-{item.get('story_number', '?')}")
                    story_title = item.get("story_title", "Untitled Story")
                    
                    # Collect all verse translations into one entry per story
                    verses = item.get("verses", [])
                    verse_translations = [v.get("translation", "") for v in verses if v.get("translation")]
                    full_text = " ".join(verse_translations)
                    
                    if len(full_text.strip()) > 50:  # Only include if substantial
                        entry = ScriptureEntry(
                            verse_id=story_id,
                            source="Hitopadesha",
                            chapter_or_story=f"Story: {story_title}",
                            verse_num=story_id,
                            sanskrit="",  # Not available in source
                            transliteration="",
                            translation=full_text[:800],  # Truncate at 800 chars
                            confidence_level=ConfidenceLevel.HIGH,
                            source_attribution="Hitopadesha (Standard Translation)",
                            is_frequently_cited=False,
                            allowed_in_advisory=True,
                            allowed_in_verdict=True,
                            tags=["hitopadesha", "story", "moral"],
                            note=f"Hitopadesha Tale: {story_title}",
                        )
                        entries.append(entry)
                except Exception as e:
                    print(f"  ⚠ Skipped Hitopadesha story: {str(e)}")
            
            print(f"  ✓ Loaded {len([e for e in entries if 'hitopadesha' in e.tags])} Hitopadesha stories")
        
        except json.JSONDecodeError as e:
            print(f"  ✗ Failed to parse Hitopadesha JSON: {e}")
    
    # ────────────────────────────────────────────────────────────────────
    # 4. Vidura Niti from JSON
    # ────────────────────────────────────────────────────────────────────
    print("Processing Vidura Niti JSON...")
    vidura_json = source_dir / "vidura_niti.json"
    
    if vidura_json.exists():
        try:
            with open(vidura_json, encoding="utf-8") as f:
                vidura_data = json.load(f)
            
            for item in vidura_data:
                try:
                    verse_id = item.get("verse_id", "VN-?")
                    translation = item.get("translation", "").strip()
                    context = item.get("context", "").strip()
                    
                    if len(translation) > 50:  # Only include substantial entries
                        entry = ScriptureEntry(
                            verse_id=verse_id,
                            source="Vidura Niti",
                            chapter_or_story="Vidura's Teachings (Mahabharata)",
                            verse_num=verse_id,
                            sanskrit=item.get("sanskrit_shloka", "").strip(),
                            transliteration="",
                            translation=translation,
                            confidence_level=ConfidenceLevel.HIGH,
                            source_attribution="Vidura Niti (KM Ganguli)",
                            is_frequently_cited=False,
                            allowed_in_advisory=True,
                            allowed_in_verdict=True,
                            tags=["vidura", "niti", "teaching"],
                            note=f"Context: {context}" if context else "",
                        )
                        entries.append(entry)
                except Exception as e:
                    print(f"  ⚠ Skipped Vidura {verse_id}: {str(e)}")
            
            print(f"  ✓ Loaded {len([e for e in entries if 'vidura' in e.tags])} Vidura Niti entries")
        
        except json.JSONDecodeError as e:
            print(f"  ✗ Failed to parse Vidura JSON: {e}")
    
    # ────────────────────────────────────────────────────────────────────
    # Build and save VSD
    # ────────────────────────────────────────────────────────────────────
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    vsd = {
        "entries": [e.to_dict() for e in entries],
        "metadata": {
            "version": "2.0",
            "last_updated": datetime.now().isoformat(),
            "total_entries": len(entries),
            "verified_count": sum(1 for e in entries if e.confidence_level == ConfidenceLevel.VERIFIED),
            "high_count": sum(1 for e in entries if e.confidence_level == ConfidenceLevel.HIGH),
            "moderate_count": sum(1 for e in entries if e.confidence_level == ConfidenceLevel.MODERATE),
            "source_breakdown": {
                "Bhagavad Gita": len([e for e in entries if e.source == "Bhagavad Gita"]),
                "Chanakya Niti": len([e for e in entries if e.source == "Chanakya Niti"]),
                "Hitopadesha": len([e for e in entries if e.source == "Hitopadesha"]),
                "Vidura Niti": len([e for e in entries if e.source == "Vidura Niti"]),
            }
        }
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(vsd, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ VSD BUILT SUCCESSFULLY")
    print(f"  Location: {output_path}")
    print(f"  Total Entries: {len(entries)}")
    print(f"  Verified: {vsd['metadata']['verified_count']}")
    print(f"  High: {vsd['metadata']['high_count']}")
    print(f"  Moderate: {vsd['metadata']['moderate_count']}")
    print(f"  Breakdown: {vsd['metadata']['source_breakdown']}")
    
    return output_path


if __name__ == "__main__":
    build_vsd_from_existing_data()
