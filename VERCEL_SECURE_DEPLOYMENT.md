# 🔒 VERCEL SECURE DEPLOYMENT GUIDE
## Store Gemini API Key Safely in Vercel Environment Variables

**Problem:** API key stored locally = risk of git commits and exposure
**Solution:** Vercel Environment Variables = secure, zero-exposure deployment

---

## Why This Works

```
Local Development              Production (Vercel)
├─ .env (local)               ├─ Environment Variables (secret)
├─ GEMINI_API_KEY=xxx         ├─ NEVER stored in code
└─ load_dotenv() reads it      └─ Injected at runtime only
```

**Your Flask apps already support this!** They use:
```python
api_key = os.environ.get("GEMINI_API_KEY")
```

Works with:
- ✅ Local `.env` file (development)
- ✅ Vercel Environment Variables (production)
- ✅ GitHub CI/CD secrets
- ✅ Docker secrets
- ✅ Any environment that sets env vars

---

## Step 1: Prepare for Vercel Deployment

### 1.1 Check Your Files Structure

```
features/
├── chatbot/
│   ├── app.py              (✅ Ready)
│   ├── requirements.txt    (✅ Ready)
│   ├── vercel.json         (Create/Update)
│   ├── api/
│   │   └── index.py        (Create)
│   └── .env                (⚠️ DO NOT COMMIT)
│
└── dharma_verdict/
    ├── app.py              (✅ Ready)
    ├── requirements.txt    (✅ Ready)
    ├── vercel.json         (Create/Update)
    ├── api/
    │   └── index.py        (Create)
    └── .env                (⚠️ DO NOT COMMIT)
```

### 1.2 Create Vercel Configuration Files

#### For Chatbot: `features/chatbot/vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb",
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "GEMINI_API_KEY": "@gemini-api-key",
    "FLASK_ENV": "production",
    "FLASK_SECRET_KEY": "@flask-secret-key"
  }
}
```

#### For Dharma Verdict: `features/dharma_verdict/vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb",
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "GEMINI_API_KEY": "@gemini-api-key",
    "FLASK_ENV": "production",
    "FLASK_SECRET_KEY": "@flask-secret-key"
  }
}
```

### 1.3 Create API Entry Point for Vercel

**For Chatbot: `features/chatbot/api/index.py`**

```python
import sys
from pathlib import Path

# Add parent directory to path so we can import app
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app import app

# Vercel expects a WSGI app named 'app'
# Our Flask app is already named 'app' in app.py
```

**For Dharma Verdict: `features/dharma_verdict/api/index.py`**

```python
import sys
from pathlib import Path

# Add parent directory to path so we can import app
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app import app

# Vercel expects a WSGI app named 'app'
# Our Flask app is already named 'app' in app.py
```

### 1.4 Update requirements.txt (Both Apps)

Ensure both have:

```txt
Flask==3.1.3
httpx==0.28.1
python-dotenv==1.2.2
flask-cors==4.0.0
gunicorn==23.0.0
```

### 1.5 Create .gitignore in Root

```
# Environment Variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# Vercel
.vercel/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## Step 2: Set Up Vercel Project

### 2.1 Create Vercel Account

1. Go to https://vercel.com/signup
2. Sign up with GitHub (recommended)
3. Authorize access to your repositories

### 2.2 Create Two Vercel Projects

**Project 1: Chatbot Backend**

1. Click "Add New" → "Project"
2. Select your GitHub repository
3. Name: `nyay-mitra-chatbot`
4. Root Directory: `features/chatbot`
5. Framework: `Other` (Flask)
6. Build Command: `pip install -r requirements.txt`
7. Install Command: `pip install -r requirements.txt`
8. Output Directory: `.`
9. Click "Deploy"

**Project 2: Dharma Verdict Backend**

1. Click "Add New" → "Project"
2. Select repository
3. Name: `nyay-mitra-verdict`
4. Root Directory: `features/dharma_verdict`
5. Framework: `Other` (Flask)
6. Build Command: `pip install -r requirements.txt`
7. Install Command: `pip install -r requirements.txt`
8. Output Directory: `.`
9. Click "Deploy"

### 2.3 Get Your Vercel URLs

After deployment, you'll get:
- Chatbot: `https://nyay-mitra-chatbot.vercel.app`
- Verdict: `https://nyay-mitra-verdict.vercel.app`

---

## Step 3: Add Environment Variables to Vercel

### 3.1 Add API Key to Chatbot Project

1. Go to https://vercel.com/dashboard
2. Select `nyay-mitra-chatbot` project
3. Click "Settings" → "Environment Variables"
4. Click "Add"
5. **Name:** `GEMINI_API_KEY`
6. **Value:** Your new Gemini API key from https://aistudio.google.com/app/apikey
7. **Select:** Production, Preview, Development
8. Click "Save"

### 3.2 Add Secret Variables (Optional but Recommended)

1. Add `FLASK_SECRET_KEY` with a random string
2. Add `LOGS_DIR` = `/tmp/vercel-logs` (for serverless)
3. Click "Save"

### 3.3 Repeat for Verdict Project

Same steps, add to `nyay-mitra-verdict` project.

### 3.4 Redeploy to Apply Variables

1. Go to "Deployments" tab
2. Click "Redeploy" on latest deployment
3. Wait for build to complete
4. Test endpoints

---

## Step 4: Test Your Vercel Deployment

### 4.1 Test Chatbot Backend

```bash
# Test health
curl https://nyay-mitra-chatbot.vercel.app/api/health

# Expected response:
# {"status": "ok"}

# Test Gemini connection
curl -X POST https://nyay-mitra-chatbot.vercel.app/api/test-gemini

# Expected response:
# {"status": "ok", "model": "gemini-2.5-flash"}

# Send actual message
curl -X POST https://nyay-mitra-chatbot.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is dharma?"}'

# Expected response:
# {"session_id": "...", "reply": "Dharma is...", "model": "gemini-2.5-flash"}
```

### 4.2 Test Verdict Backend

```bash
# Test health
curl https://nyay-mitra-verdict.vercel.app/api/health

# Test Gemini connection
curl -X POST https://nyay-mitra-verdict.vercel.app/api/test-gemini

# Submit case
curl -X POST https://nyay-mitra-verdict.vercel.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "plaintiff": "Person A claims breach",
    "defendant": "Person B denies",
    "facts": "Email evidence available"
  }'

# Expected response:
# {"verdict": "## Analysis\n...", "model": "gemini-2.5-flash"}
```

### 4.3 Check Vercel Logs

1. Go to Vercel Dashboard
2. Select project
3. Click "Deployments" → "Functions" → "Logs"
4. See real-time logs from your running app

---

## Step 5: Connect Frontend to Vercel APIs

### Update HTML Files

#### For chatbot-standalone.html

Change:
```javascript
const API_URL = 'http://127.0.0.1:5000';
```

To:
```javascript
const API_URL = 'https://nyay-mitra-chatbot.vercel.app';
```

#### For dharma-verdict-standalone.html

Change:
```javascript
const VERDICT_API = 'http://127.0.0.1:5001';
```

To:
```javascript
const VERDICT_API = 'https://nyay-mitra-verdict.vercel.app';
```

### Update React Frontend (if using)

Create `.env.production`:
```
VITE_CHATBOT_API=https://nyay-mitra-chatbot.vercel.app
VITE_VERDICT_API=https://nyay-mitra-verdict.vercel.app
```

---

## Step 6: Deploy Frontend to Vercel

### Option A: Deploy HTML to Vercel

1. Create a new project
2. Root Directory: `.` (root of repo)
3. Upload HTML files
4. Deploy

### Option B: Deploy React to Vercel

1. Create new project
2. Root Directory: `frontend`
3. Framework: React
4. Build Command: `npm run build`
5. Install Command: `npm install`
6. Output: `dist`
7. Deploy

---

## Security Best Practices

### ✅ DO

- ✅ Store API key only in Vercel Environment Variables
- ✅ Add `.env` to `.gitignore`
- ✅ Use different keys for dev/staging/production
- ✅ Rotate keys every 3-6 months
- ✅ Use Vercel's built-in secrets
- ✅ Enable branch protection on main

### ❌ DON'T

- ❌ Commit `.env` to git
- ❌ Hardcode API key in code
- ❌ Share API key via chat/email
- ❌ Use same key everywhere
- ❌ Leave old keys in Settings after rotation
- ❌ Print API key to logs

---

## Architecture After Setup

```
┌─────────────────────────────────────────┐
│        User's Browser                   │
│  ┌───────────────────────────────────┐  │
│  │ HTML/CSS/JS or React App          │  │
│  │ (Hosted on Vercel)                │  │
│  └─────────┬───────────────────────┬─┘  │
└────────────┼────────────────────────┼────┘
             │                        │
    ┌────────┴────────┐    ┌─────────┴──────────┐
    │                 │    │                    │
┌───▼──────────────┐ ┌──▼───────────────────┐
│ Vercel Function  │ │ Vercel Function      │
│ Chatbot Backend  │ │ Verdict Backend      │
│ GEMINI_API_KEY ←─┼─┤ GEMINI_API_KEY ←────┤
│ (from env var)   │ │ (from env var)       │
└────┬─────────────┘ └──┬────────────────────┘
     │                  │
     └────────┬─────────┘
              │
         ┌────▼──────────────┐
         │ Google Gemini API │
         │ (gemini-2.5-flash)│
         └───────────────────┘
```

**Key Point:** API Key NEVER stored in code, git, or logs - only in Vercel's secure vault.

---

## Troubleshooting

### Error: "GEMINI_API_KEY is NOT SET"

**Cause:** Environment variable not added to Vercel
**Solution:** 
1. Go to Vercel Settings
2. Add Environment Variable
3. Redeploy

### Error: 403 PERMISSION_DENIED

**Cause:** Old/leaked API key still in use
**Solution:**
1. Generate new key at https://aistudio.google.com/app/apikey
2. Update Vercel Environment Variable
3. Redeploy

### Error: 500 on Function

**Cause:** Dependencies missing or code error
**Solution:**
1. Check Vercel Logs (Deployments → Functions → Logs)
2. Verify `requirements.txt` is complete
3. Redeploy

### Functions Timing Out

**Cause:** API calls too slow
**Solution:**
1. Increase function timeout in `vercel.json`: `"maxDuration": 60`
2. Re-deploy

---

## Complete vercel.json Example (With All Options)

```json
{
  "version": 2,
  "buildCommand": "pip install -r requirements.txt",
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb",
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "GEMINI_API_KEY": "@gemini-api-key",
    "FLASK_ENV": "production",
    "FLASK_SECRET_KEY": "@flask-secret-key",
    "LOGS_DIR": "/tmp/vercel-logs"
  },
  "functions": {
    "api/index.py": {
      "maxDuration": 60,
      "memory": 1024
    }
  }
}
```

---

## Step-by-Step Deployment Checklist

- [ ] Create `.gitignore` with `.env`
- [ ] Create `vercel.json` in chatbot folder
- [ ] Create `vercel.json` in dharma_verdict folder
- [ ] Create `api/index.py` in chatbot folder
- [ ] Create `api/index.py` in dharma_verdict folder
- [ ] Commit changes (NOT `.env`) to git
- [ ] Create Vercel account
- [ ] Create two Vercel projects (chatbot, verdict)
- [ ] Add GEMINI_API_KEY to both projects
- [ ] Redeploy both projects
- [ ] Test `/api/health` endpoints
- [ ] Test `/api/test-gemini` endpoints
- [ ] Update HTML files with Vercel URLs
- [ ] Deploy frontend to Vercel
- [ ] Test full flow from browser
- [ ] Enable branch protection
- [ ] Document deployment process
- [ ] Set up monitoring

---

## After Deployment: Key Points

### Local Development Still Works
```bash
# Your machine - uses .env
export GEMINI_API_KEY="your-key-here"
cd features/chatbot
python app.py
# Runs on http://127.0.0.1:5000
```

### Production Uses Vercel Secrets
```
Vercel Dashboard → Environment Variables
↓
Build → GEMINI_API_KEY injected
↓
Runtime → API key available
↓
https://nyay-mitra-chatbot.vercel.app → Works!
```

### Your API Key is Safe
- ✅ Not in git history
- ✅ Not in code
- ✅ Not on your computer
- ✅ Only in Vercel's vault
- ✅ Only accessible by your project
- ✅ Encrypted in transit

---

## Next Steps

1. ✅ Create `vercel.json` files (see above)
2. ✅ Create `api/index.py` files (see above)
3. ✅ Commit to git (excluding `.env`)
4. ✅ Create Vercel projects
5. ✅ Add API key to Vercel
6. ✅ Redeploy
7. ✅ Test endpoints
8. ✅ Update frontend URLs
9. ✅ Deploy frontend
10. ✅ Test full flow

---

**Status:** 🟢 Production-Ready with Zero API Key Exposure

**Your Gemini API Key is now:**
- ✅ Secure in Vercel vault
- ✅ Never exposed in code
- ✅ Never committed to git
- ✅ Protected by Vercel encryption
- ✅ Rotatable instantly
- ✅ Environment-specific
- ✅ Audit-logged

**Deployment Time:** ~15 minutes
**Security Level:** ⭐⭐⭐⭐⭐ (Maximum)
