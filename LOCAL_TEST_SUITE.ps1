# Comprehensive Local Testing Suite for Nyay Mitra APIs
# ════════════════════════════════════════════════════════════════════

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# Configuration
$GEMINI_API_KEY = "AIzaSyCxTDULW9ovk5-LjNNX6HHMmMbNBYMb95k"
$CHATBOT_PORT = 5000
$VERDICT_PORT = 5001
$BASE_URL_CHATBOT = "http://localhost:$CHATBOT_PORT"
$BASE_URL_VERDICT = "http://localhost:$VERDICT_PORT"
$TIMEOUT = 30

# Color codes for output
$GREEN = "`e[32m"
$RED = "`e[31m"
$YELLOW = "`e[33m"
$BLUE = "`e[34m"
$RESET = "`e[0m"

Write-Host "$BLUE╔═══════════════════════════════════════════════════════════════╗$RESET"
Write-Host "$BLUE║   Nyay Mitra - Comprehensive Local API Test Suite             ║$RESET"
Write-Host "$BLUE║   Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')                  ║$RESET"
Write-Host "$BLUE╚═══════════════════════════════════════════════════════════════╝$RESET"
Write-Host ""

# ─────────────────────────────────────────────────────────────────────────────
# TEST FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [object]$Body = $null,
        [string]$Description = ""
    )
    
    Write-Host "$YELLOW→ Testing: $Name$RESET"
    if ($Description) {
        Write-Host "  Description: $Description"
    }
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
            TimeoutSec = $TIMEOUT
            Headers = @{ "Content-Type" = "application/json" }
        }
        
        if ($Body) {
            $params["Body"] = ($Body | ConvertTo-Json -Depth 10)
        }
        
        $response = Invoke-RestMethod @params
        Write-Host "  $GREEN✓ Response Status: OK$RESET"
        Write-Host "  Response: $(ConvertTo-Json $response -Depth 3)"
        return @{
            Success = $true
            Response = $response
            StatusCode = 200
        }
    }
    catch {
        Write-Host "  $RED✗ Error: $($_.Exception.Message)$RESET"
        if ($_.Exception.Response) {
            Write-Host "  Status Code: $($_.Exception.Response.StatusCode)"
        }
        return @{
            Success = $false
            Error = $_.Exception.Message
            Response = $null
        }
    }
}

function Check-ServerRunning {
    param([string]$Url, [string]$ServerName)
    
    Write-Host "$BLUE─────────────────────────────────────────$RESET"
    Write-Host "Checking if $ServerName is running..."
    Write-Host "Endpoint: $Url"
    
    try {
        $response = Invoke-WebRequest -Uri "$Url/api/test" -Method GET -TimeoutSec 5 -ErrorAction Stop
        Write-Host "$GREEN✓ $ServerName is running and responding$RESET"
        return $true
    }
    catch {
        Write-Host "$RED✗ $ServerName is NOT responding$RESET"
        Write-Host "  Error: $($_.Exception.Message)"
        return $false
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: CHATBOT API TESTS
# ─────────────────────────────────────────────────────────────────────────────

Write-Host "$BLUE" + "=" * 70 + "$RESET"
Write-Host "$BLUE SECTION 1: CHATBOT API TESTS" + " " * 35 + "$RESET"
Write-Host "$BLUE" + "=" * 70 + "$RESET"

$chatbotRunning = Check-ServerRunning -Url $BASE_URL_CHATBOT -ServerName "Chatbot API"

if ($chatbotRunning) {
    Write-Host ""
    Write-Host "$YELLOW► Test Case 1.1: Health Check$RESET"
    Test-Endpoint -Name "GET /api/test" -Url "$BASE_URL_CHATBOT/api/test" -Description "Basic health check"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 1.2: Chat Message - Simple Query$RESET"
    $test_message = @{
        message = "What is Dharma?"
    }
    Test-Endpoint -Name "POST /api/chat (Simple)" -Url "$BASE_URL_CHATBOT/api/chat" -Method "POST" -Body $test_message -Description "Test basic chat functionality"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 1.3: Chat Message - Complex Query$RESET"
    $complex_message = @{
        message = "What does the Bhagavad Gita say about fulfilling one's duties in challenging times?"
    }
    Test-Endpoint -Name "POST /api/chat (Complex)" -Url "$BASE_URL_CHATBOT/api/chat" -Method "POST" -Body $complex_message -Description "Test complex chat with philosophical question"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 1.4: History Endpoint$RESET"
    Test-Endpoint -Name "GET /api/history" -Url "$BASE_URL_CHATBOT/api/history" -Description "Retrieve conversation history"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 1.5: Reset Endpoint$RESET"
    Test-Endpoint -Name "POST /api/reset" -Url "$BASE_URL_CHATBOT/api/reset" -Method "POST" -Description "Reset conversation"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 1.6: Logs Endpoint$RESET"
    Test-Endpoint -Name "GET /api/logs" -Url "$BASE_URL_CHATBOT/api/logs" -Description "Retrieve session logs"
}
else {
    Write-Host "$RED⚠ Skipping chatbot tests - server not running$RESET"
}

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: VERDICT API TESTS
# ─────────────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "$BLUE" + "=" * 70 + "$RESET"
Write-Host "$BLUE SECTION 2: VERDICT API TESTS" + " " * 36 + "$RESET"
Write-Host "$BLUE" + "=" * 70 + "$RESET"

$verdictRunning = Check-ServerRunning -Url $BASE_URL_VERDICT -ServerName "Verdict API"

if ($verdictRunning) {
    Write-Host ""
    Write-Host "$YELLOW► Test Case 2.1: Health Check$RESET"
    Test-Endpoint -Name "GET /api/test" -Url "$BASE_URL_VERDICT/api/test" -Description "Basic health check"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 2.2: Simple Verdict Analysis$RESET"
    $simple_case = @{
        plaintiff = "Person A claims breach of contract"
        defendant = "Person B denies the agreement"
        facts = "Email evidence shows communication"
    }
    Test-Endpoint -Name "POST /api/analyze (Simple)" -Url "$BASE_URL_VERDICT/api/analyze" -Method "POST" -Body $simple_case -Description "Test basic verdict analysis"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 2.3: Complex Legal Case$RESET"
    $complex_case = @{
        plaintiff = "Merchant A claims breach of dharmic duty in business partnership"
        defendant = "Merchant B claims force majeure and unavoidable circumstances"
        facts = "Contract signed 5 years ago. Payment made for 3 years. Stopped payments citing market conditions. Merchant A invested in infrastructure based on partnership"
    }
    Test-Endpoint -Name "POST /api/analyze (Complex)" -Url "$BASE_URL_VERDICT/api/analyze" -Method "POST" -Body $complex_case -Description "Test complex legal case analysis"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 2.4: Family Matter$RESET"
    $family_case = @{
        plaintiff = "Son seeks fair inheritance distribution"
        defendant = "Father argues for unequal distribution based on care provided"
        facts = "Three sons. One stayed with father in old age, two moved abroad. Father wishes to give more to the caring son"
    }
    Test-Endpoint -Name "POST /api/analyze (Family)" -Url "$BASE_URL_VERDICT/api/analyze" -Method "POST" -Body $family_case -Description "Test family law case"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 2.5: History Endpoint$RESET"
    Test-Endpoint -Name "GET /api/history" -Url "$BASE_URL_VERDICT/api/history" -Description "Retrieve analysis history"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 2.6: Logs Endpoint$RESET"
    Test-Endpoint -Name "GET /api/logs" -Url "$BASE_URL_VERDICT/api/logs" -Description "Retrieve session logs"
}
else {
    Write-Host "$RED⚠ Skipping verdict tests - server not running$RESET"
}

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: ERROR HANDLING TESTS
# ─────────────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "$BLUE" + "=" * 70 + "$RESET"
Write-Host "$BLUE SECTION 3: ERROR HANDLING TESTS" + " " * 33 + "$RESET"
Write-Host "$BLUE" + "=" * 70 + "$RESET"

if ($chatbotRunning) {
    Write-Host ""
    Write-Host "$YELLOW► Test Case 3.1: Empty Message$RESET"
    $empty_message = @{ message = "" }
    Test-Endpoint -Name "POST /api/chat (Empty)" -Url "$BASE_URL_CHATBOT/api/chat" -Method "POST" -Body $empty_message -Description "Test handling of empty message"
    
    Write-Host ""
    Write-Host "$YELLOW► Test Case 3.2: Missing Required Field$RESET"
    $missing_field = @{ }
    Test-Endpoint -Name "POST /api/chat (Missing Field)" -Url "$BASE_URL_CHATBOT/api/chat" -Method "POST" -Body $missing_field -Description "Test error handling for missing field"
}

if ($verdictRunning) {
    Write-Host ""
    Write-Host "$YELLOW► Test Case 3.3: Incomplete Case Data$RESET"
    $incomplete_case = @{
        plaintiff = "Person A"
    }
    Test-Endpoint -Name "POST /api/analyze (Incomplete)" -Url "$BASE_URL_VERDICT/api/analyze" -Method "POST" -Body $incomplete_case -Description "Test error handling for incomplete case data"
}

# ─────────────────────────────────────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "$BLUE" + "=" * 70 + "$RESET"
Write-Host "$BLUE TEST SUITE COMPLETE" + " " * 44 + "$RESET"
Write-Host "$BLUE" + "=" * 70 + "$RESET"
Write-Host ""

if ($chatbotRunning -and $verdictRunning) {
    Write-Host "$GREEN✓ Both APIs are running and responding$RESET"
    Write-Host "$GREEN✓ All functional tests completed$RESET"
    Write-Host ""
    Write-Host "$GREEN🎉 READY FOR DEPLOYMENT!$RESET"
}
elseif ($chatbotRunning -or $verdictRunning) {
    Write-Host "$YELLOW⚠ One API is running, but not both$RESET"
}
else {
    Write-Host "$RED✗ Neither API is running$RESET"
    Write-Host ""
    Write-Host "To start the APIs, run:"
    Write-Host "  Terminal 1: cd features/chatbot && python app.py"
    Write-Host "  Terminal 2: cd features/dharma_verdict && python app.py"
}

Write-Host ""
Write-Host "Test completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
