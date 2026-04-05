"""
Vercel serverless entry point for Nyay Mitra Dharma Verdict
This file exports the Flask app for Vercel to run as a serverless function.
"""

import sys
import os
from pathlib import Path

# Ensure parent directory is in path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

try:
    from app import app
    print("✅ Successfully imported Flask app", flush=True)
except ImportError as e:
    print(f"❌ Failed to import app: {e}", flush=True)
    raise

# Vercel expects a WSGI app at module level named 'app'
if not hasattr(app, '__call__'):
    raise RuntimeError("Flask app is not callable - check app.py exports")

__all__ = ['app']
