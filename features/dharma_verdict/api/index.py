"""
api/index.py — Entry point for Vercel serverless functions
Imports and serves the Flask app for Nyay Mitra Dharma Verdict Engine
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

# Vercel serverless function
handler = app.asgi  # Using ASGI format for Vercel
