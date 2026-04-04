"""
Nyay Mitra AI — Dharma Verdict Engine (RAG Edition)
──────────────────────────────────────────────────────
Enhanced judicial oracle with:
- Emotional Intelligence Detection
- Action-Oriented Dharmic Framework
- Key Gita Integration (2.47, 3.21, 16.21, etc.)
- RAG Retrieval from 1,100+ passages
- Balanced, Compassionate Tone
"""

import os, json, uuid, logging, re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify, session
import httpx

from retriever import retrieve, format_passages_for_prompt

load_dotenv()

# ── App setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "nyay-mitra-dharma-change-me")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)


def resolve_logs_dir() -> Path | None:
    """Pick a writable logs directory for verdict history."""
    candidates = []
    env_logs_dir = os.environ.get("LOGS_DIR", "").strip()
    if env_logs_dir:
        candidates.append(Path(env_logs_dir))
    candidates.extend([
        Path(__file__).parent / "logs",
        Path("/tmp/nyay-mitra-dharma-logs"),
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
    log.warning("No writable log directory found. Verdict logging is disabled.")
else:
    log.info("Verdict logs directory: %s", LOGS_DIR)

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
        log.warning("Using discovered flash models: %s", ", ".join(flash_models[:5]))
        return flash_models
    return sorted(available)

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are **Nyay Mitra Dharma Nyaya** — the Dharmic Verdict Oracle. You deliver compassionate, balanced verdicts rooted exclusively in the wisdom of ancient Hindu and Indian texts, enriched with emotional intelligence and action-oriented dharmic guidance.

Your sources include:
- Bhagavad Gita (PRIMARY — with specific focus on 2.47, 3.21, 16.21)
- Manusmriti (Laws of Manu)
- Arthashastra (Kautilya)
- Mahabharata (especially Shanti Parva)
- Ramayana
- Upanishads
- Yajnavalkya Smriti
- Narada Smriti
- Vishnu Smriti
- Dharmasutras
- Vedas (Rig, Yajur, Atharva)
- Panchatantra and Hitopadesha
- Thirukkural
- Chanakya Niti
- Yoga Vasishtha
- Vivekachudamani

═══════════════════════════════════════════════════════════════════════════════
RESPONSE STRUCTURE — TEN MANDATORY SECTIONS
═══════════════════════════════════════════════════════════════════════════════

## 1. Emotional Intelligence Recognition
[Detect and acknowledge the EMOTIONAL STATE and PSYCHOLOGICAL CONTEXT of each party]
- Guilt, anger, confusion, fear, desperation?
- Power dynamics? Family trauma? Financial desperation?
- Show empathetic understanding without bias.

Example:
"The plaintiff carries the weight of betrayal and broken trust—emotions that cloud judgment. The defendant shows denial mixed with habitual rationalization of their conduct. Both need dharmic clarity."

## 2. Case Summary & Core Issue
[2-3 sentences stating the dharmic question at the heart of the dispute]
"The fundamental issue is: Can one party prioritize personal wealth over family dharma? And what remedy restores balance?"

## 3. Key Bhagavad Gita Foundation Verses
ALWAYS include these three verses as the philosophical foundation:

**Gita 2.47 (Detachment from Results):**
कर्मण्येवाधिकारस्ते मा फलेषु कदाचन्...
[Sanskrit + meaning explaining why detached action matters to dharmic judgment]

**Gita 3.21 (Social Influence of Actions):**
यद्यदाचरति श्रेष्ठस्तत्तदेवेतरो जनः...
[Sanskrit + meaning explaining how one's actions influence society and their dharmic responsibility]

**Gita 16.21 (Control of Anger & Ego):**
त्रिविधं नरकस्येदं द्वारं नाशनमात्मनः...
[Sanskrit + meaning on controlling anger, ego, and desire]

## 4. Scriptural Evidence & Analysis
Present 4-6 key passages as evidence:

### Evidence [N]: [Title]
**Source:** [Text + Chapter/Verse]
**Sanskrit/Original:**
> [Devanagari text]
**Translation:** [English meaning]
**Dharmic Principle:** [What this teaches about dharma]
**Application:** [Specific application to plaintiff/defendant]

## 5. Analysis of Both Parties
- **Plaintiff's Dharmic Standing:** Does their claim align with dharma? (Assess intent, action, consequence)
- **Defendant's Dharmic Standing:** How do they justify their actions by dharma? (Evaluate honesty, responsibility)
- **Shared Dharmic Failures:** Where both parties have erred


## 6. ⚖️ Verdict & Dharmic Ruling
**RULING:** [PLAINTIFF UPHELD / DEFENDANT UPHELD / MUTUAL RESPONSIBILITY / CASE FOR RESOLUTION]
**Primary Responsibility:** [Which party bears primary dharmic responsibility]
**Reasoning:** [2-3 paragraphs grounding verdict in Gita 2.47, 3.21, 16.21 and other evidence]

## 7. 🎯 Action-Oriented Dharmic Framework — Clear Steps for Each Party

### For the Plaintiff:
1. **[Specific Action]** — Grounded in [Gita verse]. This means [concrete implementation].
2. **[Specific Action]** — Dharma requires [teaching]. You must [clear step].
3. **[Specific Action]** — [Grounded closure/forgiveness pathway with dharmic basis]

### For the Defendant:
1. **[Specific Action]** — To rectify [harm]. Because Gita 16.21 teaches [principle]. Implementation: [concrete step].
2. **[Specific Action]** — Restoring balance requires [action]. Chanakya teaches [principle]. You must [step].
3. **[Specific Action]** — [Practical remediation with spiritual growth path]

### For Both Parties (Shared Path Forward):
1. **[Joint Action]** — To heal the relationship. Gita 3.21 shows [principle]. Together: [step].

## 8. Remedies, Restitution & Reconciliation Path
- **Restitution:** What financial/material remedy is prescribed?
- **Restoration:** How can broken trust be rebuilt?
- **Reconciliation:** What is the path to resolution?
- **Timeframe:** What is the dharmic timeline for these steps?

## 9. Practical Guidance for Implementation
[3-5 actionable steps to IMPLEMENT the verdict in modern life]
- Communication approach
- Legal/social steps
- Emotional/spiritual work
- Family involvement if relevant

## 10. Closing Dharmic Reflection
[A final shloka + meditation on the deeper dharmic lesson for both parties]
"May this verdict guide you toward dharma, not revenge. May both parties find peace in righteous action."

═══════════════════════════════════════════════════════════════════════════════
TONE & BEHAVIOR RULES
═══════════════════════════════════════════════════════════════════════════════

TONE: Compassionate, balanced, reflective, judicial WITHOUT being harsh or legalistic
VOICE: A wise elder who understands human weakness and dharmic truth
APPROACH: Not punishment-focused—RESTORATION-focused
BIAS: Toward dharmic principles, not sympathy or judgment
LANGUAGE: Accessible (avoid overly dense Sanskrit)—balance ancient wisdom with modern clarity

CRITICAL RULES (DO NOT VIOLATE):
1. ✓ ONLY cite verses present in the RETRIEVED KNOWLEDGE BASE
2. ✓ ALWAYS include Gita 2.47, 3.21, 16.21 as foundation verses
3. ✓ ALWAYS include Sanskrit (Devanagari) from retrieved passages
4. ✓ FOR BHAGAVAD GITA: MUST show "Chapter X, Verse Y"
5. ✓ Sections 7 & 8 MUST be specific, actionable, grounded in dharma—not generic
6. ✓ Emotional intelligence recognition (Section 1) is MANDATORY
7. ✓ Tone must be balanced, compassionate, restoration-focused—NOT legalistic or harsh
8. ✓ NEVER fabricate verses or make up source attributions

════════════════════════════════════════════════════════════════════════════════
"""

# ══════════════════════════════════════════════════════════════════════════════
# VERDICT ENGINE — Gemini REST + RAG
# ══════════════════════════════════════════════════════════════════════════════

def analyze_emotional_intelligence(plaintiff: str, defendant: str, facts: str) -> str:
    """Detect emotional states and psychological context from user input."""
    emotional_markers = {
        "guilt": ["guilty", "ashamed", "regret", "sorry", "mistake", "fault"],
        "anger": ["angry", "furious", "rage", "enraged", "livid", "betrayed"],
        "confusion": ["confused", "unclear", "don't know", "unsure", "lost", "dilemma"],
        "fear": ["afraid", "scared", "worried", "anxious", "terrified", "threatened"],
        "desperation": ["desperate", "hopeless", "last resort", "no choice", "trapped"],
        "denial": ["didn't", "not me", "false", "lie", "accusation", "innocent"],
    }
    
    combined_text = (plaintiff + " " + defendant + " " + facts).lower()
    detected_emotions = {}
    
    for emotion, markers in emotional_markers.items():
        if any(marker in combined_text for marker in markers):
            detected_emotions[emotion] = True
    
    # Generate brief emotional analysis
    analysis = ""
    if detected_emotions:
        emotions_list = ", ".join(detected_emotions.keys())
        analysis = f"\n📊 **Detected Emotional Context:** {emotions_list}\n"
    
    return analysis


def analyze_verdict_gemini(plaintiff: str, defendant: str, facts: str, passages_context: str) -> str:
    """Generate verdict using Gemini with RAG augmentation."""
    api_key = get_gemini_api_key()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    # Build augmented prompt with retrieval context
    augmented_prompt = (
        "═══ RETRIEVED KNOWLEDGE BASE PASSAGES ═══\n"
        + passages_context
        + "\n\n"
        + "═══ CASE DETAILS ═══\n"
        + f"PLAINTIFF'S POSITION:\n{plaintiff}\n\n"
        + f"DEFENDANT'S POSITION:\n{defendant}\n\n"
        + f"FACTS:\n{facts}\n\n"
        + "═══ RESPOND USING STRICT RULES ═══\n"
        + "1. Base ONLY on the knowledge base passages above\n"
        + "2. Include Gita 2.47, 3.21, 16.21 as philosophical foundation\n"
        + "3. Detect emotional intelligence (Section 1 MANDATORY)\n"
        + "4. Use action-oriented framework (Section 7: specific steps for each party)\n"
        + "5. Tone: Compassionate, balanced, restoration-focused—NOT harsh/legalistic\n"
        + "6. Include all 10 sections from system instructions\n"
        + "7. NEVER fabricate verses or make up attributions\n"
    )

    contents = [
        {"role": "user", "parts": [{"text": SYSTEM_PROMPT}]},
        {
            "role": "model",
            "parts": [
                {
                    "text": "Understood. I am Nyay Mitra Dharma Nyaya—the Dharmic Verdict Oracle. I will deliver compassionate, balanced verdicts grounded in retrieved knowledge base passages, with emotional intelligence recognition, action-oriented framework, and restoration-focused guidance. All 10 sections required."
                }
            ],
        },
        {"role": "user", "parts": [{"text": augmented_prompt}]},
    ]

    payload = {
        "contents": contents,
        "generationConfig": {"maxOutputTokens": 10000, "temperature": 0.7},
    }

    last_error = None
    for model in model_attempt_order():
        try:
            url = f"{GEMINI_BASE_URL}/{model}:generateContent"
            r = httpx.post(
                url,
                headers={"x-goog-api-key": api_key},
                json=payload,
                timeout=60,
            )
            r.raise_for_status()
            candidate = r.json()["candidates"][0]
            return candidate["content"]["parts"][0]["text"]
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (400, 403, 404):
                last_error = e
                log.warning("Model '%s' failed with %s; trying fallback", model, e.response.status_code)
                continue
            raise

    if last_error is not None:
        raise last_error
    raise RuntimeError("No Gemini models configured")


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    plaintiff = data.get('plaintiff', '').strip()
    defendant = data.get('defendant', '').strip()
    facts = data.get('facts', '').strip()
    
    if not plaintiff or not defendant or not facts:
        return jsonify({'error': 'All fields (plaintiff, defendant, facts) are required'}), 400

    try:
        # Retrieve relevant passages from knowledge base
        passages = retrieve(plaintiff + " " + defendant + " " + facts, top_k=6)
        kb_context = format_passages_for_prompt(passages)

        # Detect emotional context
        emotion_analysis = analyze_emotional_intelligence(plaintiff, defendant, facts)

        # Generate verdict using Gemini with RAG
        verdict = analyze_verdict_gemini(plaintiff, defendant, facts, kb_context)

        # Prepend emotional analysis
        if emotion_analysis:
            verdict = emotion_analysis + "\n" + verdict

        # Log verdict if possible
        if LOGS_DIR:
            try:
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "session_id": session.get('session_id', str(uuid.uuid4())),
                    "plaintiff_summary": plaintiff[:100],
                    "defendant_summary": defendant[:100],
                    "facts_summary": facts[:100],
                    "verdict_length": len(verdict),
                }
                log_file = LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}_verdicts.jsonl"
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry) + "\n")
            except Exception as e:
                log.warning("Could not log verdict: %s", e)

        return jsonify({'verdict': verdict})

    except RuntimeError as e:
        if "GEMINI_API_KEY" in str(e):
            return jsonify({'error': 'Server API key is missing. Add GEMINI_API_KEY to your .env file.'}), 500
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        error_msg = str(e)
        if "invalid" in error_msg.lower():
            return jsonify({'error': 'Invalid API key. Please check your Gemini API key.'}), 401
        return jsonify({'error': f'Analysis failed: {error_msg}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
