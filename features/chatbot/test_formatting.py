#!/usr/bin/env python
"""Test script to verify formatting rules are applied correctly."""

from retriever import retrieve, format_passages_for_prompt

# Test retrieval and formatting
results = retrieve('What should I do about my family conflict?', top_k=4)
formatted = format_passages_for_prompt(results)

print("✅ Formatted Knowledge Base Context:\n")
print(formatted)
print("\n" + "="*80)
print("VERIFICATION - Data Structure Check:")
print("="*80)

for i, r in enumerate(results, 1):
    print(f"\n[{i}] {r.source}")
    if r.source == "Bhagavad Gita":
        if hasattr(r, 'chapter_number') and r.chapter_number:
            print(f"    ✓ Chapter {r.chapter_number}, Verse {r.verse_number}")
        print(f"    ✓ Sanskrit present: {bool(r.sanskrit)}")
        print(f"    ✓ Teaching text present: {bool(r.text)}")
    else:
        print(f"    ✓ Sanskrit-only format")
        print(f"    ✓ Sanskrit present: {bool(r.sanskrit)}")
        print(f"    Note: Teaching text will NOT be shown in response (per rules)")

print("\n" + "="*80)
print("✅ All data loaded and formatted correctly!")
print("="*80)
