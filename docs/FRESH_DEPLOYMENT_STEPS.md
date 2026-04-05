# 🚀 FRESH VERCEL DEPLOYMENT - MANUAL STEPS

## Step 1: Delete Existing Vercel Projects (Manual - Do This First!)

### On Vercel Dashboard:

1. **Delete Chatbot Project:**
   - Go to https://vercel.com/dashboard
   - Find project: `nyay-mitra-chatbot`
   - Click **Settings** → scroll down → **Delete Project**
   - Confirm deletion

2. **Delete Dharma Verdict Project:**
   - Go to https://vercel.com/dashboard
   - Find project: `nyay-mitra-verdict`
   - Click **Settings** → scroll down → **Delete Project**
   - Confirm deletion

3. **Keep Frontend Project (if exists):**
   - Leave any frontend project running (we'll update it)

---

## Step 2: Prepare Your Local Repository (I Will Do This)

✅ **What I Will Do Automatically:**

```
Root Directory/
├── features/
│   ├── chatbot/                    (old - will be cleaned)
│   └── dharma_verdict/             (old - will be cleaned)
│
├── vercel-deployments/             (NEW - I'll create this)
│   ├── chatbot-api/                (NEW backend)
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   ├── vercel.json
│   │   ├── wsgi.py
│   │   ├── retriever.py
│   │   ├── data/
│   │   └── .env.example
│   │
│   ├── verdict-api/                (NEW backend)
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   ├── vercel.json
│   │   ├── wsgi.py
│   │   ├── retriever.py
│   │   ├── data/
│   │   └── .env.example
│   │
│   └── frontend/                   (existing - will update)
│       ├── chatbot-standalone.html
│       ├── dharma-verdict-standalone.html
│       ├── vercel.json
│       └── .env.example
│
└── README_DEPLOYMENT.md            (deployment guide)
```

---

## Step 3: Configure Environment Variables on Vercel (Manual)

After I set up the directories, you will:

### For Chatbot API Project:
1. Go to Vercel → `nyay-mitra-chatbot-api`
2. Settings → Environment Variables
3. Add: `GEMINI_API_KEY` = your-new-key
4. Redeploy

### For Verdict API Project:
1. Go to Vercel → `nyay-mitra-verdict-api`
2. Settings → Environment Variables
3. Add: `GEMINI_API_KEY` = your-new-key
4. Redeploy

### For Frontend Project:
1. Go to Vercel → `nyay-mitra-frontend`
2. Settings → Environment Variables
3. Add these (I will provide exact values):
   - `VITE_CHATBOT_API` = https://nyay-mitra-chatbot-api.vercel.app
   - `VITE_VERDICT_API` = https://nyay-mitra-verdict-api.vercel.app
4. Redeploy

---

## Step 4: Get Your New Vercel URLs (You Will See These)

After deployment, you'll have:
- **Chatbot API:** `https://nyay-mitra-chatbot-api.vercel.app`
- **Verdict API:** `https://nyay-mitra-verdict-api.vercel.app`
- **Frontend:** `https://nyay-mitra-frontend.vercel.app` (or your custom domain)

---

## Step 5: Test Everything

After all 3 are deployed:

```bash
# Test chatbot backend
curl https://nyay-mitra-chatbot-api.vercel.app/api/health

# Test verdict backend
curl https://nyay-mitra-verdict-api.vercel.app/api/health

# Test frontend loads
curl https://nyay-mitra-frontend.vercel.app
```

---

## 📝 What You Must Do Manually

1. ✅ Delete `nyay-mitra-chatbot` project from Vercel
2. ✅ Delete `nyay-mitra-verdict` project from Vercel
3. ✅ Generate NEW Gemini API key (if not done already)
4. ✅ After repo is updated: Create 2 new Vercel projects (chatbot-api, verdict-api)
5. ✅ Add GEMINI_API_KEY to each project
6. ✅ Add environment variables to frontend project
7. ✅ Redeploy all 3

---

## 🎯 Current Status

- Deleting old projects: **WAITING FOR YOU** ⏳
- Setting up new directory structure: **I'LL DO AUTOMATICALLY** ✅
- Creating Vercel configs: **I'LL DO AUTOMATICALLY** ✅
- Pushing to GitHub: **I'LL DO AUTOMATICALLY** ✅
- Creating new projects on Vercel: **YOU WILL DO** (simple clicks)
- Adding API keys: **YOU WILL DO** (simple paste)

---

## ⏭️ Tell Me When Ready

Once you:
1. Delete the 2 old projects on Vercel dashboard
2. Generate new Gemini API key (from https://aistudio.google.com/app/apikey)

**Then reply: "Ready! I've deleted old projects and have my new API key"**

I'll immediately:
1. Create the new directory structure
2. Copy all files to proper locations
3. Update vercel.json files
4. Create environment variable templates
5. Push everything to GitHub
6. Give you exact steps to create 2 new Vercel projects

---

**Waiting for you to complete Step 1 & generate API key! 🚀**
