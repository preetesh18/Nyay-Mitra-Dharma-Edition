# 🚀 CREATE NEW VERCEL PROJECTS - STEP BY STEP MANUAL GUIDE

**Status:** Fresh deployment structure is ready in `/vercel-deployments/`  
**GitHub:** All changes pushed to `main` branch

---

## 📋 YOUR MANUAL STEPS (You Do These!)

### ✅ Step 1: Create "Chatbot API" Project on Vercel

1. Go to: https://vercel.com/new
2. Select your GitHub repository: `Nyay-Mitra-Dharma-Edition`
3. Fill in these settings:
   - **Project Name:** `nyay-mitra-chatbot-api` (or your preference)
   - **Framework:** `Other`
   - **Root Directory:** `vercel-deployments/chatbot-api`
   - **Build Command:** `pip install -r requirements.txt`
   - **Output Directory:** `.`
4. Click "Deploy"
5. **Wait for deployment** (2-3 minutes)
6. ✅ You'll get URL: `https://nyay-mitra-chatbot-api.vercel.app`

### ✅ Step 2: Add API Key to Chatbot Project

1. In Vercel Dashboard, find your `nyay-mitra-chatbot-api` project
2. Click **Settings** → **Environment Variables**
3. Click **Add**
4. **Name:** `GEMINI_API_KEY`
5. **Value:** Your new API key from https://aistudio.google.com/app/apikey
6. **Environments:** Select ALL (Production, Preview, Development)
7. Click **Save**
8. Go to **Deployments** tab
9. Click the **3 dots** on latest deployment → **Redeploy**
10. ✅ Wait for redeployment to finish

### ✅ Step 3: Create "Verdict API" Project on Vercel

1. Go to: https://vercel.com/new
2. Select your GitHub repository: `Nyay-Mitra-Dharma-Edition`
3. Fill in these settings:
   - **Project Name:** `nyay-mitra-verdict-api` (or your preference)
   - **Framework:** `Other`
   - **Root Directory:** `vercel-deployments/verdict-api`
   - **Build Command:** `pip install -r requirements.txt`
   - **Output Directory:** `.`
4. Click "Deploy"
5. **Wait for deployment** (2-3 minutes)
6. ✅ You'll get URL: `https://nyay-mitra-verdict-api.vercel.app`

### ✅ Step 4: Add API Key to Verdict Project

1. In Vercel Dashboard, find your `nyay-mitra-verdict-api` project
2. Click **Settings** → **Environment Variables**
3. Click **Add**
4. **Name:** `GEMINI_API_KEY`
5. **Value:** Same new API key (from Step 2)
6. **Environments:** Select ALL (Production, Preview, Development)
7. Click **Save**
8. Go to **Deployments** tab
9. Click the **3 dots** on latest deployment → **Redeploy**
10. ✅ Wait for redeployment to finish

### ✅ Step 5: Test Both Backends

Open your terminal and run:

```bash
# Test Chatbot
curl https://nyay-mitra-chatbot-api.vercel.app/api/health

# Test Verdict
curl https://nyay-mitra-verdict-api.vercel.app/api/health
```

Both should return:
```json
{"status": "ok"}
```

### ✅ Step 6: Test Gemini Connection

```bash
# Test Chatbot - Verify Gemini API Key
curl -X POST https://nyay-mitra-chatbot-api.vercel.app/api/test-gemini

# Test Verdict - Verify Gemini API Key
curl -X POST https://nyay-mitra-verdict-api.vercel.app/api/test-gemini
```

Expected response:
```json
{"status": "ok", "model": "gemini-2.5-flash"}
```

If you get **403 PERMISSION_DENIED**, your API key is invalid/blocked. Generate a new one.

### ✅ Step 7: (Optional) Deploy Frontend to Vercel

1. Go to: https://vercel.com/new
2. Select your GitHub repository: `Nyay-Mitra-Dharma-Edition`
3. Fill in these settings:
   - **Project Name:** `nyay-mitra-frontend` (or your preference)
   - **Framework:** `Other`
   - **Root Directory:** `vercel-deployments/frontend`
4. Click "Deploy"
5. ✅ You'll get URL: `https://nyay-mitra-frontend.vercel.app`

---

## 📊 Final URLs

After completing all steps, you'll have:

| Component | URL | Purpose |
|-----------|-----|---------|
| **Chatbot Backend** | `https://nyay-mitra-chatbot-api.vercel.app` | API for chat functionality |
| **Verdict Backend** | `https://nyay-mitra-verdict-api.vercel.app` | API for case analysis |
| **Frontend** (Optional) | `https://nyay-mitra-frontend.vercel.app` | Web interface |

---

## 🧪 Full Test (After All Setup)

### Test 1: Chatbot Chat
```bash
curl -X POST https://nyay-mitra-chatbot-api.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is dharma?"}'
```

Expected response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "reply": "Dharma is the cosmic law and order..."
}
```

### Test 2: Verdict Analysis
```bash
curl -X POST https://nyay-mitra-verdict-api.vercel.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "plaintiff": "Person A claims breach of contract",
    "defendant": "Person B denies the agreement",
    "facts": "Email evidence shows communication"
  }'
```

Expected response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "verdict": "## Nyay Mitra Analysis\n\nBased on the facts...",
  "model": "gemini-2.5-flash"
}
```

---

## ⚠️ Troubleshooting

### Error: "Module not found: retriever"
- **Solution:** Make sure `Root Directory` is set to `vercel-deployments/chatbot-api` or `vercel-deployments/verdict-api`

### Error: "GEMINI_API_KEY is not set"
- **Solution:** 
  1. Go to project Settings
  2. Add `GEMINI_API_KEY` environment variable
  3. Redeploy project

### Error: "403 Forbidden - API key was reported as leaked"
- **Solution:**
  1. Generate new key: https://aistudio.google.com/app/apikey
  2. Update Vercel environment variable
  3. Redeploy

### Error: "Connection refused"
- **Solution:** Wait a few minutes for deployment to complete, then try again

### No response from /api/analyze
- **Solution:** 
  1. Check API key is added to environment (see Error #2)
  2. Test with `/api/test-gemini` first
  3. Check Vercel logs: Deployments → Functions → Logs

---

## ✅ Success Checklist

- [ ] Both old Vercel projects deleted
- [ ] Chatbot API project created
- [ ] Chatbot API has GEMINI_API_KEY environment variable
- [ ] Chatbot API /api/health returns 200
- [ ] Chatbot API /api/test-gemini returns ok
- [ ] Verdict API project created
- [ ] Verdict API has GEMINI_API_KEY environment variable
- [ ] Verdict API /api/health returns 200
- [ ] Verdict API /api/test-gemini returns ok
- [ ] Frontend deployed (optional)
- [ ] Standalone HTML file works locally

---

## 🎯 What's Next

Once everything is deployed:

1. **Use the frontend:**
   - Open `vercel-deployments/frontend/chatbot-standalone.html` in browser
   - Or visit `https://nyay-mitra-frontend.vercel.app`

2. **Customize frontend URLs** (if needed):
   - Edit HTML files to update API endpoints
   - Redeploy frontend

3. **Monitor logs:**
   - Vercel Dashboard → Project → Deployments → Functions → Logs

4. **Scale:**
   - Both backends are serverless and auto-scale
   - No database management needed
   - No long-term costs for low traffic

---

## 🔐 Security Notes

✅ **API Key Protection:**
- API key stored ONLY in Vercel's encrypted environment variables
- NOT in code
- NOT in git
- NOT in logs
- Easy to rotate instantly

✅ **Stateless Design:**
- No database = no data leaks
- Each request independent
- Perfect for serverless

✅ **CORS Enabled:**
- Frontend can call APIs from different domain
- Production-ready

---

## 📚 Documentation

- [Vercel Docs](https://vercel.com/docs)
- [Python on Vercel](https://vercel.com/docs/functions/python)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [Deployment Troubleshooting](https://vercel.com/docs/troubleshooting)

---

**You're ready! All your code is on GitHub. Follow the 7 steps above and you'll be live! 🚀**

---

**Questions?** Check the logs and verify against the test commands above.

**Ready to go!** ✅
