# Nyay Mitra (न्याय मित्र) — Dharma Edition

> **Friend of Justice** — A celestial gateway to dharmic wisdom and legal consciousness

A beautifully designed, immersive web application dedicated to exploring dharmic principles, justice systems, and contemporary legal understanding through the lens of ancient and modern wisdom traditions.

![Dharma Edition](https://img.shields.io/badge/Edition-Dharma-gold?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

---

## ✨ Features

### 🌌 Immersive User Experience
- **Celestial Login Page** — Featuring an animated space scene with stars, galaxies, and shooting stars
- **Dharmic Color Palette** — Gold (#C9A84C), Saffron (#E8831A), and Deep Ink (#080604) throughout
- **Smooth Animations** — Canvas-based rendering for optimal performance
- **Responsive Design** — Seamless experience on desktop, tablet, and mobile

### 🔐 Authentication System
- User registration and login capabilities
- Secure credential storage using localStorage
- Session management with automatic redirect to login for protected pages
- Demo user provided for testing (`demo` / `password123`)

### 🎵 Persistent Background Music
- Ambient background music starts on login page
- Music continues seamlessly across page navigation
- Volume control with percentage-based slider (0-100%)
- Playback state preserved during session

### 📚 Content Pages
- **Index (Home)** — Overview and introduction to Nyay Mitra
- **Modern Law** — Intersection of dharmic principles with contemporary legal systems
- **Studies** — In-depth research and scholarly explorations
- **Yuga Events** — Historical and cosmological perspectives
- **Texts Hub** — Curated collection of dharmic texts and resources

---

## 🚀 Quick Start

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/preetesh18/Nyay-Mitra-Dharma-Edition.git
   cd "Nyay-Mitra-Dharma Edition"
   ```

2. **Open in browser:**
   - Simply open `login.html` in your web browser
   - No build process or dependencies required
   - Pure static HTML, CSS, and JavaScript

3. **Test Login:**
   - Username: `demo`
   - Password: `password123`
   - Or register a new account

### Live Demo
Visit the deployed version on Vercel: *(URL will be available after deployment)*

---

## 📖 Usage Guide

### Logging In
1. Navigate to the login page
2. Enter credentials or register for a new account
3. Background music automatically starts
4. Browse through content pages with persistent audio

### Volume Control
- Use the **Volume ±** buttons at the bottom-right corner
- Adjust the **Volume Slider** (0-100%)
- **Mute button** available for quick silence
- Settings persist across page navigation

### Navigation
- Use the top navigation bar to browse different sections
- Click **Logout** button in the top-right to exit
- All pages are authentication-protected

---

## 🏗️ Project Structure

```
Nyay-Mitra-Dharma Edition/
├── login.html                    # Authentication gateway with space animation
├── index.html                    # Home page
├── modern-law.html              # Legal systems & dharmic principles
├── studies.html                 # Research & scholarly content
├── texts-hub.html               # Curated texts collection
├── yuga-events.html             # Historical & cosmological perspective
├── auth.js                      # Authentication system (60 lines)
├── shared-audio.js              # Cross-page audio management (180 lines)
├── audio-sounds.js              # Audio controls & UI (400+ lines)
├── vercel.json                  # Vercel deployment configuration
├── deployment-guide.md          # Deployment instructions
└── README.md                    # This file
```

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Animations** | Canvas API, CSS Keyframes |
| **Audio** | HTML5 Audio API |
| **State Management** | localStorage, sessionStorage |
| **Deployment** | Vercel (Static Site) |
| **Version Control** | Git & GitHub |

### Key Dependencies
- **None** — Pure vanilla JavaScript, no external libraries required
- Single audio file: "Interstellar Theme Song" MP3

---

## 🔐 Authentication Details

### User Storage
- Users stored in `localStorage` under key: `nyay-users`
- Credentials stored as JSON array format
- Sessions managed via `nyay-current-user` key

### Security Notes
- ⚠️ This is a demo implementation using Base64 encoding
- For production: Implement server-side authentication with bcrypt hashing
- Never store passwords in plaintext in real applications
- HTTPS recommended for all deployments

### Demo Users
```javascript
{
  username: "demo",
  password: "password123"  // Base64 encoded in storage
}
```

---

## 🎨 Design System

### Color Palette (Dharmic Theme)
```css
--gold: #C9A84C          /* Primary accent */
--gold-lt: #F0D483       /* Light highlight */
--saffron: #E8831A       /* Secondary accent */
--cream: #F5E8CA         /* Text color */
--ink: #080604           /* Deep background */
```

### Typography
- **Headers:** Cinzel Decorative (serif)
- **Titles:** Cinzel (serif)
- **Body:** EB Garamond (serif)
- **Devanagari Text:** Noto Serif Devanagari

### Animations
- Login slide-in: 0.8s cubic-bezier
- Tab transitions: 0.3s smooth
- Twinkling stars: Natural twinkle effect
- Galaxies: Slow rotation at 0.001 rad/frame
- Shooting stars: 2-3 second streaks across viewport

---

## 🚀 Deployment

### Deploy to Vercel (Recommended)

1. **Push to GitHub:**
   ```bash
   git push origin main
   ```

2. **Deploy on Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Select your GitHub repository
   - Click "Deploy"
   - Your site goes live instantly!

### Custom Domain (Optional)
1. In Vercel dashboard, go to Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### Local Testing
```bash
# Using Python 3
python -m http.server 8000

# Using Node.js (http-server)
npx http-server

# Using Live Server in VS Code
# Install Live Server extension and open login.html
```

---

## 📝 File Descriptions

| File | Purpose | Size |
|------|---------|------|
| `login.html` | Login gateway with space animation | 480 lines |
| `auth.js` | User authentication & registration | 60 lines |
| `shared-audio.js` | Cross-page audio persistence | 180 lines |
| `audio-sounds.js` | Audio playback controls | 400+ lines |
| `index.html` | Home page content | 200+ lines |
| `modern-law.html` | Legal systems page | 200+ lines |
| `studies.html` | Research content page | 200+ lines |
| `texts-hub.html` | Sacred texts collection | 200+ lines |
| `yuga-events.html` | Cosmological events page | 200+ lines |

---

## 🎵 Audio Credit

**Background Music:** "Interstellar Theme Song _ Interstellar Background Music"
- Perfect ambience for dharmic wisdom exploration
- Loops seamlessly across page navigation
- Volume-controlled for user preference

---

## 🔄 Recent Updates

### Latest Release (March 2026)
✅ Space scene animation with stars and galaxies
✅ Volume slider fixed (0-100% working)
✅ Persistent background music across pages
✅ User authentication system
✅ Responsive mobile design
✅ Vercel deployment ready

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Guidelines
- Follow the existing code style (Vanilla JS practices)
- Test changes locally before submitting PR
- Update README if adding new features
- Maintain the dharmic design theme

---

## 📄 License

This project is licensed under the **MIT License** — see the LICENSE file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify and distribute
- ✅ Use privately
- ❌ Hold liable (provided as-is)

---

## 📞 Support & Feedback

- **Issues:** Report bugs via GitHub Issues
- **Discussions:** Share ideas in GitHub Discussions
- **Email:** Consider reaching out through project contacts

---

## 🙏 Acknowledgments

- **Dharmic Wisdom Traditions** — Ancient sources of justice and righteousness
- **Modern Legal Scholars** — Contemporary perspectives on justice
- **Web Community** — Open-source tools and practices
- **Night Sky** — Inspiration for celestial design

---

## 📚 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [GitHub Pages](https://pages.github.com)

---

**Made with ❤️ for justice, dharma, and knowledge**

*न्याय मित्र — Friend of Justice*
