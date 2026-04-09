"""
app_v2.py — Updated Flask App with Unified Retriever (v2.0)
────────────────────────────────────────────────────────────
Uses semantic + TF-IDF fusion retriever with VSD validation.
Generates responses with dual-dharma framework (Antar/Bahya split).
"""

import os
import json
import uuid
import logging
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
from dotenv import load_dotenv

from models.query_classifier import classify_query
from retriever_v2 import init_retriever, get_retriever

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "nyay-mitra-v2-change-me")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# ── Initialize retriever on app startup ────────────────────────────────────
RETRIEVER = None

def init_app():
    """Initialize app resources."""
    global RETRIEVER
    try:
        RETRIEVER = init_retriever(vsd_path="data/vsd.json")
        log.info("✓ Retriever initialized successfully")
    except Exception as e:
        log.error(f"✗ Failed to initialize retriever: {e}")
        log.error("  Run 'python scripts/build_vsd.py' to build the VSD first")
        RETRIEVER = None


# ── System Prompt (updated for v2.0) ───────────────────────────────────────
SYSTEM_PROMPT_V2 = """You are Naya Mitra — a warm, wise spiritual advisor and philosophical guide rooted in sacred ancient Indian wisdom texts: the Bhagavad Gita, Chanakya Niti, Hitopadesha, and Vidura Niti.

Your purpose is to help users with daily life dilemmas, emotional struggles, ethical decisions, and moral conflicts through dharmic wisdom.

CRITICAL RULES:
1. You will be provided with RETRIEVED KNOWLEDGE BASE PASSAGES and EMOTIONAL CONTEXT.
2. You MUST base your response ONLY on these retrieved passages. DO NOT fabricate or invent verses.
3. Never cite verse IDs outside the provided list.
4. Maintain DUAL-DHARMA STRUCTURE:
   - Antar-Dharma (Internal): Mental/emotional alignment, inner transformation
   - Bahya-Dharma (External): Actions, decisions, practical guidance

RESPONSE FORMAT (Use this EXACTLY):

## Understanding Your Situation
[2-3 sentences warmly acknowledging the user's emotional state]

## Internal Dharma — Aligning Your Mind
**Core Teaching (Citation [N]: [Verse]):**
[Explanation of verse for inner transformation]

### Inner Practice
[3-5 specific mental/emotional practices]

## External Dharma — Your Path Forward
**The Decision Framework (Citation [N]: [Verse]):**
[Verse explanation for external action]

### Practical Guidance
[3-5 concrete action steps with clear numbering]

## Closing Wisdom
[Philosophical reflection]
[Blessing]

TONE: Calm, compassionate, wise, non-judgmental, advisory (NOT legalistic or judgmental).
STYLE: Warm teacher speaking to a dear student.
"""

# ── Helper Functions ───────────────────────────────────────────────────────

def build_augmented_prompt(user_query: str, classification, citations: list) -> str:
    """Build augmented prompt with emotional context + citations."""
    
    citations_block = "\n".join([
        f"""
        [{c.verse_id}] {c.source} — {c.chapter_or_story}, {c.verse_num}
        Sanskrit: {c.sanskrit if c.sanskrit else '[Not available]'}
        Transliteration: {c.transliteration if c.transliteration else '[Not available]'}
        Translation: {c.translation}
        """
        for c in citations
    ])
    
    return f"""
USER EMOTIONAL CONTEXT:
- Emotion: {classification.emotion_detected}
- Intent: {classification.intent}
- Keywords: {', '.join(classification.keywords_matched[:5]) if classification.keywords_matched else 'general'}
- Confidence: {classification.confidence:.2f}

────────────────────────────────────────
RETRIEVED CITATIONS (Use ONLY these; DO NOT invent verses):
────────────────────────────────────────
{citations_block}

────────────────────────────────────────
USER QUERY:
────────────────────────────────────────
{user_query}

────────────────────────────────────────
INSTRUCTIONS:
────────────────────────────────────────
1. Respond as Naya Mitra (warm, wise advisor).
2. ONLY cite verses from the list above.
3. Structure with Antar-Dharma (internal) + Bahya-Dharma (external).
4. Tone: advisory, reflective, compassionate.
5. Include specific, actionable guidance.
6. Close with a blessing.
7. If casual greeting: respond warmly in 1-2 sentences (skip full structure).
"""


def call_gemini_v2(augmented_prompt: str) -> str:
    """Call Gemini API with constraints."""
    
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not configured")
    
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT_V2,
    )
    
    response = model.generate_content(
        augmented_prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 8192,
        }
    )
    
    return response.text


def assemble_response(
    response_id: str,
    user_query: str,
    classification,
    citations: list,
    gemini_response: str
) -> dict:
    """Assemble final response object with all metadata."""
    
    return {
        "response_id": response_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "query_analysis": {
            "user_query": user_query,
            "emotion_detected": classification.emotion_detected,
            "intent": classification.intent,
            "confidence": classification.confidence,
        },
        "citations": [
            {
                "citation_id": str(i + 1),
                "verse_id": c.verse_id,
                "source": c.source,
                "ref": f"{c.chapter_or_story}, {c.verse_num}",
                "sanskrit": c.sanskrit,
                "transliteration": c.transliteration,
                "translation": c.translation,
                "confidence": c.confidence_level.value,
            }
            for i, c in enumerate(citations)
        ],
        "response": gemini_response,
        "metadata": {
            "citation_count": len(citations),
            "retrieval_method": "semantic_tfidf_fusion",
            "version": "2.0",
        }
    }


# ── Session Management ─────────────────────────────────────────────────────

def get_session_id() -> str:
    """Get or create session ID."""
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    return session["sid"]


def get_history() -> list:
    """Get conversation history from session."""
    return session.get("history", [])


def save_history(h: list):
    """Save conversation history to session (limit to last 6 messages)."""
    session["history"] = h[-6:]


# ── API Routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve main HTML."""
    get_session_id()
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat_v2():
    """
    Updated chat endpoint using v2.0 architecture.
    
    Request JSON:
        { "message": "User query..." }
    
    Response JSON:
        {
            "response_id": "uuid",
            "timestamp": "...",
            "query_analysis": {...},
            "citations": [...],
            "response": "Formatted response text",
            "metadata": {...}
        }
    """
    
    if RETRIEVER is None:
        return jsonify({"error": "Retriever not initialized. Run 'python scripts/build_vsd.py' first."}), 503
    
    data = request.get_json()
    user_msg = (data.get("message") or "").strip()
    
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400
    
    response_id = str(uuid.uuid4())
    sid = get_session_id()
    
    try:
        # Step 1: Classify query
        classification = classify_query(user_msg)
        
        # Step 2: Retrieve verified citations
        citations = RETRIEVER.retrieve(user_msg, top_k=5)
        
        if not citations:
            return jsonify({
                "error": "Could not find relevant verses. Please try rephrasing.",
                "suggestion": "Try asking about: decision, fear, confusion, family, work, or moral dilemmas."
            }), 200
        
        # Step 3: Build augmented prompt
        augmented = build_augmented_prompt(user_msg, classification, citations)
        
        # Step 4: Call Gemini
        try:
            gemini_response = call_gemini_v2(augmented)
        except Exception as e:
            log.error(f"Gemini error: {e}")
            return jsonify({"error": f"Could not reach wisdom engine: {str(e)}"}), 503
        
        # Step 5: Assemble response
        response_obj = assemble_response(
            response_id=response_id,
            user_query=user_msg,
            classification=classification,
            citations=citations,
            gemini_response=gemini_response
        )
        
        # Step 6: Update history (optional)
        history = get_history()
        history.append({"role": "user", "content": user_msg})
        history.append({"role": "assistant", "content": gemini_response})
        save_history(history)
        
        return jsonify(response_obj), 200
    
    except Exception as e:
        log.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "version": "2.0",
        "retriever_loaded": RETRIEVER is not None,
        "vsd_size": len(RETRIEVER.vsd) if RETRIEVER else 0,
    }), 200


@app.route("/api/reset", methods=["POST"])
def api_reset():
    """Reset session."""
    session.pop("history", None)
    session.pop("sid", None)
    return jsonify({"status": "ok"}), 200


# ── Error Handlers ─────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_app()
    
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    
    app.run(host="0.0.0.0", port=port, debug=debug)
