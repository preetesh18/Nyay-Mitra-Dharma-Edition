# 🚨 CRITICAL: API KEY ISSUE & COMPLETE SOLUTION

## Problem Identified

### Root Cause 1: Compromised Gemini API Key ❌
```
GEMINI_API_KEY = AIzaSyDRM4PCYpRITerkohJB7MH1Sv5wa9mk9C8
Status: ⛔ LEAKED - Blocked by Google
Error: "Your API key was reported as leaked. Please use another API key."
```

**Why it's not working in production:**
- The API key has been publicly exposed (likely in git history)
- Google automatically blocked it
- Any requests using this key will return 403 Forbidden

### Root Cause 2: Missing Templates ❌
```
jinja2.exceptions.TemplateNotFound: index.html
```
When we cleaned up Flask files, we deleted `templates/` directory, but Flask still tries to render them.

---

## Solution: Complete React + Flask Refactor

### Step 1: Generate New Gemini API Key

**DO THIS FIRST:**

1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Select your project
4. Copy the new key
5. Update your `.env` files:

```env
# features/chatbot/.env
GEMINI_API_KEY=YOUR_NEW_KEY_HERE

# features/dharma_verdict/.env
GEMINI_API_KEY=YOUR_NEW_KEY_HERE
```

**🔒 Security Tips:**
- Add `.env` to `.gitignore`
- **DO NOT** commit API keys to git
- Use different keys for dev/production
- Rotate keys regularly
- Set up IP restrictions in Google Cloud Console

---

### Step 2: Modified Flask Backend (API-Only)

The Flask apps are now **API servers only** (no template rendering):

#### Chatbot Backend: `features/chatbot/app.py`

**Endpoints:**
- `GET /api/health` - Server status
- `POST /api/test-gemini` - Test API connectivity
- `POST /api/chat` - Send message & get response
- `POST /api/session` - Create new session
- `GET /api/session/<id>` - Get session history
- `POST /api/reset` - Reset session

**Response Format:**
```json
{
  "session_id": "uuid",
  "reply": "Gemini response text",
  "model": "gemini-2.5-flash"
}
```

#### Dharma Verdict Backend: `features/dharma_verdict/app.py`

**Endpoints:**
- `GET /api/health` - Server status
- `POST /api/test-gemini` - Test API connectivity
- `POST /api/analyze` - Submit case & get verdict
- `POST /api/test-gemini` - Test connectivity

**Request Format:**
```json
{
  "plaintiff": "...",
  "defendant": "...",
  "facts": "..."
}
```

**Response Format:**
```json
{
  "verdict": "Markdown text",
  "model": "gemini-2.5-flash",
  "passages_used": 5
}
```

---

### Step 3: React Frontend (Separate Directory)

Create a new React app that connects to both backends:

**Directory Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatBot.jsx
│   │   └── DharmaVerdict.jsx
│   ├── pages/
│   │   ├── ChatPage.jsx
│   │   └── VerdictPage.jsx
│   ├── services/
│   │   ├── chatApi.js
│   │   └── verdictApi.js
│   ├── App.jsx
│   └── styles/
│       ├── chatbot.css
│       └── verdict.css
├── package.json
└── vite.config.js
```

---

### Step 4: Setup Instructions

#### 4.1 Create React App

```bash
cd d:\Nyay-Mitra-Dharma Edition

# Create React app with Vite
npm create vite@latest frontend -- --template react

cd frontend
npm install

# Install Axios for API calls
npm install axios

# Install routing
npm install react-router-dom
```

#### 4.2 Update `.env` Files

```bash
# features/chatbot/.env
GEMINI_API_KEY=YOUR_NEW_KEY_HERE
FLASK_SECRET_KEY=naya-mitra-secure-key-2024
FLASK_ENV=production
PORT=5000

# features/dharma_verdict/.env
GEMINI_API_KEY=YOUR_NEW_KEY_HERE
FLASK_SECRET_KEY=nyay-mitra-dharma-change-me
FLASK_ENV=production
PORT=5001
```

#### 4.3 Run All Services

**Terminal 1 - Chatbot Backend:**
```bash
cd features/chatbot
python app.py
# Runs on http://127.0.0.1:5000
```

**Terminal 2 - Dharma Verdict Backend:**
```bash
cd features/dharma_verdict
python app.py
# Runs on http://127.0.0.1:5001
```

**Terminal 3 - React Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://127.0.0.1:5173
```

---

### Step 5: Python Changes Made

#### `features/chatbot/app.py`

**Key Changes:**
1. ✅ Added `CORS` support for React frontend
2. ✅ Added `/api/test-gemini` endpoint to test connectivity
3. ✅ Made `/api/chat` return JSON only (no templates)
4. ✅ Added health check endpoint
5. ✅ Proper error messages for API key issues
6. ✅ Session management in memory (not Flask session)

**Important Note:**
- Removed `render_template("index.html")` 
- Now serves **API endpoints only**
- React frontend communicates via `/api/` endpoints

#### `features/dharma_verdict/app.py`

**Key Changes:**
1. ✅ Added `CORS` support
2. ✅ `/api/analyze` endpoint for verdict generation
3. ✅ `/api/test-gemini` to verify API key
4. ✅ Removed template rendering
5. ✅ RAG retrieval integrated into API

---

## Testing the Setup

### 1. Test API Key Connectivity
```bash
curl -X POST http://127.0.0.1:5000/api/test-gemini
```

**Expected Response (if key is valid):**
```json
{
  "status": "ok",
  "model": "gemini-2.5-flash",
  "message": "Gemini API is working"
}
```

### 2. Test Chat Endpoint
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is dharma?"}'
```

### 3. Test Verdict Endpoint
```bash
curl -X POST http://127.0.0.1:5001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "plaintiff": "...",
    "defendant": "...",
    "facts": "..."
  }'
```

---

## Common Issues & Solutions

### Issue: "API key was reported as leaked"
**Solution:** Generate a new API key at https://aistudio.google.com/app/apikey

### Issue: CORS errors in React
**Solution:** Ensure `CORS(app)` is enabled in Flask
```python
from flask_cors import CORS
CORS(app)
```

### Issue: "Templates not found"
**Solution:** Backends are now API-only. Use React frontend instead.

### Issue: Session data not persisting
**Solution:** Sessions stored in-memory. For production, use Redis or database.

---

## Production Deployment

### For Local Development ✅
Files are now ready. Just:
1. Update API keys
2. Run all 3 services
3. Access React app at http://127.0.0.1:5173

### For Production 🚀
- Use `.env` files with proper secrets management
- Set up HTTPS/TLS
- Use production WSGI server (Gunicorn)
- Set up database for session persistence
- Configure proper CORS for your domain
- Implement rate limiting
- Add authentication if needed

---

## File Locations

| File | Location | Purpose |
|------|----------|---------|
| Chatbot Backend | `features/chatbot/app.py` | API server |
| Verdict Backend | `features/dharma_verdict/app.py` | API server |
| React Frontend | `frontend/` | User interface |
| Chatbot API Key | `features/chatbot/.env` | Configuration |
| Verdict API Key | `features/dharma_verdict/.env` | Configuration |

---

## Quick Reference

| Service | Port | Status | URL |
|---------|------|--------|-----|
| Chatbot API | 5000 | ← Python Flask | http://127.0.0.1:5000/api/* |
| Verdict API | 5001 | ← Python Flask | http://127.0.0.1:5001/api/* |
| React Frontend | 5173 | ← Vite Dev | http://127.0.0.1:5173 |

---

## Next Steps

1. **Update API Key** (CRITICAL!)
2. Run test commands above
3. Create React components using provided API
4. Deploy to production

For detailed React component examples, see `REACT_SETUP.md`

---

**Last Updated:** April 6, 2026
**Status:** ✅ Ready for implementation
