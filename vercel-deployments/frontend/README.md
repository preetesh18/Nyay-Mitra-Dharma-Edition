# Nyay Mitra - Frontend

Standalone HTML and CSS frontend for Nyay Mitra - Spiritual Advisory & Dharm Verdict Engine

##  Files

- `chatbot-standalone.html` - Chatbot interface (can be hosted standalone or connect to Vercel API)
- `dharma-verdict-standalone.html` - Verdict engine interface (can be hosted standalone or connect to Vercel API)

## API Configuration

Update the API endpoints in the HTML files to point to your Vercel backends:

```javascript
// In chatbot-standalone.html
const API_URL = 'https://nyay-mitra-chatbot-api.vercel.app';

// In dharma-verdict-standalone.html
const VERDICT_API = 'https://nyay-mitra-verdict-api.vercel.app';
```

## Deployment

### Option 1: Deploy Standalone (No Backend)
- Just open the HTML files directly in a browser
- Will use demo responses without server

### Option 2: Deploy on Vercel with Backend
1. Update API URLs in the HTML files
2. Deploy this folder to Vercel
3. Both backends must be deployed and have GEMINI_API_KEY set
4. Frontend will automatically connect to backends

## Features

- ✅ Responsive design
- ✅ Voice input/output (browser Web Speech API)
- ✅ Chat history
- ✅ Case analysis
- ✅ Markdown rendering
- ✅ Offline fallback responses
- ✅ Works with or without backend

## Build/Deploy Commands

```bash
# Deploy to Vercel
vercel deploy

# Or if already connected
vercel
```
