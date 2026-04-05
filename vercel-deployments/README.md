# Complete Deployment Structure

This is the new deployment structure for Nyay Mitra - Spiritual Advisory & Dharma Verdict Engine.

## Directory Structure

```
vercel-deployments/
├── chatbot-api/              # Chatbot Backend (Flask + Gemini + RAG)
│   ├── app.py
│   ├── retriever.py
│   ├── wsgi.py
│   ├── requirements.txt
│   ├── vercel.json
│   ├── .env.example
│   └── data/                 # Knowledge base files
│       ├── Bhagwad_Gita.csv
│       ├── chanakya.json
│       ├── hitopadesha.json
│       └── vidura_niti.json
│
├── verdict-api/              # Verdict Backend (Flask + Gemini + RAG)
│   ├── app.py
│   ├── retriever.py
│   ├── wsgi.py
│   ├── requirements.txt
│   ├── vercel.json
│   ├── .env.example
│   └── data/                 # Knowledge base files (same as chatbot)
│       ├── Bhagwad_Gita.csv
│       ├── chanakya.json
│       ├── hitopadesha.json
│       └── vidura_niti.json
│
└── frontend/                 # Frontend (HTML + CSS + JavaScript)
    ├── chatbot-standalone.html
    ├── dharma-verdict-standalone.html
    ├── vercel.json
    └── README.md
```

## Quick Start

### Step 1: Deploy Chatbot Backend
```bash
cd vercel-deployments/chatbot-api
vercel deploy
```
You'll get: `https://nyay-mitra-chatbot-api.vercel.app`

### Step 2: Deploy Verdict Backend
```bash
cd vercel-deployments/verdict-api
vercel deploy
```
You'll get: `https://nyay-mitra-verdict-api.vercel.app`

### Step 3: Deploy Frontend
```bash
cd vercel-deployments/frontend
vercel deploy
```
You'll get: `https://nyay-mitra-frontend.vercel.app` (or custom domain)

## Environment Variables (Manual - You Do This)

### For Chatbot API on Vercel:
1. Go to project settings
2. Add Environment Variables:
   - `GEMINI_API_KEY` = your-new-api-key
   - `FLASK_ENV` = production

### For Verdict API on Vercel:
1. Go to project settings
2. Add Environment Variables:
   - `GEMINI_API_KEY` = your-new-api-key
   - `FLASK_ENV` = production

### For Frontend on Vercel (Optional):
- No environment variables needed if using the deployed APIs

## API Endpoints

### Chatbot Backend
- `GET /api/health` - Health check
- `POST /api/test-gemini` - Test API key
- `POST /api/chat` - Send message

### Verdict Backend
- `GET /api/health` - Health check
- `POST /api/test-gemini` - Test API key
- `POST /api/analyze` - Submit case

## Features

- ✅ 100% Stateless APIs (works on serverless)
- ✅ No SQL database needed
- ✅ Standalone HTML works offline
- ✅ RAG-based knowledge retrieval
- ✅ Gemini 2.5-Flash integration
- ✅ Voice input/output support
- ✅ Session tracking
- ✅ Markdown verdict rendering

## API Key Management

Your Gemini API key is stored ONLY in Vercel's environment variables:
- ✅ Not in git
- ✅ Not in code
- ✅ Not in logs
- ✅ Encrypted by Vercel
- ✅ Easy to rotate instantly

## Testing

```bash
# Test chatbot health
curl https://nyay-mitra-chatbot-api.vercel.app/api/health

# Test verdict health
curl https://nyay-mitra-verdict-api.vercel.app/api/health

# Test Gemini connection (after adding key to Vercel)
curl -X POST https://nyay-mitra-chatbot-api.vercel.app/api/test-gemini
curl -X POST https://nyay-mitra-verdict-api.vercel.app/api/test-gemini
```

## Troubleshooting

### "No flask entrypoint found"
- ✓ Fixed - using `wsgi.py` as entrypoint
- ✓ Vercel now finds Flask app automatically

### "GEMINI_API_KEY is not set"
- Add key to Vercel Environment Variables
- Redeploy project

### API returns 403
- Your API key is leaked/blocked
- Generate new key at https://aistudio.google.com/app/apikey
- Update Vercel environment variable
- Redeploy

## Documentation

- See `FRESH_DEPLOYMENT_STEPS.md` in root for manual steps
- See each backend's README.md for details
- See `VERCEL_SECURE_DEPLOYMENT.md` for security best practices

---

**All three components are independent and can be deployed separately!**
