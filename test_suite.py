#!/usr/bin/env python3
"""
Operational Acceptance Testing (OAT) & Stress Testing Suite
For Nyay Mitra Chatbot and Dharma Verdict systems
"""

import asyncio
import json
import time
import httpx
from datetime import datetime
import statistics

# Configuration
CHATBOT_URL = "https://chatbot-two-sigma-56.vercel.app"
VERDICT_URL = "https://dharmaverdict.vercel.app"
TIMEOUT = 60

class TestResults:
    def __init__(self):
        self.tests = []
        self.start_time = datetime.now()
    
    def add_result(self, test_name, status, response_time=None, error=None, details=None):
        self.tests.append({
            "test": test_name,
            "status": status,
            "response_time": response_time,
            "error": error,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def summary(self):
        total = len(self.tests)
        passed = sum(1 for t in self.tests if t["status"] == "PASS")
        failed = sum(1 for t in self.tests if t["status"] == "FAIL")
        
        response_times = [t["response_time"] for t in self.tests if t["response_time"]]
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": f"{(passed/total*100):.1f}%" if total > 0 else "0%",
            "avg_response_time": f"{statistics.mean(response_times):.2f}s" if response_times else "N/A",
            "min_response_time": f"{min(response_times):.2f}s" if response_times else "N/A",
            "max_response_time": f"{max(response_times):.2f}s" if response_times else "N/A",
            "duration": str(datetime.now() - self.start_time)
        }


# ================================================================================
# OPERATIONAL ACCEPTANCE TESTS (OAT)
# ================================================================================

async def test_chatbot_health():
    """Test 1: Chatbot endpoint health"""
    results = TestResults()
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            start = time.time()
            response = await client.get(f"{CHATBOT_URL}/", follow_redirects=True)
            elapsed = time.time() - start
            
            if response.status_code == 200 and "Nyay Mitra" in response.text:
                results.add_result("Chatbot: Homepage loads", "PASS", elapsed)
            else:
                results.add_result("Chatbot: Homepage loads", "FAIL", elapsed, 
                                 f"Status {response.status_code}")
    except Exception as e:
        results.add_result("Chatbot: Homepage loads", "FAIL", error=str(e))
    
    return results


async def test_chatbot_api():
    """Test 2: Chatbot API response quality"""
    results = TestResults()
    
    test_query = {
        "question": "What does Bhagavad Gita teach about duty and dharma?",
        "expected_sections": ["Understanding Your Situation", "Ancient Wisdom", "Clear Dharmic Directive"]
    }
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            start = time.time()
            response = await client.post(
                f"{CHATBOT_URL}/chat",
                json={"message": test_query["question"]},
                headers={"Content-Type": "application/json"}
            )
            elapsed = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                if "reply" in data and len(data["reply"]) > 100:
                    results.add_result("Chatbot: API response quality", "PASS", elapsed, 
                                     details=f"Response length: {len(data['reply'])} chars")
                else:
                    results.add_result("Chatbot: API response quality", "FAIL", elapsed, 
                                     "Response too short or malformed")
            else:
                results.add_result("Chatbot: API response quality", "FAIL", elapsed, 
                                 f"Status {response.status_code}")
    except Exception as e:
        results.add_result("Chatbot: API response quality", "FAIL", error=str(e))
    
    return results


async def test_verdict_health():
    """Test 3: Dharma Verdict endpoint health"""
    results = TestResults()
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            start = time.time()
            response = await client.get(f"{VERDICT_URL}/", follow_redirects=True)
            elapsed = time.time() - start
            
            if response.status_code == 200 and "Nyay Mitra" in response.text:
                results.add_result("Verdict: Homepage loads", "PASS", elapsed)
            else:
                results.add_result("Verdict: Homepage loads", "FAIL", elapsed, 
                                 f"Status {response.status_code}")
    except Exception as e:
        results.add_result("Verdict: Homepage loads", "FAIL", error=str(e))
    
    return results


async def test_verdict_api():
    """Test 4: Dharma Verdict API response"""
    results = TestResults()
    
    case_data = {
        "plaintiff": "John claims his brother stole his inheritance shares.",
        "defendant": "The brother denies this and claims joint ownership.",
        "facts": "The father passed 6 months ago. Inheritance divided. Brother claims shares."
    }
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            start = time.time()
            response = await client.post(
                f"{VERDICT_URL}/analyze",
                json=case_data,
                headers={"Content-Type": "application/json"}
            )
            elapsed = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                if "verdict" in data and len(data["verdict"]) > 500:
                    results.add_result("Verdict: API verdict generation", "PASS", elapsed,
                                     details=f"Verdict length: {len(data['verdict'])} chars")
                else:
                    results.add_result("Verdict: API verdict generation", "FAIL", elapsed,
                                     "Verdict too short or missing")
            else:
                results.add_result("Verdict: API verdict generation", "FAIL", elapsed,
                                 f"Status {response.status_code}")
    except Exception as e:
        results.add_result("Verdict: API verdict generation", "FAIL", error=str(e))
    
    return results


async def test_error_handling():
    """Test 5: Error handling"""
    results = TestResults()
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Test with empty payload
            start = time.time()
            response = await client.post(
                f"{VERDICT_URL}/analyze",
                json={"plaintiff": "", "defendant": "", "facts": ""},
                headers={"Content-Type": "application/json"}
            )
            elapsed = time.time() - start
            
            if response.status_code in [400, 422]:
                results.add_result("Error: Validation catches empty fields", "PASS", elapsed)
            else:
                results.add_result("Error: Validation catches empty fields", "FAIL", elapsed,
                                 f"Expected 400/422, got {response.status_code}")
    except Exception as e:
        results.add_result("Error: Validation catches empty fields", "FAIL", error=str(e))
    
    return results


# ================================================================================
# STRESS TESTS
# ================================================================================

async def stress_test_concurrent_requests():
    """Stress Test 1: Concurrent requests"""
    results = TestResults()
    
    # Test with 5 concurrent chatbot requests
    async def make_request(client, request_num):
        try:
            start = time.time()
            response = await client.post(
                f"{CHATBOT_URL}/chat",
                json={"message": f"Request {request_num}: Tell me about dharma"},
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT
            )
            elapsed = time.time() - start
            return ("PASS" if response.status_code == 200 else "FAIL", elapsed)
        except Exception as e:
            return ("FAIL", None)
    
    try:
        async with httpx.AsyncClient() as client:
            tasks = [make_request(client, i) for i in range(5)]
            responses = await asyncio.gather(*tasks)
            
            passed = sum(1 for r in responses if r[0] == "PASS")
            times = [r[1] for r in responses if r[1]]
            
            if passed >= 4:  # Allow 1 failure
                results.add_result("Stress: 5 concurrent chatbot requests", "PASS",
                                 statistics.mean(times) if times else None,
                                 details=f"{passed}/5 succeeded, avg time: {statistics.mean(times):.2f}s")
            else:
                results.add_result("Stress: 5 concurrent chatbot requests", "FAIL",
                                 details=f"Only {passed}/5 requests succeeded")
    except Exception as e:
        results.add_result("Stress: 5 concurrent chatbot requests", "FAIL", error=str(e))
    
    return results


async def stress_test_payload_size():
    """Stress Test 2: Large payload handling"""
    results = TestResults()
    
    # Test with large case details
    large_case = {
        "plaintiff": "A" * 2000,  # 2KB of text
        "defendant": "B" * 2000,
        "facts": "C" * 3000
    }
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            start = time.time()
            response = await client.post(
                f"{VERDICT_URL}/analyze",
                json=large_case,
                headers={"Content-Type": "application/json"}
            )
            elapsed = time.time() - start
            
            if response.status_code in [200, 400, 422]:  # Accept 400/422 if validation fails
                results.add_result("Stress: Large payload (7KB)", "PASS", elapsed)
            else:
                results.add_result("Stress: Large payload (7KB)", "FAIL", elapsed,
                                 f"Status {response.status_code}")
    except Exception as e:
        results.add_result("Stress: Large payload (7KB)", "FAIL", error=str(e))
    
    return results


async def stress_test_response_time():
    """Stress Test 3: Response time validation"""
    results = TestResults()
    
    query = "What is the meaning of Nishkama Karma in the Bhagavad Gita?"
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            start = time.time()
            response = await client.post(
                f"{CHATBOT_URL}/chat",
                json={"message": query},
                headers={"Content-Type": "application/json"}
            )
            elapsed = time.time() - start
            
            # SLA: Response within 30 seconds
            if elapsed < 30 and response.status_code == 200:
                results.add_result("SLA: Response time < 30s", "PASS", elapsed)
            elif elapsed >= 30:
                results.add_result("SLA: Response time < 30s", "FAIL", elapsed,
                                 f"Exceeded SLA ({elapsed:.2f}s)")
            else:
                results.add_result("SLA: Response time < 30s", "FAIL", elapsed,
                                 f"Status {response.status_code}")
    except asyncio.TimeoutError:
        results.add_result("SLA: Response time < 30s", "FAIL", error="Request timeout")
    except Exception as e:
        results.add_result("SLA: Response time < 30s", "FAIL", error=str(e))
    
    return results


async def stress_test_sequential_requests():
    """Stress Test 4: Sequential rapid requests"""
    results = TestResults()
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            times = []
            failures = 0
            
            for i in range(3):
                try:
                    start = time.time()
                    response = await client.post(
                        f"{VERDICT_URL}/analyze",
                        json={
                            "plaintiff": f"Plaintiff statement {i}",
                            "defendant": f"Defendant statement {i}",
                            "facts": f"Case facts {i}"
                        },
                        headers={"Content-Type": "application/json"}
                    )
                    elapsed = time.time() - start
                    
                    if response.status_code != 200:
                        failures += 1
                    times.append(elapsed)
                except Exception as e:
                    failures += 1
            
            if failures == 0:
                avg_time = statistics.mean(times)
                results.add_result("Stress: 3 sequential verdict requests", "PASS",
                                 avg_time, details=f"All succeeded, avg: {avg_time:.2f}s")
            else:
                results.add_result("Stress: 3 sequential verdict requests", "FAIL",
                                 details=f"{failures}/3 failed")
    except Exception as e:
        results.add_result("Stress: 3 sequential verdict requests", "FAIL", error=str(e))
    
    return results


# ================================================================================
# MAIN TEST RUNNER
# ================================================================================

async def run_all_tests():
    """Run all OAT and stress tests"""
    print("=" * 80)
    print("NYAY MITRA — OPERATIONAL ACCEPTANCE TESTING & STRESS TESTING SUITE")
    print("=" * 80)
    print(f"Start Time: {datetime.now().isoformat()}\n")
    
    all_results = TestResults()
    
    # OAT Tests
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║ OPERATIONAL ACCEPTANCE TESTS (OAT)                                         ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    print("▶ OAT-1: Chatbot endpoint health...")
    test1 = await test_chatbot_health()
    for t in test1.tests:
        print(f"  [{t['status']}] {t['test']} ({t['response_time']:.2f}s)")
        all_results.tests.extend(test1.tests)
    print()
    
    print("▶ OAT-2: Chatbot API response quality...")
    test2 = await test_chatbot_api()
    for t in test2.tests:
        print(f"  [{t['status']}] {t['test']} ({t['response_time']:.2f}s)")
        all_results.tests.extend(test2.tests)
    print()
    
    print("▶ OAT-3: Dharma Verdict endpoint health...")
    test3 = await test_verdict_health()
    for t in test3.tests:
        print(f"  [{t['status']}] {t['test']} ({t['response_time']:.2f}s)")
        all_results.tests.extend(test3.tests)
    print()
    
    print("▶ OAT-4: Dharma Verdict API response...")
    test4 = await test_verdict_api()
    for t in test4.tests:
        print(f"  [{t['status']}] {t['test']} ({t['response_time']:.2f}s)")
        all_results.tests.extend(test4.tests)
    print()
    
    print("▶ OAT-5: Error handling validation...")
    test5 = await test_error_handling()
    for t in test5.tests:
        print(f"  [{t['status']}] {t['test']} ({t['response_time']:.2f}s)")
        all_results.tests.extend(test5.tests)
    print()
    
    # Stress Tests
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║ STRESS TESTS                                                               ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    print("▶ STRESS-1: Concurrent requests (5 parallel)...")
    test6 = await stress_test_concurrent_requests()
    for t in test6.tests:
        print(f"  [{t['status']}] {t['test']}")
        if t['details']:
            print(f"      Details: {t['details']}")
        all_results.tests.extend(test6.tests)
    print()
    
    print("▶ STRESS-2: Large payload handling (7KB)...")
    test7 = await stress_test_payload_size()
    for t in test7.tests:
        print(f"  [{t['status']}] {t['test']} ({t['response_time']:.2f}s)")
        all_results.tests.extend(test7.tests)
    print()
    
    print("▶ STRESS-3: Response time SLA check (<30s)...")
    test8 = await stress_test_response_time()
    for t in test8.tests:
        print(f"  [{t['status']}] {t['test']} ({t['response_time']:.2f}s)")
        all_results.tests.extend(test8.tests)
    print()
    
    print("▶ STRESS-4: Sequential rapid requests (3 verdicts)...")
    test9 = await stress_test_sequential_requests()
    for t in test9.tests:
        print(f"  [{t['status']}] {t['test']}")
        if t['details']:
            print(f"      Details: {t['details']}")
        all_results.tests.extend(test9.tests)
    print()
    
    # Summary
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║ TEST SUMMARY                                                               ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    summary = all_results.summary()
    print(f"Total Tests:        {summary['total_tests']}")
    print(f"Passed:             {summary['passed']}")
    print(f"Failed:             {summary['failed']}")
    print(f"Pass Rate:          {summary['pass_rate']}")
    print(f"Avg Response Time:  {summary['avg_response_time']}")
    print(f"Min Response Time:  {summary['min_response_time']}")
    print(f"Max Response Time:  {summary['max_response_time']}")
    print(f"Total Duration:     {summary['duration']}\n")
    
    # Save report to JSON
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "tests": all_results.tests
    }
    
    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Report saved to: test_report.json\n")
    
    return summary['failed'] == 0


if __name__ == "__main__":
    try:
        success = asyncio.run(run_all_tests())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        exit(1)
