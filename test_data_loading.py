#!/usr/bin/env python3
"""Diagnostic script to test data loading"""
import sys
import csv
import json
from pathlib import Path

# Fix encoding on Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Test Chatbot data
print("="*70)
print("TESTING CHATBOT DATA LOADING")
print("="*70)

chatbot_data_dir = Path("features/chatbot/data")
print(f"\nChecking directory: {chatbot_data_dir.resolve()}")
print(f"Exists: {chatbot_data_dir.exists()}")

if chatbot_data_dir.exists():
    files = list(chatbot_data_dir.glob("*"))
    print(f"Files found: {len(files)}")
    for f in files:
        print(f"  - {f.name} ({f.stat().st_size} bytes)")

# Test CSV loading
gita_file = chatbot_data_dir / "Bhagwad_Gita.csv"
if gita_file.exists():
    print(f"\nOK Gita CSV found: {gita_file}")
    try:
        with open(gita_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            print(f"  OK Loaded {len(rows)} rows")
            if rows:
                print(f"    First row keys: {list(rows[0].keys())}")
                print(f"    Sample: Chapter={rows[0].get('Chapter')}, Verse={rows[0].get('Verse')}")
    except Exception as e:
        print(f"  ERROR loading CSV: {e}")
else:
    print(f"\nERROR Gita CSV NOT found: {gita_file}")

# Test JSON loading
for json_file in ["hitopadesha.json", "chanakya.json", "vidura_niti.json"]:
    path = chatbot_data_dir / json_file
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    print(f"\nOK {json_file}: {len(data)} records")
                else:
                    print(f"\nOK {json_file}: {type(data)} with {len(data)} keys")
        except Exception as e:
            print(f"\nERROR {json_file}: {e}")
    else:
        print(f"\nERROR {json_file}: NOT FOUND")

print("\n" + "="*70)
print("TESTING RETRIEVER IMPORT")
print("="*70 + "\n")

try:
    sys.path.insert(0, "features/chatbot")
    from retriever import retrieve, _build_corpus, _tokenize
    print("OK Retriever imported successfully")
    
    print("\nBuilding corpus...")
    _build_corpus()
    print("OK Corpus built")
    
    print("\nTesting with sample queries:")
    queries = [
        "dharma duty",
        "action work",
        "karma"
    ]
    for query in queries:
        print(f"\n  Testing: '{query}'")
        results = retrieve(query, top_k=2)
        print(f"  Got {len(results)} results")
        for r in results[:1]:
            print(f"    - {r.source[:30]}: {r.text[:60]}")

except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    print("\nFull traceback:")
    print(traceback.format_exc())
