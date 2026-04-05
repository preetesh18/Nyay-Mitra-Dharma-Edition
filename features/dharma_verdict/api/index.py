"""
Vercel serverless entry point for Nyay Mitra Dharma Verdict
This file exports the Flask app for Vercel to run as a serverless function.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import app
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app import app

# Vercel expects a WSGI app at module level named 'app'
# Our Flask app is already named 'app' in app.py
# Just re-export it for Vercel
__all__ = ['app']
