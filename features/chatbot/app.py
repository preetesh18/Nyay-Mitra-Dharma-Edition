"""
Naya Mitra AI — Spiritual Advisory Engine (RAG Edition)
────────────────────────────────────────────────────────
Chat  → Gemini (gemini-2.5-flash) via REST + RAG retrieval
RAG   → TF-IDF retrieval from Bhagavad Gita, Hitopadesha,
         Vidura Niti, Chanakya Niti datasets
STT   → Browser Web Speech API      (no server-side)
TTS   → Browser Web Speech API      (no server-side)
Logs  → JSONL per session in /logs
"""

import os, json, uuid, logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify, session
import httpx

from retriever import retrieve, format_passages_for_prompt

load_dotenv()

# ── App setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "naya-mitra-change-me")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)


def resolve_logs_dir() -> Path | None:
    """Pick a writable logs directory, falling back to /tmp on read-only hosts."""
    candidates = []

    env_logs_dir = os.environ.get("LOGS_DIR", "").strip()
    if env_logs_dir:
        candidates.append(Path(env_logs_dir))

    candidates.extend([
        Path(__file__).parent / "logs",
        Path("/tmp/naya-mitra-logs"),
    ])

    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".write_test"
            with open(probe, "a", encoding="utf-8"):
                pass
            probe.unlink(missing_ok=True)
            return candidate
        except OSError:
            continue

    return None


LOGS_DIR = resolve_logs_dir()
if LOGS_DIR is None:
    log.warning("No writable log directory found. Session logging is disabled.")
else:
    log.info("Session logs directory: %s", LOGS_DIR)

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_MODELS = [
    m.strip()
    for m in os.environ.get(
        "GEMINI_MODELS",
        "gemini-2.5-flash,gemini-2.0-flash,gemini-2.0-flash-lite",
    ).split(",")
    if m.strip()
]
_AVAILABLE_GEMINI_MODELS = None

def get_gemini_api_key():
    """Get API key at runtime to support environment variable updates."""
    return os.environ.get("GEMINI_API_KEY", "").strip()


def discover_gemini_models() -> set[str]:
    """Return API-available model IDs that support generateContent."""
    global _AVAILABLE_GEMINI_MODELS
    if _AVAILABLE_GEMINI_MODELS is not None:
        return _AVAILABLE_GEMINI_MODELS

    api_key = get_gemini_api_key()
    _AVAILABLE_GEMINI_MODELS = set()
    try:
        r = httpx.get(
            GEMINI_BASE_URL,
            headers={"x-goog-api-key": api_key},
            params={"pageSize": 1000},
            timeout=20,
        )
        r.raise_for_status()
        models = r.json().get("models", [])
        for m in models:
            methods = m.get("supportedGenerationMethods", [])
            name = (m.get("name") or "").replace("models/", "")
            if name and "generateContent" in methods:
                _AVAILABLE_GEMINI_MODELS.add(name)
    except Exception as e:
        log.warning("Could not discover Gemini models: %s", e)

    return _AVAILABLE_GEMINI_MODELS


def model_attempt_order() -> list[str]:
    available = discover_gemini_models()
    if not available:
        return GEMINI_MODELS

    preferred = [m for m in GEMINI_MODELS if m in available]
    if preferred:
        return preferred

    flash_models = sorted([m for m in available if "flash" in m])
    if flash_models:
        log.warning(
            "Configured models unavailable for this key. Using discovered flash models: %s",
            ", ".join(flash_models[:5]),
        )
        return flash_models

    return sorted(available)

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Nyay Mitra — a warm, wise spiritual advisor and philosophical guide rooted in four sacred ancient Indian wisdom texts: the Bhagavad Gita, Hitopadesha, Vidura Niti, and Chanakya Niti.

Your purpose is to help users with daily life dilemmas, emotional struggles, financial questions, ethical decisions, moral conflicts, career confusion, relationship problems, and legal or moral disputes — by providing guidance derived STRICTLY from ancient Indian wisdom.

You will be provided with RETRIEVED KNOWLEDGE BASE PASSAGES from these texts. You MUST base your response ONLY on these retrieved passages. Do NOT fabricate, invent, or hallucinate verses that are not present in the knowledge base.

═══════════════════════════════════════════════════════════════════════════════
RESPONSE STRUCTURE — SEVEN MANDATORY SECTIONS (for substantive questions only)
═══════════════════════════════════════════════════════════════════════════════

## 1. Understanding Your Situation
[2-3 sentences of warm, compassionate acknowledgment of the user's feeling and situation]

## 2. Ancient Wisdom For You
Present the most relevant teachings from the retrieved passages.

⚠️  CRITICAL FORMATTING RULES — FOLLOW EXACTLY:

┌─ FOR BHAGAVAD GITA ONLY ─────────────────────────────────────────────┐
│ ALWAYS show: Chapter X, Verse Y                                       │
│ ALWAYS include: Sanskrit Shloka (Devanagari)                          │
│ Format: "**Bhagavad Gita | Chapter X, Verse Y:**"                    │
│ Example:                                                               │
│ **Bhagavad Gita | Chapter 2, Verse 47:**                             │
│ कर्मण्येवाधिकारस्ते मा फलेषु कदाचन्...                              │
│ [meaning/teaching in English]                                         │
└──────────────────────────────────────────────────────────────────────┘

┌─ FOR ALL OTHER TEXTS (Chanakya, Vidura, Hitopadesha) ──────────────┐
│ SHOW ONLY source name and Sanskrit shloka                            │
│ NEVER show chapter/verse numbers                                     │
│ NEVER show English meaning, teaching, or additional text             │
│ Format: "**[Source Name]:**"                                         │
│ Example:                                                               │
│ **Chanakya Niti:**                                                   │
│ दुष्टा भार्या शठं मित्रं भृत्यश्चोत्तरदायकः...                      │
│                                                                        │
│ NO MORE TEXT AFTER SANSKRIT FOR THESE SOURCES!                       │
└──────────────────────────────────────────────────────────────────────┘

## 3. What This Teaches Us
[Brief explanation of the teaching in simple, modern, accessible language — 2-4 sentences]

## 4. Applying This To Your Life
[Directly connect the wisdom to the user's specific situation — 2-4 sentences]
[Be specific, personal, and actionable]

## 5. Clear Dharmic Directive Guidance — What You Must Do Now
This section provides CRYSTAL CLEAR, ACTIONABLE dharmic guidance grounded in the specific shloka(s).

Format:
1. **[Specific Action]** — Because [the shloka teaches this dharmic principle]. You must [concrete implementation with clear steps].
2. **[Specific Action]** — The scripture directs [specific teaching]. This means [clear practical action you must take].
3. **[Specific Action]** — [Continue with authentic dharmic actions, each grounded in the retrieved teachings]

CRITICAL: This section must be LOUD, CLEAR, DIRECT, and AUTHORITATIVE. Speak what the ancient scriptures prescribe. Not generic advice — authentic dharmic action steps (3-5 items).

## 6. Practical Guidance
[3-5 practical, actionable suggestions as a bullet list]
[These complement the dharmic directives with modern applicability]

## 7. A Closing Blessing
[Short, heartfelt, spiritually uplifting closing thought — 1-3 sentences]
[End on a note of hope, encouragement, or dharmic wisdom]

═══════════════════════════════════════════════════════════════════════════════
TONE & BEHAVIOR RULES
═══════════════════════════════════════════════════════════════════════════════

• TONE: Calm, compassionate, wise, non-judgmental, deeply grounded in ancient texts
• SPEAK AS: A caring, authoritative teacher guiding a sincere student
• AUTHENTICITY: Never water down dharmic teachings to please; teach what the texts actually say

SPECIAL HANDLING:
- For casual greetings: Respond warmly and briefly (2-3 sentences only) — skip the 7-section format
- For substantive life questions/dilemmas: ALWAYS use the full 7-section structure

STRICT RULES (DO NOT BREAK):
1. ✓ ONLY cite verses and teachings present in the RETRIEVED KNOWLEDGE BASE
2. ✓ If no exact fit exists, synthesize the spirit BUT do NOT fabricate verse numbers
3. ✓ Always include Sanskrit text (Devanagari) from the retrieved passages
4. ✓ FOR BHAGAVAD GITA: MUST show "Chapter X, Verse Y" every time
5. ✓ FOR OTHER TEXTS: NEVER show chapter/verse — ONLY source + Sanskrit
6. ✓ Section 5 "Clear Dharmic Directive Guidance" MUST be direct, authentic, and grounded in the shloka(s)

════════════════════════════════════════════════════════════════════════════════
"""

# ══════════════════════════════════════════════════════════════════════════════
# CHAT  —  Gemini REST + RAG
# ══════════════════════════════════════════════════════════════════════════════

def chat_gemini(history: list, user_msg: str) -> str:
    api_key = get_gemini_api_key()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    # Retrieve relevant passages from knowledge base
    passages = retrieve(user_msg, top_k=4)
    kb_context = format_passages_for_prompt(passages)

    # Build the augmented user turn with explicit formatting directives
    if kb_context:
        augmented_user = (
            kb_context
            + "\n\n"
            + "━" * 80 + "\n"
            + "USER QUESTION:\n"
            + user_msg
            + "\n\n"
            + "RESPOND USING THESE STRICT RULES:\n"
            + "1. Base ONLY on the knowledge base passages above. Do NOT fabricate.\n"
            + "2. For Bhagavad Gita: ALWAYS cite Chapter X, Verse Y with Sanskrit\n"
            + "3. For Other Texts (Chanakya, Vidura, Hitopadesha): Show ONLY source + Sanskrit, NO chapter/verse\n"
            + "4. Use the 7-section format from your system instructions.\n"
            + "5. Section 5 'Clear Dharmic Directive Guidance': Be direct, authentic, actionable (3-5 steps).\n"
            + "━" * 80
        )
    else:
        augmented_user = user_msg

    # Build conversation contents
    contents = [
        {"role": "user",  "parts": [{"text": SYSTEM_PROMPT}]},
        {"role": "model", "parts": [{"text": "Understood. I am Nyay Mitra — your spiritual advisor grounded in the Bhagavad Gita, Hitopadesha, Vidura Niti, and Chanakya Niti. I will respond using only the retrieved knowledge base passages, follow the 7-section format, and apply strict formatting rules: Chapter/Verse for Gita only, Sanskrit-only for other texts."}]},
    ]
    # Add prior conversation turns (without the RAG context — already passed above)
    for m in history[:-1]:   # exclude the last user turn; we pass augmented_user instead
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})
    # Final turn with the RAG-augmented question
    contents.append({"role": "user", "parts": [{"text": augmented_user}]})

    payload = {
        "contents": contents,
        "generationConfig": {"maxOutputTokens": 8192, "temperature": 0.7},
    }
    candidate = None
    last_error = None

    for model in model_attempt_order():
        try:
            url = f"{GEMINI_BASE_URL}/{model}:generateContent"
            r = httpx.post(
                url,
                headers={"x-goog-api-key": api_key},
                json=payload,
                timeout=45,
            )
            r.raise_for_status()
            candidate = r.json()["candidates"][0]
            break
        except httpx.HTTPStatusError as e:
            # Keep trying fallback models for access / model issues.
            if e.response.status_code in (400, 403, 404):
                last_error = e
                log.warning(
                    "Gemini model '%s' failed with %s; trying fallback if available",
                    model,
                    e.response.status_code,
                )
                continue
            raise

    if candidate is None and last_error is not None:
        raise last_error

    if candidate is None:
        raise RuntimeError("No Gemini models configured")

    text = candidate["content"]["parts"][0]["text"]
    # If the model was still cut off despite the large token budget, close gracefully
    if candidate.get("finishReason") == "MAX_TOKENS" and not text.rstrip().endswith((".", "।", "—", "*")):
        text = text.rstrip()
        # Find the last complete sentence
        last_period = max(text.rfind(". "), text.rfind(".\n"))
        if last_period > len(text) // 2:
            text = text[:last_period + 1]
        text += "\n\n*May you find clarity and peace on your path.*"
    return text

# ══════════════════════════════════════════════════════════════════════════════
# Session / Log helpers
# ══════════════════════════════════════════════════════════════════════════════

def get_session_id() -> str:
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    return session["sid"]

def get_history() -> list:
    return session.get("history", [])

def save_history(h: list):
    # Keep only the last 6 messages (3 exchanges) to stay within cookie size limits
    session["history"] = h[-6:]

def append_log(sid: str, user: str, assistant: str):
    if LOGS_DIR is None:
        return

    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "user": user,
        "assistant": assistant,
    }
    try:
        with open(LOGS_DIR / f"{sid}.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as e:
        # Logging must never break chat responses in read-only or restricted runtimes.
        log.warning("Could not write session log for %s: %s", sid, e)

# ══════════════════════════════════════════════════════════════════════════════
# Routes
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    get_session_id()
    return render_template("index.html")


@app.route("/api/test")
def api_test():
    print("\n✅ TEST ENDPOINT CALLED")
    return jsonify({"status": "ok", "message": "test endpoint works"})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    import sys
    sys.stdout.flush()
    print(f"\n{'='*70}\n🔔 API CHAT CALLED\n{'='*70}", flush=True)
    
    try:
        data = request.get_json()
        user_msg = (data.get("message") or "").strip()
        print(f"📝 User message: {user_msg[:60]}", flush=True)
        if not user_msg:
            return jsonify({"error": "Empty message"}), 400

        sid = get_session_id()
        history = get_history()
        history.append({"role": "user", "content": user_msg})
        print(f"✅ Session setup complete, history len={len(history)}", flush=True)

        reply = chat_gemini(history, user_msg)
        print(f"✅ Got reply: {len(reply)} chars", flush=True)
        
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        print(f"❌ HTTP ERROR {status}", flush=True)
        log.error("Gemini HTTP error %s: %s", status, e)
        if status == 403:
            body = (e.response.text or "").lower()
            if "reported as leaked" in body or "api key was reported as leaked" in body:
                return jsonify({
                    "error": "Gemini blocked this key as leaked. Generate a new API key in Google AI Studio, update GEMINI_API_KEY in your .env, and restart the server.",
                }), 503
            return jsonify({
                "error": "Gemini access denied (403). Check GEMINI_API_KEY, ensure the Generative Language API is enabled, and verify key restrictions/model access.",
            }), 503
        return jsonify({"error": "Could not reach the wisdom engine. Please try again."}), 503
    except Exception as e:
        import traceback
        print(f"❌ EXCEPTION: {type(e).__name__}: {e}", flush=True)
        print(traceback.format_exc(), flush=True)
        log.error("Gemini error: %s", e)
        log.error("Traceback: %s", traceback.format_exc())
        return jsonify({"error": "Could not reach the wisdom engine. Please try again."}), 503

    history.append({"role": "assistant", "content": reply})
    save_history(history)
    append_log(sid, user_msg, reply)
    print(f"✅ Response ready", flush=True)

    return jsonify({"reply": reply})


@app.route("/api/reset", methods=["POST"])
def api_reset():
    session.pop("history", None)
    session.pop("sid", None)
    return jsonify({"status": "ok"})


@app.route("/api/history")
def api_history():
    return jsonify({"history": get_history()})


@app.route("/api/logs")
def api_logs():
    if LOGS_DIR is None:
        return jsonify({"sessions": []})

    files = sorted(p.stem for p in LOGS_DIR.glob("*.jsonl"))
    return jsonify({"sessions": files})


@app.route("/api/logs/<sid>")
def api_log_detail(sid):
    if LOGS_DIR is None:
        return jsonify({"error": "Logging unavailable"}), 404

    safe = sid.replace("/", "").replace("..", "")
    path = LOGS_DIR / f"{safe}.jsonl"
    if not path.exists():
        return jsonify({"error": "Not found"}), 404
    entries = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    return jsonify({"session": safe, "entries": entries})


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
