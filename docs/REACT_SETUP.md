# React Nyay Mitra - Complete Setup Guide

## Quick Start

### 1. Create React App

```bash
cd "d:\Nyay-Mitra-Dharma Edition"

# Create React app with Vite (faster than CRA)
npm create vite@latest frontend -- --template react

cd frontend

# Install dependencies
npm install
npm install axios react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 2. Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatBot/
│   │   │   ├── ChatBot.jsx
│   │   │   ├── ChatBot.module.css
│   │   │   ├── MessageBubble.jsx
│   │   │   └── SuggestionButtons.jsx
│   │   ├── DharmaVerdict/
│   │   │   ├── DharmaVerdict.jsx
│   │   │   ├── VerdictForm.jsx
│   │   │   ├── VerdictDisplay.jsx
│   │   │   └── VerdictDisplay.module.css
│   │   ├── Navigation.jsx
│   │   └── Header.jsx
│   ├── services/
│   │   ├── chatApi.js
│   │   └── verdictApi.js
│   ├── pages/
│   │   ├── ChatPage.jsx
│   │   ├── VerdictPage.jsx
│   │   └── HomePage.jsx
│   ├── styles/
│   │   ├── globals.css
│   │   ├── theme.css
│   │   └── animations.css
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
├── index.html
├── package.json
├── vite.config.js
├── postcss.config.js
├── tailwind.config.js
└── .env
```

### 3. Environment Setup

Create `frontend/.env`:
```env
VITE_CHATBOT_API=http://127.0.0.1:5000
VITE_VERDICT_API=http://127.0.0.1:5001
```

### 4. Update Tailwind Config

`frontend/tailwind.config.js`:
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          50: '#faf8f3',
          100: '#f0d483',
          200: '#e8c469',
          300: '#d4a017',
          400: '#c9a84c',
          500: '#b8961e',
          600: '#7a6230',
        },
        saffron: {
          50: '#fff7f0',
          100: '#ffe8d6',
          300: '#ff9933',
          500: '#e8831a',
          600: '#c85a00',
        },
        cream: '#f5e8ca',
        ink: '#080604',
      },
      fontFamily: {
        serif: ['EB Garamond', 'Georgia', 'serif'],
        decorative: ['Cinzel Decorative', 'serif'],
        cinzel: ['Cinzel', 'serif'],
      },
    },
  },
  plugins: [],
}
```

### 5. Global CSS

`frontend/src/styles/globals.css`:
```css
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cinzel:wght@400;500;600;700&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Noto+Serif+Devanagari:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --gold: #D4A017;
  --gold-light: #F0C040;
  --saffron: #E8751A;
  --ink: #0D0805;
  --cream: #F5EDD8;
}

body {
  font-family: 'EB Garamond', Georgia, serif;
  background: var(--ink);
  color: var(--cream);
  line-height: 1.6;
}

html {
  scroll-behavior: smooth;
}
```

---

## React Components

### `src/services/chatApi.js`

```javascript
import axios from 'axios';

const API_BASE = import.meta.env.VITE_CHATBOT_API;

const chatApi = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const testConnection = async () => {
  try {
    const res = await chatApi.get('/api/health');
    return res.data;
  } catch (err) {
    console.error('Health check failed:', err.message);
    throw err;
  }
};

export const testGeminiAPI = async () => {
  try {
    const res = await chatApi.post('/api/test-gemini');
    return res.data;
  } catch (err) {
    throw err.response?.data || { error: err.message };
  }
};

export const sendMessage = async (message, sessionId = null) => {
  try {
    const res = await chatApi.post('/api/chat', {
      message,
      session_id: sessionId,
    });
    return res.data;
  } catch (err) {
    throw err.response?.data || { error: err.message };
  }
};

export const createSession = async () => {
  try {
    const res = await chatApi.post('/api/session');
    return res.data;
  } catch (err) {
    throw err.response?.data || { error: err.message };
  }
};

export const getSessionHistory = async (sessionId) => {
  try {
    const res = await chatApi.get(`/api/session/${sessionId}`);
    return res.data;
  } catch (err) {
    throw err.response?.data || { error: err.message };
  }
};

export const resetSession = async (sessionId) => {
  try {
    const res = await chatApi.post('/api/reset', { session_id: sessionId });
    return res.data;
  } catch (err) {
    throw err.response?.data || { error: err.message };
  }
};
```

### `src/services/verdictApi.js`

```javascript
import axios from 'axios';

const API_BASE = import.meta.env.VITE_VERDICT_API;

const verdictApi = axios.create({
  baseURL: API_BASE,
  timeout: 45000,
});

export const testConnection = async () => {
  try {
    const res = await verdictApi.get('/api/health');
    return res.data;
  } catch (err) {
    console.error('Health check failed:', err.message);
    throw err;
  }
};

export const testGeminiAPI = async () => {
  try {
    const res = await verdictApi.post('/api/test-gemini');
    return res.data;
  } catch (err) {
    throw err.response?.data || { error: err.message };
  }
};

export const analyzeCase = async (plaintiff, defendant, facts) => {
  try {
    const res = await verdictApi.post('/api/analyze', {
      plaintiff,
      defendant,
      facts,
    });
    return res.data;
  } catch (err) {
    throw err.response?.data || { error: err.message };
  }
};
```

### `src/components/ChatBot/ChatBot.jsx`

```javascript
import { useState, useEffect, useRef } from 'react';
import { sendMessage, createSession, testConnection } from '../../services/chatApi';
import MessageBubble from './MessageBubble';
import SuggestionButtons from './SuggestionButtons';
import styles from './ChatBot.module.css';

export default function ChatBot() {
  const [messages, setMessages] = useState([
    {
      id: 'init',
      role: 'assistant',
      content: '🙏 Namaste, dear seeker. I am Naya Mitra — your companion on the path of dharma. Share what weighs upon your heart.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [apiReady, setApiReady] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const initSession = async () => {
      try {
        const health = await testConnection();
        setApiReady(true);
        const session = await createSession();
        setSessionId(session.session_id);
      } catch (err) {
        console.error('Failed to initialize:', err);
        setError('Could not connect to server. Using demo mode.');
      }
    };
    initSession();
  }, []);

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    const userMsg = { id: Date.now(), role: 'user', content: text };
    setMessages(prev => [...prev, userMsg, { id: Date.now() + 1, role: 'assistant', content: '⏳ Consulting the ancient wisdom...', loading: true }]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const data = await sendMessage(text, sessionId);
      setMessages(prev => [
        ...prev.slice(0, -1),
        { id: Date.now() + 2, role: 'assistant', content: data.reply },
      ]);
    } catch (err) {
      console.error('Error:', err);
      setError(err.error || 'Failed to get response');
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(input);
    }
  };

  return (
    <div className={styles.chatContainer}>
      {error && <div className={styles.errorBanner}>{error}</div>}
      
      <div className={styles.header}>
        <h1>🪷 Naya Mitra</h1>
        <p>Dharma Upadeshak · Spiritual Wisdom</p>
      </div>

      <div className={styles.messagesBox}>
        {messages.map(msg => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {messages.length === 1 && (
        <SuggestionButtons onSelect={handleSendMessage} />
      )}

      <div className={styles.inputBox}>
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Share what weighs upon your heart…"
          disabled={loading}
          rows={1}
        />
        <button
          onClick={() => handleSendMessage(input)}
          disabled={loading || !input.trim()}
          className={styles.sendBtn}
        >
          🪷
        </button>
      </div>
    </div>
  );
}
```

### `src/components/DharmaVerdict/DharmaVerdict.jsx`

```javascript
import { useState } from 'react';
import { analyzeCase, testConnection } from '../../services/verdictApi';
import VerdictForm from './VerdictForm';
import VerdictDisplay from './VerdictDisplay';
import styles from './DharmaVerdict.module.css';

export default function DharmaVerdict() {
  const [verdict, setVerdict] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (plaintiff, defendant, facts) => {
    setLoading(true);
    setError(null);

    try {
      const data = await analyzeCase(plaintiff, defendant, facts);
      setVerdict(data.verdict);
    } catch (err) {
      setError(err.error || 'Failed to analyze case');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>⚖️ Nyay Mitra Dharma Nyaya</h1>
        <p>न्याय मित्र धर्म न्याय</p>
        <p>The Oracle of Compassionate Dharmic Justice</p>
      </div>

      {error && <div className={styles.error}>{error}</div>}

      {!verdict ? (
        <VerdictForm onSubmit={handleSubmit} loading={loading} />
      ) : (
        <VerdictDisplay verdict={verdict} onNewCase={() => setVerdict(null)} />
      )}
    </div>
  );
}
```

### `src/App.jsx`

```javascript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import ChatPage from './pages/ChatPage';
import VerdictPage from './pages/VerdictPage';
import HomePage from './pages/HomePage';
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/verdict" element={<VerdictPage />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

## Running the Complete Setup

### Terminal 1: Chatbot Backend
```bash
cd features/chatbot
python app.py
```

### Terminal 2: Dharma Verdict Backend
```bash
cd features/dharma_verdict
python app.py
```

### Terminal 3: React Frontend
```bash
cd frontend
npm run dev
```

### Access
- 🌐 Frontend: http://127.0.0.1:5173
- 🔌 Chatbot API: http://127.0.0.1:5000/api/*
- ⚖️ Verdict API: http://127.0.0.1:5001/api/*

---

## Key Files to Update

1. **Update API Keys First:**
   - `features/chatbot/.env`
   - `features/dharma_verdict/.env`

2. **Replace Python Files:**
   - `features/chatbot/app.py` (now API-only)
   - `features/dharma_verdict/app.py` (now API-only)

3. **Create React App:**
   - All files in `frontend/` directory

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in `.env` or kill process |
| CORS error | Ensure `CORS(app)` in Flask |
| API key blocked | Generate new key at aistudio.google.com |
| React won't connect | Check API URLs in `frontend/.env` |
| Session not saved | In-memory storage - cleared on server restart |

---

**Status:** ✅ Complete React + Flask architecture ready
**Last Updated:** April 6, 2026
