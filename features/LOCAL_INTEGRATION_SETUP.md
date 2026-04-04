# Local Chatbot Integration - Setup Guide

## ✅ What Was Updated

Your main website now has the chatbot links pointing to **local routes**:

### Links Updated:
1. **Features Section** (Line 500)
   - From: `https://chatbot-1-three.vercel.app/`
   - To: `/chatbot/`

2. **Footer** (Line 618)
   - From: `https://chatbot-1-three.vercel.app/`
   - To: `/chatbot/`

---

## 🚀 Next Steps: Set Up Your Chatbot Server

### Option A: Running Locally (Development)

```bash
# Navigate to chatbot directory
cd "d:\Nyay-Mitra-Dharma Edition\features\chatbot"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with:
# GEMINI_API_KEY=your_api_key_here
# FLASK_SECRET_KEY=your_secret_key_here

# Run the chatbot server
python app.py
```

**Access at:** `http://localhost:5000`

Then update your main website to point to `http://localhost:5000/chatbot/`

---

### Option B: Production Deployment

**Choose one platform:**

#### 1. **Vercel (Easiest - Recommended)**
```bash
npm install -g vercel
cd features/chatbot
vercel
```

Then update your website links to the Vercel URL or keep `/chatbot/` if serving from same domain.

#### 2. **Heroku**
```bash
heroku create your-app-name
git push heroku main
```

#### 3. **AWS/Self-Hosted**
See `DEPLOYMENT_GUIDE.md` for comprehensive instructions.

---

## ⚙️ Integration Architecture

### Current Setup:
```
Your Main Website (index.html)
    ↓
Click "Seek Wisdom" link
    ↓
Route: /chatbot/
    ↓
Chatbot Server (Flask app)
    ↓
Knowledge Base (1,088 passages)
    ↓
Gemini API
    ↓
Response to User
```

---

## 🔧 Flask Route Configuration

If you want to serve chatbot from your main app.py:

```python
from flask import Flask, render_template

app = Flask(__name__)

# Main website routes
@app.route('/')
def home():
    return render_template('index.html')

# Chatbot route
@app.route('/chatbot/')
def chatbot():
    return render_template('chatbot/index.html')

# Chatbot API route
@app.route('/api/chat', methods=['POST'])
def api_chat():
    # Import chatbot functions
    from features.chatbot.app import chat_gemini
    # ... handle request
```

---

## 📋 Verification Checklist

After setting up:

```
□ Chatbot server running (python app.py)
□ Visit http://localhost:5000 - should load chatbot
□ Main website loads at http://localhost:8000 (or your port)
□ Click "Seek Wisdom" button in features section
□ Browser navigates to /chatbot/
□ Chatbot loads with your website styling
□ Type a question and get response
□ Verify Bhagavad Gita shows Chapter/Verse format
□ Verify other texts show Sanskrit-only format
```

---

## 🔗 URL Mapping

**Local Development:**
```
Main site:    http://localhost:8000/
Chatbot:      http://localhost:8000/chatbot/
              OR http://localhost:5000/
```

**Production (Single Server):**
```
Main site:    https://yoursite.com/
Chatbot:      https://yoursite.com/chatbot/
```

**Production (Separate Servers):**
```
Main site:    https://yoursite.com/
Chatbot:      https://chatbot.yoursite.com/
              OR https://yoursite.vercel.app/
```

---

## 💡 Quick Start (Fastest Way)

1. **Open Terminal:**
   ```bash
   cd "d:\Nyay-Mitra-Dharma Edition\features\chatbot"
   ```

2. **Install & Run:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

3. **Test:**
   - Open http://localhost:5000
   - Ask a question
   - Verify it works

4. **Update Main Website:**
   - Change `/chatbot/` links to point to your server

---

## ⚠️ Important Notes

### .env File
Create `features/chatbot/.env`:
```
GEMINI_API_KEY=your_actual_api_key
FLASK_SECRET_KEY=generate_a_random_32_char_key
FLASK_ENV=development
DEBUG=True
```

**Never commit .env file to git!** Add to .gitignore:
```
.env
.env.local
```

### Ports
- Default Flask: 5000
- If port taken: `python app.py --port 5001`

### CORS (If Needed)
If running chatbot on different domain:
```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "https://yoursite.com"}})
```

---

## 🐛 Troubleshooting

### "Port 5000 already in use"
```bash
# Find what's using it
lsof -i :5000

# Or just use different port
python app.py --port 5001
```

### "ModuleNotFoundError: No module named 'flask'"
```bash
# Make sure venv is activated
pip install -r requirements.txt
```

### "GEMINI_API_KEY not found"
```bash
# Create .env file in chatbot folder
# Add: GEMINI_API_KEY=your_key_here
```

### Links still going to old Vercel URL
```bash
# Clear browser cache: Ctrl+Shift+Delete
# Or open in Incognito mode
```

---

## 📚 Documentation Reference

For more detailed information:
- `DEPLOYMENT_GUIDE.md` - Full deployment options
- `CHATBOT_MASTER_SUMMARY.md` - Project overview
- `CHATBOT_WEBSITE_INTEGRATION.md` - Integration options
- `CHATBOT_QUICK_REFERENCE.md` - Common questions

---

## ✅ You're Ready!

Your chatbot is now:
1. ✅ Updated in main website links
2. ✅ Ready to run locally
3. ✅ Ready to deploy to production
4. ✅ Integrated with your website aesthetic

**Next action:** Run `python app.py` and test locally!
