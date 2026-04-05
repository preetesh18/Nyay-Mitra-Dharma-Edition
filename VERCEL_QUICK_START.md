# 🚀 VERCEL DEPLOYMENT QUICK START

## What We've Created

```
✅ VERCEL_SECURE_DEPLOYMENT.md    - Complete deployment guide
✅ features/chatbot/vercel.json    - Vercel config (chatbot)
✅ features/chatbot/api/index.py   - Vercel entry point (chatbot)
✅ features/dharma_verdict/vercel.json    - Vercel config (verdict)
✅ features/dharma_verdict/api/index.py   - Vercel entry point (verdict)
✅ .gitignore                       - Prevents .env leaks
```

## Why This Solves API Key Leak

Your Flask apps already read API key from environment variables:
```python
api_key = os.environ.get("GEMINI_API_KEY")  # ✅ Works locally & on Vercel
```

**Local:** Uses `.env` file with `load_dotenv()`
**Vercel:** Uses Vercel's Environment Variables (no file needed)

API key is NEVER:
- ❌ Committed to git
- ❌ Exposed in code
- ❌ Visible in logs
- ❌ Stored locally after deployment

---

## 5-Minute Setup Overview

### 1. Generate New API Key (2 min)
```
https://aistudio.google.com/app/apikey
→ Click "Create API Key"
→ Copy it (keep it safe!)
```

### 2. Create Vercel Account (1 min)
```
https://vercel.com/signup
→ Sign up with GitHub
→ Authorize GitHub access
```

### 3. Deploy Chatbot Backend (1 min each)
```
1. Go to https://vercel.com/new
2. Import repository
3. Root Directory: features/chatbot
4. Click Deploy
5. Wait ~2 minutes
6. Get URL: https://nyay-mitra-chatbot.vercel.app
```

### 4. Deploy Verdict Backend (1 min)
```
1. Go to https://vercel.com/new
2. Import repository
3. Root Directory: features/dharma_verdict
4. Click Deploy
5. Wait ~2 minutes
6. Get URL: https://nyay-mitra-verdict.vercel.app
```

### 5. Add API Key to Vercel (2 min)
```
For each project:
1. Go to Settings → Environment Variables
2. Add: GEMINI_API_KEY = your-key-from-step-1
3. Add: FLASK_SECRET_KEY = random-string
4. Click "Redeploy" on Deployments
```

---

## Test Your Deployment

```bash
# Test Chatbot
curl https://nyay-mitra-chatbot.vercel.app/api/health
# → {"status": "ok"}

curl -X POST https://nyay-mitra-chatbot.vercel.app/api/test-gemini
# → {"status": "ok", "model": "gemini-2.5-flash"}

# Test Verdict
curl https://nyay-mitra-verdict.vercel.app/api/health
# → {"status": "ok"}

curl -X POST https://nyay-mitra-verdict.vercel.app/api/test-gemini
# → {"status": "ok", "model": "gemini-2.5-flash"}
```

---

## Update Your Frontend

### In HTML Files

**chatbot-standalone.html:**
Change: `const API_URL = 'http://127.0.0.1:5000'`
To: `const API_URL = 'https://nyay-mitra-chatbot.vercel.app'`

**dharma-verdict-standalone.html:**
Change: `const VERDICT_API = 'http://127.0.0.1:5001'`
To: `const VERDICT_API = 'https://nyay-mitra-verdict.vercel.app'`

### Deploy Frontend to Vercel

```
1. https://vercel.com/new
2. Import repository
3. Root Directory: . (or create frontend folder)
4. Build: (leave empty for static HTML)
5. Deploy
```

---

## Security Checklist ✅

- [ ] `.env` added to `.gitignore`
- [ ] API key NOT in any Python files
- [ ] Vercel projects created
- [ ] GEMINI_API_KEY added to both projects' Environment Variables
- [ ] Projects redeployed with env vars
- [ ] `/api/test-gemini` returns 200 OK
- [ ] Chat/verdict endpoints return real responses
- [ ] HTML files updated with Vercel URLs
- [ ] Frontend deployed to Vercel

---

## Architecture

```
Old (UNSAFE):              New (SAFE with Vercel):
.env (in git) ❌           Vercel Vault (encrypted) ✅
    ↓                              ↓
  Code                        Environment
    ↓                              ↓
 Exposed                      Injected at runtime
    ↓                              ↓
  Risk                         Secure
```

---

## Production URLs

After deployment, you'll have:

```
API Endpoints:
- Chatbot:     https://nyay-mitra-chatbot.vercel.app/api/chat
- Verdict:     https://nyay-mitra-verdict.vercel.app/api/analyze
- Health:      https://nyay-mitra-chatbot.vercel.app/api/health
- Test API:    https://nyay-mitra-chatbot.vercel.app/api/test-gemini

Frontend (if deployed):
- HTML:        https://[your-domain].vercel.app
- React:       https://[your-domain].vercel.app
```

---

## Key Benefit

**API Key is NOW:**
✅ Secure in Vercel (encrypted)
✅ Never in git history
✅ Never in code
✅ Never on your computer
✅ Only available to your app at runtime
✅ Easy to rotate instantly
✅ Environment-specific (dev/prod different keys)

---

## Next Steps

1. Read: `VERCEL_SECURE_DEPLOYMENT.md` (complete guide)
2. Generate: New Gemini API key
3. Create: Vercel account
4. Deploy: Both backends
5. Add: GEMINI_API_KEY to Vercel
6. Test: All endpoints
7. Update: Frontend URLs
8. Deploy: Frontend
9. Celebrate: 🎉 Zero-exposure production

---

## Estimated Timeline

| Task | Time | Status |
|------|------|--------|
| Read guide | 5 min | 📖 |
| Create Vercel account | 2 min | 🆓 |
| Deploy chatbot | 3 min | ⏳ |
| Deploy verdict | 3 min | ⏳ |
| Add API key | 2 min | 🔑 |
| Test endpoints | 2 min | ✅ |
| Deploy frontend | 2 min | 🚀 |
| **Total** | **~20 min** | **DONE** |

---

**Everything is ready. Let's go! 🚀**

File: VERCEL_QUICK_START.md
