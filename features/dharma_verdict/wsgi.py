"""
WSGI entrypoint for Nyay Mitra Dharma Verdict
This file can be used by both traditional WSGI servers and Vercel
"""

from app import app

if __name__ == "__main__":
    app.run(debug=False)
