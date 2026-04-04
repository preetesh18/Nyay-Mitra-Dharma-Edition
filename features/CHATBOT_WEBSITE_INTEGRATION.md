# Chatbot Integration with Main Website

## 🎯 Integration Overview

Your chatbot feature can be integrated with your main website in several ways:

---

## Option 1: Separate Flask Route (Recommended)

### Step 1: Update Your Main `index.html`

Add a link to the chatbot:

```html
<!-- In your main website's navigation -->
<li><a href="/chatbot">Dharma Adviser</a></li>

<!-- OR add a button in features section -->
<button onclick="window.location.href='/chatbot'" class="btn-o">Ask Naya Mitra</button>
```

### Step 2: Create Router in Main App

Add to your main `app.py` (or create `chatbot_routes.py`):

```python
# In your main app.py or separate file
from flask import Blueprint, render_template
import os

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@chatbot_bp.route('/')
def chatbot():
    return render_template('chatbot.html')

# Register blueprint in main app init
app.register_blueprint(chatbot_bp)
```

### Step 3: Copy the Chatbot

```
Copy entire /features/chatbot folder to your main project:

your-website/
├── chatbot/                <- Copy here
│   ├── app.py
│   ├── retriever.py
│   ├── requirements.txt
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   └── js/app.js
│   └── data/
│       ├── Bhagwad_Gita.csv
│       ├── chanakya.json
│       ├── hitopadesha.json
│       └── vidura_niti.json
```

### Step 4: Update Paths in Chatbot Code

In `chatbot/app.py`, update the template path:

```python
# Change from:
return render_template("index.html")

# To:
return render_template("chatbot/templates/index.html")
```

In `chatbot/retriever.py`, update the data path:

```python
# Change from:
DATA_DIR = Path(__file__).parent / "data"

# To:
DATA_DIR = Path(__file__).parent / "chatbot" / "data"
```

---

## Option 2: Iframe Embed

### In Your Main Website

```html
<!-- Embed chatbot as iframe -->
<div class="chatbot-container" style="height: 600px; border: 1px solid #ccc;">
  <iframe 
    src="http://localhost:5000/chatbot" 
    style="width: 100%; height: 100%; border: none;">
  </iframe>
</div>

<!-- Or with custom styling -->
<style>
  .chatbot-container {
    max-width: 800px;
    margin: 2rem auto;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  }
  
  .chatbot-container iframe {
    width: 100%;
    height: 100%;
    border: none;
  }
</style>
```

**Pros:** Easy to implement, isolated styling
**Cons:** Limited integration, separate scrollbars

---

## Option 3: Direct Integration (Advanced)

### Combine Both Frontend & Backend

```
/
├── app.py (main + chatbot_routes)
├── retriever.py (shared)
├── templates/
│   ├── index.html (main website)
│   └── chatbot.html (restyled chatbot)
├── static/
│   ├── js/
│   │   ├── app.js (main)
│   │   └── chatbot.js (chatbot logic)
│   └── css/
│       └── styles.css (shared + chatbot)
└── data/
    ├── Bhagwad_Gita.csv
    └── [other data files]
```

**Pros:** Full integration, consistent experience
**Cons:** More setup required

---

## 📋 Quick Integration Checklist

### For Option 1 (Recommended)

```
□ 1. Copy /features/chatbot to main project folder
□ 2. Update DATA_DIR path in retriever.py
□ 3. Update template path in app.py
□ 4. Create blueprint for chatbot routes
□ 5. Register blueprint in main app
□ 6. Add navigation link to chatbot
□ 7. Test: Visit /chatbot in browser
□ 8. Verify: Chat works, styling matches
□ 9. Voice: Test microphone input
□ 10. Deploy: Push to production
```

---

## 🔗 URL Structure

### Option 1: Separate Route
```
Main site:    http://yoursite.com/
Chatbot:      http://yoursite.com/chatbot/
API:          http://yoursite.com/api/chat

Access from nav:
<a href="/chatbot">Ask Wisdom</a>
```

### Option 2: Subdirectory
```
Main site:    http://yoursite.com/
Chatbot:      http://yoursite.com/wisdom/
API:          http://yoursite.com/wisdom/api/chat
```

### Option 3: Same Domain Embed
```
Load on multiple pages with iframe
Keeps session if same domain
```

---

## 📝 Environment Setup

### Main Project `.env`

```
# Keep existing config
GEMINI_API_KEY=your_key_here
FLASK_SECRET_KEY=your_secret_key

# Add chatbot-specific (if needed)
LOGS_DIR=./chatbot/logs
CHATBOT_DATA_DIR=./chatbot/data
```

### Requirements

Add to main project's `requirements.txt`:

```
flask>=3.0.0
httpx>=0.27.0
python-dotenv>=1.0.0
gunicorn>=21.0.0
```

(Most likely already there from other features)

---

## 🚀 Deployment Strategies

### Local Development
```bash
# Run main app with chatbot
python app.py

# Access at:
# http://localhost:5000/
# http://localhost:5000/chatbot/
```

### Production (Vercel/Cloud)

**1. Update vercel.json:**
```json
{
  "builds": [
    {"src": "app.py", "use": "@vercel/python"}
  ],
  "routes": [
    {"src": "/(.*)", "dest": "app.py"}
  ]
}
```

**2. Ensure paths are correct:**
```python
# Use relative paths that work on cloud
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "chatbot" / "data"
LOGS_DIR = BASE_DIR / "chatbot" / "logs"
```

### With Gunicorn
```bash
gunicorn -c gunicorn.conf.py app:app

# Or with specific workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🔐 Security Considerations

### CORS Headers
```python
from flask_cors import CORS

CORS(app)  # Allow cross-origin if embedding

# Or specific domains:
CORS(app, origins=["yoursite.com", "www.yoursite.com"])
```

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/chat", methods=["POST"])
@limiter.limit("10 per minute")
def api_chat():
    # ... your code
```

### API Key Protection
```python
# Never expose keys in frontend
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in environment")
```

---

## 🧪 Testing Integration

### Test 1: Navigation
```
1. Open main website
2. Click on chatbot link
3. Verify URL changed to /chatbot
4. Verify styling matches main site
```

### Test 2: Chat Functionality
```
1. Type a question
2. Click send button
3. Wait for response
4. Verify message appears correctly
5. Verify formatting is correct
```

### Test 3: Voice Features
```
1. Click microphone button
2. Speak a question
3. Verify transcription appears
4. Wait for response
5. Verify voice response plays (if enabled)
```

### Test 4: Session Persistence
```
1. Ask first question
2. Refresh page (F5)
3. Verify chat history persists
4. Ask follow-up question
5. Verify context maintained
```

### Test 5: Responsive Design
```
1. Desktop: 1920px wide - ✓
2. Tablet: 768px wide - ✓
3. Mobile: 375px wide - ✓
4. Touch: Test buttons - ✓
5. Scroll: Check chat history - ✓
```

---

## 📊 Performance Tips

### 1. Lazy Load Data
```python
# Load data only when needed
_corpus = None

def get_corpus():
    global _corpus
    if _corpus is None:
        _corpus = load_all_data()
    return _corpus
```

### 2. Cache Responses
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_retrieve(query: str):
    return retrieve(query, top_k=4)
```

### 3. Optimize Assets
```html
<!-- Defer non-critical JS -->
<script src="app.js" defer></script>

<!-- Preload critical fonts -->
<link rel="preload" as="font" href="fonts/cinzel.woff2">
```

### 4. Enable Compression
```python
# In Flask
from flask_compress import Compress

Compress(app)
```

---

## 🎯 Example Integration (Complete)

### Main app.py with Chatbot

```python
from flask import Flask, render_template, request, jsonify, session
from features.chatbot.retriever import retrieve, format_passages_for_prompt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# ── Main website routes ──
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/studies")
def studies():
    return render_template("studies.html")

# ── Chatbot routes ──
@app.route("/chatbot/")
def chatbot():
    return render_template("chatbot/templates/index.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    # Chatbot chat endpoint
    from features.chatbot.app import chat_gemini
    try:
        data = request.get_json()
        user_msg = data.get("message", "").strip()
        if not user_msg:
            return jsonify({"error": "Empty message"}), 400
        
        history = session.get("history", [])
        history.append({"role": "user", "content": user_msg})
        
        reply = chat_gemini(history, user_msg)
        
        history.append({"role": "assistant", "content": reply})
        session["history"] = history[-6:]  # Keep last 6 messages
        
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Static files ──
@app.route("/static/<path:filename>")
def static_files(filename):
    return app.send_static_file(filename)

if __name__ == "__main__":
    app.run(debug=True)
```

---

## ✅ Final Checklist

- [ ] Chatbot files copied to main project
- [ ] Paths updated in app.py
- [ ] Paths updated in retriever.py
- [ ] Routes added to main app
- [ ] Navigation links updated
- [ ] Local testing complete
- [ ] Voice features work
- [ ] Styling matches main site
- [ ] Responsive design verified
- [ ] Light/Dark mode works
- [ ] Session persistence works
- [ ] Deployed to production

---

## 📞 Troubleshooting

### "Module not found" error
```python
# Add to main app.py:
import sys
sys.path.insert(0, os.path.dirname(__file__))
```

### "Data files not found"
```python
# Check path construction
print(DATA_DIR)  # Debug path
print(DATA_DIR.exists())  # Verify exists
```

### "Styles not loading"
```html
<!-- Verify static files route works -->
<!-- Check browser network tab -->
<!-- Verify file paths are correct -->
```

### "Voice not working"
```javascript
// Check browser permissions
// Verify microphone access granted
// Check console for errors
```

---

**Status:** ✅ **Ready for Integration**

Your chatbot is styled, functional, and ready to embed in your main website!
