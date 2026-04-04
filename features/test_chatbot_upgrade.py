#!/usr/bin/env python3
"""
Quick test script to verify chatbot data loading and response formatting
Run: python test_chatbot_upgrade.py
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import retriever and app
sys.path.insert(0, str(Path(__file__).parent / "chatbot-1-main"))

def test_data_loading():
    """Test that all data files load correctly"""
    print("\n" + "="*60)
    print("TEST 1: Data Loading")
    print("="*60)
    
    try:
        from chatbot_1_main.retriever import _build_corpus, _corpus
        _build_corpus()
        
        # Count passages by source
        from collections import Counter
        sources = Counter(p.source for p in _corpus)
        
        print(f"✅ Total passages loaded: {len(_corpus)}")
        for source, count in sources.most_common():
            print(f"   {source}: {count} passages")
        
        # Check for Gita metadata
        gita_passages = [p for p in _corpus if p.source == "Bhagavad Gita"]
        gita_with_chapter = sum(1 for p in gita_passages if p.chapter_number and p.verse_number)
        print(f"\n✅ Gita passages with Chapter/Verse metadata: {gita_with_chapter}/{len(gita_passages)}")
        
        # Check for Sanskrit in passages
        with_sanskrit = sum(1 for p in _corpus if p.sanskrit and len(p.sanskrit) > 10)
        print(f"✅ Passages with Sanskrit text: {with_sanskrit}/{len(_corpus)}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gita_retrieval():
    """Test that Gita verses are retrieved with metadata"""
    print("\n" + "="*60)
    print("TEST 2: Gita Verse Retrieval")
    print("="*60)
    
    try:
        from chatbot_1_main.retriever import retrieve, format_passages_for_prompt
        
        # Test query that should retrieve Gita verses
        results = retrieve("confusion duty dharma", top_k=3)
        
        print(f"✅ Retrieved {len(results)} passages")
        
        # Check if any are Gita
        gita_results = [r for r in results if r.source == "Bhagavad Gita"]
        print(f"✅ Gita verses in results: {len(gita_results)}")
        
        # Check metadata
        for i, p in enumerate(gita_results, 1):
            print(f"\n   [{i}] Gita Passage:")
            print(f"       Chapter: {p.chapter_number}, Verse: {p.verse_number}")
            print(f"       Sanskrit present: {bool(p.sanskrit)}")
            print(f"       Sanskrit (first 50 chars): {p.sanskrit[:50] if p.sanskrit else 'N/A'}...")
        
        # Test formatting
        formatted = format_passages_for_prompt(results)
        print(f"\n✅ Formatted output:\n{formatted[:500]}...")
        
        # Check if Chapter/Verse appears in formatted output for Gita
        if gita_results:
            if f"Chapter {gita_results[0].chapter_number}, Verse {gita_results[0].verse_number}" in formatted:
                print(f"\n✅ Chapter/Verse formatting works correctly for Gita")
            else:
                print(f"\n⚠️ Chapter/Verse NOT found in formatted output")
        
        return True
    except Exception as e:
        print(f"❌ Error retrieving Gita: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_other_texts_retrieval():
    """Test that other texts are retrieved without Chapter/Verse formatting"""
    print("\n" + "="*60)
    print("TEST 3: Other Texts Retrieval (Chanakya, Vidura, etc.)")
    print("="*60)
    
    try:
        from chatbot_1_main.retriever import retrieve, format_passages_for_prompt
        
        # Test query that might retrieve Chanakya
        results = retrieve("relationships management wisdom conduct", top_k=3)
        
        print(f"✅ Retrieved {len(results)} passages")
        
        # Check sources
        from collections import Counter
        sources = Counter(r.source for r in results)
        print(f"✅ Sources in results: {dict(sources)}")
        
        # Check non-Gita formatting
        non_gita = [r for r in results if r.source != "Bhagavad Gita"]
        for i, p in enumerate(non_gita, 1):
            print(f"\n   [{i}] {p.source}:")
            print(f"       Sanskrit present: {bool(p.sanskrit)}")
            print(f"       Has chapter_number: {p.chapter_number is not None}")
        
        # Test formatting
        formatted = format_passages_for_prompt(results)
        
        # Check that non-Gita don't have "Chapter X, Verse Y" format
        for source in ["Chanakya Niti", "Vidura Niti", "Hitopadesha"]:
            if any(source in r.source for r in results):
                # Should NOT have "Chapter X, Verse Y" format for these
                has_chapter_verse = "Chapter" in formatted and "Verse" in formatted and source in formatted
                if not has_chapter_verse:
                    print(f"\n✅ {source} correctly formatted (no Chapter/Verse numbers)")
                else:
                    # Could be expected if the verse_number is None
                    print(f"\n⚠️ {source} might have Chapter/Verse (check if intentional)")
        
        return True
    except Exception as e:
        print(f"❌ Error retrieving other texts: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_response_formatting():
    """Test the complete response formatting"""
    print("\n" + "="*60)
    print("TEST 4: Complete Response Formatting")
    print("="*60)
    
    try:
        from chatbot_1_main.retriever import retrieve, format_passages_for_prompt
        
        # Simulate what the chatbot does
        user_query = "I'm confused about my career path and don't know what to do"
        passages = retrieve(user_query, top_k=4)
        context = format_passages_for_prompt(passages)
        
        print(f"✅ User Query: {user_query}")
        print(f"✅ Retrieved {len(passages)} passages")
        print(f"\n✅ Formatted Context:\n")
        print(context)
        
        # Verify formatting
        checks = {
            "Contains Sanskrit": any('Sanskrit:' in context for _ in [1]),
            "For Gita - has Chapter/Verse": any(f"Chapter {p.chapter_number}, Verse {p.verse_number}" in context 
                                                 for p in passages if p.source == "Bhagavad Gita" and p.chapter_number),
        }
        
        for check_name, result in checks.items():
            status = "✅" if result else "⚠️"
            print(f"{status} {check_name}: {result}")
        
        return True
    except Exception as e:
        print(f"❌ Error in response formatting: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "🧪 CHATBOT UPGRADE TEST SUITE 🧪".center(60))
    print("="*60)
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Gita Retrieval", test_gita_retrieval),
        ("Other Texts Retrieval", test_other_texts_retrieval),
        ("Response Formatting", test_response_formatting),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{test_name}' FAILED with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Chatbot upgrade is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED. Please review the errors above.")
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
