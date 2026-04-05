# 🎯 Nyay Mitra - Complete Deployment Guide

## Current Status ✅

You now have:
1. ✅ **Two standalone HTML files** (for quick access without setup)
2. ✅ **Flask API backends** (modified to be API-only)
3. ✅ **Complete React setup guide** (modern frontend)
4. ✅ **Critical issue identified** (Gemini API key leaked)

---

## 🚨 IMMEDIATE ACTION REQUIRED

### Step 1: Generate New Gemini API Key (DO THIS FIRST!)

**Why:** Your current API key is blocked by Google

```
Current Key Status: ❌ LEAKED & BLOCKED
New Key Status: ✅ REQUIRED
```

**How to get a new key:**

1. Visit: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Keep it in a safe place
4. **NEVER** commit it to git

### Step 2: Update Both `.env` Files

**File:** `features/chatbot/.env`
```env
GEMINI_API_KEY=YOUR_NEW_KEY_HERE
FLASK_SECRET_KEY=naya-mitra-secure-key-2024
FLASK_ENV=production
PORT=5000
```

**File:** `features/dharma_verdict/.env`
```env
GEMINI_API_KEY=YOUR_NEW_KEY_HERE
FLASK_SECRET_KEY=nyay-mitra-dharma-change-me
FLASK_ENV=production
PORT=5001
```

**Save files and restart!**

---

## 📋 Three Ways to Run Your Website

### Option A: Quick HTML (No Server Needed) ⚡

**Perfect for:** Quick testing, offline use, no setup

```bash
# Just open this file directly in your browser:
d:\Nyay-Mitra-Dharma Edition\chatbot-standalone.html
d:\Nyay-Mitra-Dharma Edition\dharma-verdict-standalone.html
```

**Features:**
- ✅ Works immediately
- ✅ No API key needed
- ✅ Uses demo responses
- ✅ Voice features included

**Drawback:**
- ❌ No real Gemini responses
- ❌ No API connectivity

---

### Option B: Flask Only (Python Backend + HTML) 🐍

**Perfect for:** Simple deployment, production

**Setup:**
```bash
# Terminal 1: Chatbot
cd features/chatbot
pip install -r requirements.txt
export GEMINI_API_KEY=YOUR_NEW_KEY_HERE
python app.py
# Runs on http://127.0.0.1:5000

# Terminal 2: Dharma Verdict
cd features/dharma_verdict
pip install -r requirements.txt
export GEMINI_API_KEY=YOUR_NEW_KEY_HERE
python app.py
# Runs on http://127.0.0.1:5001
```

**Access:**
- Chatbot: http://127.0.0.1:5000
- Verdict: http://127.0.0.1:5001
- Uses `chatbot-standalone.html` and `dharma-verdict-standalone.html` directly

**Features:**
- ✅ Real Gemini API responses
- ✅ Voice input/output
- ✅ Chat history
- ✅ Beautiful UI

**Installation:**
1. Update API keys in `.env`
2. Run the commands above
3. Open in browser

---

### Option C: React + Flask (Modern Stack) 🚀

**Perfect for:** Full-featured web app, scalability, team development

**Complete Setup:**

```bash
# 1. Create React app
cd "d:\Nyay-Mitra-Dharma Edition"
npm create vite@latest frontend -- --template react
cd frontend
npm install axios react-router-dom

# 2. Create config
echo "VITE_CHATBOT_API=http://127.0.0.1:5000" > .env
echo "VITE_VERDICT_API=http://127.0.0.1:5001" >> .env

# 3. Terminal 1: Chatbot Backend
cd features/chatbot
python app.py

# 4. Terminal 2: Dharma Verdict Backend
cd features/dharma_verdict
python app.py

# 5. Terminal 3: React Frontend
cd frontend
npm run dev
# Runs on http://127.0.0.1:5173
```

**Components Provided:**
- ✅ ChatBot component
- ✅ DilarmaVerdict component
- ✅ Message bubbles
- ✅ Form handling
- ✅ API services

**Features:**
- ✅ Modern, responsive UI
- ✅ Real Gemini responses
- ✅ Professional architecture
- ✅ Easy to extend

---

## 📂 File Structure

```
d:\Nyay-Mitra-Dharma Edition\
├── chatbot-standalone.html          ← Open directly in browser
├── dharma-verdict-standalone.html   ← Open directly in browser
├── CRITICAL_FIX.md                  ← READ THIS FOR API KEY ISSUE
├── REACT_SETUP.md                   ← React implementation guide
├── STANDALONE_HTML_GUIDE.md         ← HTML-only guide
│
├── features/
│   ├── chatbot/
│   │   ├── app.py                   ← API backend (PORT 5000)
│   │   ├── retriever.py             ← RAG logic
│   │   ├── requirements.txt          ← Python deps
│   │   └── data/                     ← Knowledge base
│   │
│   └── dharma_verdict/
│       ├── app.py                   ← API backend (PORT 5001)
│       ├── retriever.py             ← RAG logic
│       ├── requirements.txt          ← Python deps
│       └── data/                     ← Knowledge base
│
└── frontend/                         ← Create this with React
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   └── App.jsx
    └── package.json
```

---

## 🔒 Security Checklist

**Before Production:**

- [ ] New API key generated
- [ ] API key NOT in git (add .env to .gitignore)
- [ ] HTTPS/TLS enabled
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Input validation added
- [ ] Error messages sanitized
- [ ] Logging configured
- [ ] Database setup (if needed)
- [ ] Backup strategy planned

---

## 📊 API Endpoints Reference

### Chatbot Backend (Port 5000)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Server status check |
| POST | `/api/test-gemini` | Test API key connectivity |
| POST | `/api/chat` | Send message & get response |
| POST | `/api/session` | Create new session |
| GET | `/api/session/<id>` | Get session history |
| POST | `/api/reset` | Reset session |

### Dharma Verdict Backend (Port 5001)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Server status check |
| POST | `/api/test-gemini` | Test API key connectivity |
| POST | `/api/analyze` | Submit case & get verdict |

---

## 🧪 Testing

### Test 1: Health Check
```bash
# Chatbot
curl http://127.0.0.1:5000/api/health

# Dharma Verdict
curl http://127.0.0.1:5001/api/health
```

**Expected:**
```json
{
  "status": "ok",
  "api_key_configured": true
}
```

### Test 2: Gemini Connectivity
```bash
curl -X POST http://127.0.0.1:5000/api/test-gemini
```

**Expected (with valid key):**
```json
{
  "status": "ok",
  "model": "gemini-2.5-flash",
  "message": "Gemini API is working"
}
```

### Test 3: Send Message
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is dharma?"}'
```

---

## ⚠️ Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| 500 Internal Error | Template not found | Use standalone HTML or React |
| 403 API Key Error | Key is leaked/blocked | Generate new key at aistudio.google.com |
| CORS Error | Frontend trying different origin | Ensure CORS enabled in Flask |
| Port already in use | Another app on same port | Change port or kill process |
| Timeout | Server too slow | Increase timeout, check internet |

---

## 🚀 Deployment Options

### Option 1: Local Machine
```bash
# Just run all 3 services locally
python app.py        # Terminal 1 & 2
npm run dev          # Terminal 3
```

### Option 2: Docker
```dockerfile
FROM python:3.11
RUN pip install flask httpx flask-cors python-dotenv
COPY . /app
WORKDIR /app/features/chatbot
CMD ["python", "app.py"]
```

### Option 3: Cloud Platforms
- **Vercel** - React frontend
- **Railway** - Flask backends
- **Heroku** - Python apps
- **AWS/GCP/Azure** - Full stack

### Option 4: Standalone Executable
- Use PyInstaller to bundle Python
- Use `npm build` for React
- Create desktop app with Electron

---

## 📞 Support

### Quick Fixes
1. **API key issue?** → Visit https://aistudio.google.com/app/apikey
2. **Port conflict?** → Change PORT in .env or kill process
3. **Can't connect?** → Check all 3 services are running
4. **React won't load?** → Check browser console (F12)
5. **Response slow?** → Check internet, increase timeout

### Debug Mode
```bash
# Flask debug mode
export FLASK_ENV=development
python app.py

# React debug
npm run dev -- --host

# Check logs
tail -f features/chatbot/logs/*.jsonl
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `CRITICAL_FIX.md` | API key issue & solution |
| `REACT_SETUP.md` | React implementation guide |
| `STANDALONE_HTML_GUIDE.md` | HTML-only usage |
| `README.md` | Original project info |

---

## ✅ Implementation Checklist

- [ ] Read CRITICAL_FIX.md
- [ ] Generate new Gemini API key
- [ ] Update .env files
- [ ] Choose deployment option (A, B, or C)
- [ ] Install dependencies
- [ ] Run backend(s)
- [ ] Test health endpoints
- [ ] Test Gemini connectivity
- [ ] Access frontend
- [ ] Test chat/verdict functionality
- [ ] Deploy to production

---

## 🎯 Next Steps

### For Quick Testing (5 minutes)
1. Open `chatbot-standalone.html` directly
2. Open `dharma-verdict-standalone.html` directly
3. No server needed, works offline

### For Production (30 minutes)
1. Generate new API key
2. Update .env files
3. Run Flask backends
4. Open in browser
5. Done!

### For Full React App (60 minutes)
1. Follow REACT_SETUP.md
2. Create React project
3. Run all 3 services
4. Access React frontend
5. Deploy

---

**Status:** ✅ Ready to Deploy
**Last Updated:** April 6, 2026
**API Key Status:** ⚠️ NEEDS UPDATE - Generate new key immediately!

---

## Quick Command Reference

```bash
# Generate new Gemini API key
https://aistudio.google.com/app/apikey

# Update API keys in both .env files
# features/chatbot/.env
# features/dharma_verdict/.env

# Terminal 1: Chatbot Backend
cd features/chatbot && python app.py

# Terminal 2: Dharma Verdict Backend
cd features/dharma_verdict && python app.py

# Terminal 3: React Frontend (optional)
cd frontend && npm run dev

# Access Points
# http://127.0.0.1:5000        ← Chatbot standalone (if using standalone)
# http://127.0.0.1:5001        ← Verdict standalone (if using standalone)
# http://127.0.0.1:5173        ← React frontend (if using React)

# Direct HTML (no server needed)
d:\Nyay-Mitra-Dharma Edition\chatbot-standalone.html
d:\Nyay-Mitra-Dharma Edition\dharma-verdict-standalone.html
```

**You're all set! Choose your deployment method and go live.** 🚀
