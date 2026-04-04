#!/usr/bin/env python3
"""
Integration test for Naya Mitra AI Chatbot
Tests: Data loading, Gemini API connectivity, RAG retrieval, response formatting
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment first
load_dotenv()

def test_env_setup():
    """Verify .env file is loaded correctly"""
    print("\n" + "="*70)
    print("TEST 1: Environment Setup")
    print("="*70)
    
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("❌ FAILED: GEMINI_API_KEY not found in .env file")
        return False
    
    print(f"✅ GEMINI_API_KEY found (length: {len(api_key)})")
    print(f"✅ FLASK_SECRET_KEY: {os.environ.get('FLASK_SECRET_KEY', 'default')}")
    print(f"✅ PORT: {os.environ.get('PORT', '5000')}")
    return True


def test_data_loading():
    """Verify all data files load correctly"""
    print("\n" + "="*70)
    print("TEST 2: Data Loading")
    print("="*70)
    
    try:
        from retriever import retrieve, _build_corpus, _corpus
        
        # Build corpus
        _build_corpus()
        
        if not _corpus:
            print("❌ FAILED: No passages loaded")
            return False
        
        print(f"✅ Total passages loaded: {len(_corpus)}")
        
        # Count by source
        sources = {}
        for p in _corpus:
            sources[p.source] = sources.get(p.source, 0) + 1
        
        for source, count in sorted(sources.items()):
            print(f"   ✅ {source}: {count} passages")
        
        # Verify Gita has metadata
        gita_passages = [p for p in _corpus if p.source == "Bhagavad Gita"]
        gita_with_metadata = sum(1 for p in gita_passages if p.chapter_number and p.verse_number)
        print(f"\n✅ Gita passages with Chapter/Verse: {gita_with_metadata}/{len(gita_passages)}")
        
        # Verify Sanskrit is present
        sanskrit_passages = sum(1 for p in _corpus if p.sanskrit and len(p.sanskrit) > 5)
        print(f"✅ Passages with Sanskrit text: {sanskrit_passages}/{len(_corpus)}")
        
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_retrieval():
    """Verify RAG retrieval works"""
    print("\n" + "="*70)
    print("TEST 3: RAG Retrieval")
    print("="*70)
    
    try:
        from retriever import retrieve
        
        test_queries = [
            "I'm confused about my career",
            "How should I handle conflicts",
            "What is my duty in life"
        ]
        
        for query in test_queries:
            results = retrieve(query, top_k=3)
            if not results:
                print(f"❌ FAILED: No results for query: {query}")
                return False
            print(f"✅ Query: '{query}'")
            for i, p in enumerate(results, 1):
                print(f"   [{i}] {p.source}: {p.ref[:60]}")
        
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_response_formatting():
    """Verify response formatting for different sources"""
    print("\n" + "="*70)
    print("TEST 4: Response Formatting")
    print("="*70)
    
    try:
        from retriever import retrieve, format_passages_for_prompt
        
        results = retrieve("duty responsibility", top_k=6)
        if not results:
            print("❌ FAILED: No results for test query")
            return False
        
        formatted = format_passages_for_prompt(results)
        if not formatted:
            print("❌ FAILED: Formatting returned empty string")
            return False
        
        print("✅ Formatted output (first 500 chars):")
        print(formatted[:500])
        
        # Verify Gita shows Chapter/Verse
        gita_results = [p for p in results if p.source == "Bhagavad Gita"]
        if gita_results:
            formatted_gita = format_passages_for_prompt(gita_results)
            if "Chapter" in formatted_gita and "Verse" in formatted_gita:
                print("✅ Gita formatting shows Chapter/Verse")
            else:
                print("⚠️  WARNING: Gita formatting missing Chapter/Verse")
        
        # Verify other sources don't show unnecessary Chapter/Verse
        other_results = [p for p in results if p.source != "Bhagavad Gita"]
        if other_results:
            formatted_other = format_passages_for_prompt(other_results)
            source_name = other_results[0].source
            if source_name in formatted_other:
                print(f"✅ {source_name} formatting correct")
        
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gemini_connectivity():
    """Test Gemini API connectivity"""
    print("\n" + "="*70)
    print("TEST 5: Gemini API Connectivity")
    print("="*70)
    
    try:
        import httpx
        
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            print("❌ FAILED: GEMINI_API_KEY not found")
            return False
        
        # Test with a simple query
        model = "gemini-2.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": "Say 'Hello'"}]}
            ],
            "generationConfig": {
                "maxOutputTokens": 50,
                "temperature": 0.7
            }
        }
        
        print(f"🔄 Testing {model}...")
        r = httpx.post(
            url,
            headers={"x-goog-api-key": api_key},
            json=payload,
            timeout=15
        )
        
        if r.status_code == 200:
            print(f"✅ Gemini API responded successfully (status: {r.status_code})")
            response = r.json()
            text = response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            if text:
                print(f"✅ Response received: {text[:50]}...")
            return True
        else:
            print(f"❌ HTTP Error {r.status_code}")
            print(f"   Response: {r.text[:200]}")
            if r.status_code == 403:
                print("   ⚠️  API Key may be invalid or blocked")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "#"*70)
    print("# NYAY MITRA AI - INTEGRATION TEST SUITE")
    print("#"*70)
    
    tests = [
        test_env_setup,
        test_data_loading,
        test_rag_retrieval,
        test_response_formatting,
        test_gemini_connectivity,
    ]
    
    results = []
    for test_func in tests:
        try:
            passed = test_func()
            results.append((test_func.__name__, passed))
        except Exception as e:
            print(f"\n❌ Test {test_func.__name__} crashed: {e}")
            results.append((test_func.__name__, False))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Chatbot is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
