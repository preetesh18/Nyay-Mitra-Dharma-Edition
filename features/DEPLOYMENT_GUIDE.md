# Chatbot Deployment Guide

## 🚀 Deployment Overview

This guide covers deploying your optimized Nyay Mitra Chatbot to production with your main website.

---

## Part 1: Pre-Deployment Checklist

### Code Verification
```
□ All Python code syntax checked (no import errors)
□ All template files in place 
□ Static files (JS, CSS) loading correctly
□ Data files accessible from deployment location
□ Environment variables configured
□ No hardcoded paths or credentials
```

### Testing Checklist
```
□ Local: Chat works with test queries
□ Local: Bhagavad Gita shows Chapter/Verse format
□ Local: Other texts show Sanskrit-only format
□ Local: Dharmic Guidance section present
□ Local: Voice input/output functional
□ Local: Light/Dark mode toggling works
□ Local: Responsive on mobile/tablet
□ Local: Session history persists after refresh
```

### Performance Checklist
```
□ Knowledge base loads within 5 seconds
□ First chat response within 3 seconds
□ Subsequent responses within 2 seconds
□ No memory leaks (check with long sessions)
□ Asset files compressed
□ Database queries optimized
```

---

## Part 2: File Structure for Deployment

### Recommended Structure
```
your-site-repo/
│
├── app.py (main Flask app with integrated chatbot routes)
├── requirements.txt (all dependencies)
├── .env (environment variables - DO NOT commit)
├── .gitignore (include .env, __pycache__, logs/)
│
├── templates/
│   ├── index.html (main website)
│   └── chatbot.html (chatbot interface)
│
├── static/
│   ├── js/
│   │   ├── app.js (main website)
│   │   ├── chatbot.js (chatbot)
│   │   └── shared.js (shared utilities)
│   ├── css/
│   │   ├── styles.css (main website)
│   │   └── chatbot.css (chatbot - embedded in HTML)
│   └── fonts/
│
├── modules/
│   ├── __init__.py
│   └── retriever.py (knowledge base retrieval)
│
├── data/
│   ├── Bhagwad_Gita.csv
│   ├── chanakya.json
│   ├── vidura_niti.json
│   └── hitopadesha.json
│
├── logs/ (auto-created, add to .gitignore)
│
├── config/
│   ├── gunicorn.conf.py
│   └── vercel.json (if using Vercel)
│
└── docs/
    ├── CHATBOT_OPTIMIZATION_SUMMARY.md
    ├── CHATBOT_FRONTEND_STYLING_GUIDE.md
    ├── CHATBOT_WEBSITE_INTEGRATION.md
    └── DEPLOYMENT_GUIDE.md
```

---

## Part 3: Environment Configuration

### Create `.env` File (DO NOT COMMIT)

```bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CRITICAL: Never commit this file to git
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Flask Configuration
FLASK_ENV=production
FLASK_SECRET_KEY=your-secret-key-here-min-32-chars

# Gemini API Configuration  
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODELS=gemini-2.0-flash,gemini-2.0-flash-lite

# Application Settings
DEBUG=False
HOST=0.0.0.0
PORT=5000

# File Paths (relative to app root)
DATA_DIR=./data
LOGS_DIR=./logs
TEMPLATE_DIR=./templates
STATIC_DIR=./static

# Logging
LOGGING_LEVEL=INFO
LOG_FORMAT=json  # or text

# Deployment Target (development|staging|production)
TARGET_ENV=production
```

### `.gitignore` Configuration

```
# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Logs
logs/
*.log
*.jsonl

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Database
*.db
*.sqlite
```

---

## Part 4: Dependency Management

### Update `requirements.txt`

```
flask==3.0.0
flask-cors==4.0.0
flask-compress==1.14.0
flask-limiter==3.5.0
httpx==0.27.0
python-dotenv==1.0.0
gunicorn==21.2.0
google-generativeai==0.3.0
numpy==1.24.0
scikit-learn==1.3.0
pandas==2.1.0
```

### Installation for Production

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt --no-cache-dir

# Verify installation
python -c "import flask, httpx, dotenv; print('✓ All deps installed')"
```

---

## Part 5: Production Configurations

### Gunicorn Configuration (`config/gunicorn.conf.py`)

```python
import multiprocessing
import os

# Server configuration
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "nyay-mitra-chatbot"

# Server hooks
def on_starting(server):
    print("🚀 Nyay Mitra Chatbot starting...")

def on_exit(server):
    print("🛑 Nyay Mitra Chatbot stopped")

def post_fork(server, worker):
    # Reset database connections for new worker
    pass
```

### Production Flask Configuration

```python
# In app.py
class ProductionConfig:
    DEBUG = False
    TESTING = False
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600
    
    # Compression
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 1024
    
    # Logging
    LOG_LEVEL = 'INFO'
    
    # API
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

app.config.from_object(ProductionConfig)
```

---

## Part 6: Deployment to Vercel

### Step 1: Create `vercel.json`

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "installCommand": "pip install -r requirements.txt",
  "env": {
    "FLASK_ENV": "production",
    "PYTHONUNBUFFERED": "1"
  },
  "functions": {
    "app.py": {
      "memory": 3008,
      "maxDuration": 60
    }
  },
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Step 2: Update `app.py` for Vercel

```python
from flask import Flask
from vercel_runtime_wsgi import handle
import os
from pathlib import Path

app = Flask(__name__, 
    static_folder=str(Path(__file__).parent / "static"),
    template_folder=str(Path(__file__).parent / "templates")
)

# Use /tmp for logs on Vercel (read-only file system)
LOGS_DIR = os.getenv("LOGS_DIR", "/tmp/nyay-mitra-logs")
Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)

# Routes here...

# Vercel handler
app = handle(app)
```

### Step 3: Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel deploy

# See logs
vercel logs --follow

# Rollback if needed
vercel rollback
```

---

## Part 7: Deployment to Heroku

### Step 1: Create `Procfile`

```
web: gunicorn -c config/gunicorn.conf.py app:app
```

### Step 2: Deploy

```bash
# Install Heroku CLI
npm i -g heroku

# Login to Heroku
heroku login

# Create app
heroku create nyay-mitra-chatbot

# Add environment variables
heroku config:set GEMINI_API_KEY=your_key_here
heroku config:set FLASK_SECRET_KEY=your_secret_here
heroku config:set TARGET_ENV=production

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Scale workers if needed
heroku ps:scale web=2
```

---

## Part 8: Deployment to AWS (EC2)

### Step 1: Launch EC2 Instance

```bash
# Use Ubuntu 20.04 LTS
# Security group: Allow ports 80, 443, 22
```

### Step 2: Setup Instance

```bash
# Connect to instance
ssh -i key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# Clone repository
git clone your-repo-url /app
cd /app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Create .env file
sudo nano .env  # Add your variables
```

### Step 3: Setup Nginx Reverse Proxy

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/chatbot

# Add this:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable config
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/

# Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

### Step 4: Setup SSL with Let's Encrypt

```bash
# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

### Step 5: Setup Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/nyay-mitra.service

# Add this:
[Unit]
Description=Nyay Mitra Chatbot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/app
ExecStart=/app/venv/bin/gunicorn -c config/gunicorn.conf.py app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable nyay-mitra
sudo systemctl start nyay-mitra

# View logs
sudo systemctl status nyay-mitra
sudo journalctl -u nyay-mitra -f
```

---

## Part 9: Docker Deployment (Optional)

### Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 5000

# Run gunicorn
CMD ["gunicorn", "-c", "config/gunicorn.conf.py", "app:app"]
```

### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  chatbot:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
      - TARGET_ENV=production
    volumes:
      - ./logs:/app/logs
    restart: always
```

### Deploy with Docker

```bash
# Build image
docker build -t nyay-mitra:latest .

# Run container
docker run -d \
  -p 5000:5000 \
  -e GEMINI_API_KEY=your_key \
  -e FLASK_SECRET_KEY=your_secret \
  --name nyay-mitra \
  nyay-mitra:latest

# Check logs
docker logs -f nyay-mitra

# Stop container
docker stop nyay-mitra
```

---

## Part 10: Monitoring & Maintenance

### Setup Error Tracking

```python
# Using Sentry for error monitoring
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1
)
```

### Health Check Endpoint

```python
@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }), 200
```

### Monitor Gemini API

```python
# Log API usage
def track_api_usage(query_length, response_length):
    with open(f"logs/api_usage_{datetime.now().strftime('%Y%m%d')}.log", "a") as f:
        f.write(f"{datetime.now()} | Query: {query_length} | Response: {response_length}\n")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    query = request.json.get("message")
    response = chat_gemini(query)
    track_api_usage(len(query), len(response))
    return jsonify({"reply": response})
```

### Automated Backups

```bash
# Create backup script (backup.sh)
#!/bin/bash
BACKUP_DIR="/backups/nyay-mitra"
mkdir -p $BACKUP_DIR
tar -czf "$BACKUP_DIR/backup-$(date +%Y%m%d).tar.gz" \
  /app/logs \
  /app/data

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

# Add to crontab (backup daily at 2 AM)
# 0 2 * * * /app/backup.sh
```

---

## Part 11: Performance Optimization

### Enable Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route("/api/passages/<query>")
@cache.cached(timeout=3600)
def get_passages(query):
    return retrieve(query)
```

### CDN for Static Files

```html
<!-- Use CDN for common libraries -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-name@1.0.0/styles.css">

<!-- Or self-hosted with caching headers -->
<link rel="stylesheet" href="/static/css/styles.css">
```

### Database Connection Pool

```python
# For future database integration
from sqlalchemy.pool import QueuePool

db = SQLAlchemy(
    session_options={
        "pool_pre_ping": True,
        "poolclass": QueuePool,
        "pool_size": 10,
        "max_overflow": 20,
    }
)
```

---

## Part 12: Security Checklist

```
□ All API keys in environment variables
□ HTTPS enabled in production
□ Rate limiting configured
□ CORS properly scoped to your domains
□ SQL injection prevention (if using DB)
□ XSS protection enabled
□ CSRF tokens in forms
□ Secure cookies configured
□ Input validation on all endpoints
□ Regular security updates
□ Access logs monitored
```

---

## Part 13: Rollback Procedures

### Vercel Rollback
```bash
vercel rollback
vercel ls  # See deployment history
```

### Heroku Rollback
```bash
heroku releases
heroku rollback v123
```

### Git-Based Rollback
```bash
git log --oneline  # Find commit
git revert <commit-hash>
git push
```

### Docker Rollback
```bash
docker pull nyay-mitra:previous-tag
docker stop nyay-mitra
docker run -d --name nyay-mitra nyay-mitra:previous-tag
```

---

## Part 14: Post-Deployment Testing

### Smoke Tests
```bash
curl https://your-domain/health
curl -X POST https://your-domain/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is dharma?"}'
```

### Load Test with Apache Bench
```bash
ab -n 100 -c 10 https://your-domain/
```

### Full Integration Test
```
1. Access homepage
2. Navigate to chatbot
3. Submit Gita query → Check format
4. Submit Chanakya query → Check format  
5. Verify styling matches
6. Test voice input
7. Clear browser data, refresh → Verify new session
```

---

## Part 15: Troubleshooting Deployment

### Issue: "Module not found"
```python
# Solution: Check Python path
import sys
print(sys.path)
# Ensure app.py directory is first
```

### Issue: "Connection refused" on port 5000
```bash
# Solution: Check if process running
lsof -i :5000
# Kill and restart
pkill -f gunicorn
```

### Issue: "Gemini API key invalid"
```bash
# Solution: Verify key in production environment
echo $GEMINI_API_KEY
# Re-set if needed
```

### Issue: "Static files not loading"
```python
# Solution: Verify static folder path
print(app.static_folder)
print(app.static_url_path)
```

### Issue: "High memory usage"
```bash
# Solution: Monitor and restart workers
top -p $(pgrep -f gunicorn)
# Reduce workers in config
```

---

## 📋 Final Deployment Checklist

```
PRE-DEPLOYMENT
□ All code tested locally
□ All dependencies in requirements.txt
□ .env configured (DO NOT commit)
□ .gitignore configured properly
□ All paths are relative or environment-based
□ Data files included

DEPLOYMENT
□ Choose platform (Vercel/Heroku/AWS/Self-hosted)
□ Configure environment variables
□ Deploy code
□ Verify deployment successful
□ Run smoke tests

POST-DEPLOYMENT
□ Monitor error logs
□ Check response times
□ Verify all features working
□ Test voice input
□ Verify styling loads
□ Monitor API usage
□ Set up backups
□ Configure alerts
```

---

**Status:** ✅ **Ready for Production Deployment**

Your chatbot is optimized, styled, and this guide covers all deployment scenarios!
