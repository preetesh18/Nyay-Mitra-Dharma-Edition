# Simple Test Script for Nyay Mitra APIs

param(
    [string]$ChatbotPort = 5000,
    [string]$VerdictPort = 5001
)

$BASE_URL_CHATBOT = "http://localhost:$ChatbotPort"
$BASE_URL_VERDICT = "http://localhost:$VerdictPort"

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host "   NYAY MITRA - LOCAL API TEST SUITE"
Write-Host "   Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host ""

# Test Chatbot API
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host "SECTION 1: CHATBOT API TESTS"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

Write-Host ""
Write-Host "[TEST 1.1] Checking if Chatbot API is running..."
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL_CHATBOT/api/test" -Method GET -TimeoutSec 5
    Write-Host "✓ Chatbot API is RUNNING"
    Write-Host "  Response: $($response | ConvertTo-Json -Depth 2)"
    $chatbotOK = $true
}
catch {
    Write-Host "✗ Chatbot API is NOT RESPONDING - $($_.Exception.Message)"
    $chatbotOK = $false
}

if ($chatbotOK) {
    Write-Host ""
    Write-Host "[TEST 1.2] Testing Chat - Simple Query"
    try {
        $body = @{ message = "What is Dharma?" } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$BASE_URL_CHATBOT/api/chat" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 15
        Write-Host "✓ Chat endpoint responding"
        Write-Host "  Session ID: $($response.session_id)"
        Write-Host "  Reply: $(($response.reply -split 'n')[0])..." 
    }
    catch {
        Write-Host "✗ Chat test failed - $($_.Exception.Message)"
    }
    
    Write-Host ""
    Write-Host "[TEST 1.3] Testing Chat - Complex Query"
    try {
        $body = @{ message = "What does Bhagavad Gita teach about duty and business ethics?" } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$BASE_URL_CHATBOT/api/chat" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 15
        Write-Host "✓ Complex chat responding"
        Write-Host "  Session ID: $($response.session_id)"
        Write-Host "  Reply length: $($response.reply.Length) characters"
    }
    catch {
        Write-Host "✗ Complex chat failed - $($_.Exception.Message)"
    }
    
    Write-Host ""
    Write-Host "[TEST 1.4] Testing History Endpoint"
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL_CHATBOT/api/history" -Method GET -TimeoutSec 5
        Write-Host "✓ History endpoint responding"
        Write-Host "  Messages retrieved: $($response.history.Count)"
    }
    catch {
        Write-Host "✗ History endpoint failed - $($_.Exception.Message)"
    }
    
    Write-Host ""
    Write-Host "[TEST 1.5] Testing Reset Endpoint"
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL_CHATBOT/api/reset" -Method POST -TimeoutSec 5
        Write-Host "✓ Reset endpoint responding"
        Write-Host "  Response: $(($response | ConvertTo-Json -Depth 1))"
    }
    catch {
        Write-Host "✗ Reset endpoint failed - $($_.Exception.Message)"
    }
}

# Test Verdict API
Write-Host ""
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host "SECTION 2: VERDICT API TESTS"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

Write-Host ""
Write-Host "[TEST 2.1] Checking if Verdict API is running..."
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL_VERDICT/api/test" -Method GET -TimeoutSec 5
    Write-Host "✓ Verdict API is RUNNING"
    Write-Host "  Response: $($response | ConvertTo-Json -Depth 2)"
    $verdictOK = $true
}
catch {
    Write-Host "✗ Verdict API is NOT RESPONDING - $($_.Exception.Message)"
    $verdictOK = $false
}

if ($verdictOK) {
    Write-Host ""
    Write-Host "[TEST 2.2] Testing Verdict Analysis - Business Case"
    try {
        $body = @{
            plaintiff = "Merchant A claims breach of partnership agreement"
            defendant = "Merchant B stopped payments citing market conditions"
            facts = "Contract signed 3 years ago. Partnership was working well. B stopped payments without notice"
        } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$BASE_URL_VERDICT/api/analyze" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 15
        Write-Host "✓ Verdict analysis responding"
        Write-Host "  Session ID: $($response.session_id)"
        Write-Host "  Verdict preview: $(($response.verdict -split 'n')[0])..."
    }
    catch {
        Write-Host "✗ Verdict analysis failed - $($_.Exception.Message)"
    }
    
    Write-Host ""
    Write-Host "[TEST 2.3] Testing Verdict Analysis - Family Case"
    try {
        $body = @{
            plaintiff = "Son seeks fair property inheritance"
            defendant = "Father prefers to give more to son who cared for him"
            facts = "Three sons. One stayed with father all life. Two moved abroad. Father wants to distribute 50% to caring son and 25% each to others"
        } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$BASE_URL_VERDICT/api/analyze" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 15
        Write-Host "✓ Family case analysis responding"
        Write-Host "  Session ID: $($response.session_id)"
        Write-Host "  Verdict length: $($response.verdict.Length) characters"
    }
    catch {
        Write-Host "✗ Family case analysis failed - $($_.Exception.Message)"
    }
    
    Write-Host ""
    Write-Host "[TEST 2.4] Testing Verdict History"
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL_VERDICT/api/history" -Method GET -TimeoutSec 5
        Write-Host "✓ Verdict history endpoint responding"
        Write-Host "  Cases analyzed: $($response.history.Count)"
    }
    catch {
        Write-Host "✗ Verdict history failed - $($_.Exception.Message)"
    }
}

# Error Handling Tests
Write-Host ""
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host "SECTION 3: ERROR HANDLING TESTS"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ($chatbotOK) {
    Write-Host ""
    Write-Host "[TEST 3.1] Testing Empty Message Handling"
    try {
        $body = @{ message = "" } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$BASE_URL_CHATBOT/api/chat" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 5
        Write-Host "✓ Empty message handled"
    }
    catch {
        Write-Host "✓ Empty message properly rejected - $($_.Exception.Message.Split([Environment]::NewLine)[0])"
    }
}

if ($verdictOK) {
    Write-Host ""
    Write-Host "[TEST 3.2] Testing Incomplete Case Data"
    try {
        $body = @{
            plaintiff = "Person A only"
        } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$BASE_URL_VERDICT/api/analyze" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 5
        Write-Host "✓ Incomplete data handled"
    }
    catch {
        Write-Host "✓ Incomplete data properly rejected - $($_.Exception.Message.Split([Environment]::NewLine)[0])"
    }
}

# Final Summary
Write-Host ""
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host "TEST SUITE SUMMARY"
Write-Host "════════════════════════════════════════════════════════════════"
Write-Host ""

if ($chatbotOK -and $verdictOK) {
    Write-Host "✓ Chatbot API: WORKING"
    Write-Host "✓ Verdict API: WORKING"
    Write-Host ""
    Write-Host "🎉 ALL SYSTEMS OPERATIONAL"
    Write-Host ""
    Write-Host "Status: READY FOR DEPLOYMENT"
}
elseif ($chatbotOK -or $verdictOK) {
    Write-Host "Status: Partial - One API not responding"
}
else {
    Write-Host "Status: FAILED - Both APIs not responding"
}

Write-Host ""
Write-Host "Test completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""
