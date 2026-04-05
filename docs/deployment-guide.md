# Nyay Mitra — Deployment Guide
## Extending nyay-mitra.live with New Pages

---

### Files in This Package

| File | Description |
|------|-------------|
| `index.html` | Modified homepage — adds **Modern Law CTA button** above footer and updates nav with 3 new links |
| `modern-law.html` | Modern Indian Law System guidance page |
| `studies.html` | Sacred Texts & Modern Life — how to learn and apply dharmic texts |
| `yuga-events.html` | The Four Yugas — events, summaries, and moral takeaways |
| `texts-hub.html` | Hindu Epics & Texts Hub — consolidated resource with descriptions and links |

---

### What Was Changed vs the Original

**`index.html` only — two non-destructive additions:**
1. Nav links list extended with `Studies`, `Yugas`, and `Texts Hub` links
2. A new CTA section (`#modern-law-cta`) inserted between `#scriptures` and `<footer>` — a gold-styled redirect button to `modern-law.html`

All original content, structure, animations, and styling are completely untouched.

---

### Routing Strategy: Client-Side (Static Files)

All pages are standalone `.html` files with no dependencies beyond Google Fonts (CDN). They use relative links (`href="modern-law.html"`, `href="index.html"` etc.). This works with any static host without any server configuration.

**No backend, no build step, no framework required.**

---

### Deployment Options

#### Option A — Direct FTP / File Manager Upload (Simplest)
If nyay-mitra.live is hosted on a traditional host (cPanel, Hostinger, etc.):
1. Log into your hosting control panel
2. Open **File Manager** → navigate to `public_html/` (or `www/`)
3. **Back up** the existing `index.html` first
4. Upload all 5 HTML files into the **same root directory** as the existing `index.html`
5. Visit `https://nyay-mitra.live/modern-law.html` to verify

#### Option B — Vercel (if currently hosted on Vercel)
```bash
# Clone or download your existing Vercel project
# Place the 5 HTML files in the project root (same folder as existing index.html)
vercel --prod
```

#### Option C — Netlify Drag & Drop
1. Go to app.netlify.com → your site → **Deploys**
2. Drag the entire updated folder (with all 5 files) into the deploy drop zone
3. Netlify will auto-deploy in ~30 seconds

#### Option D — GitHub Pages
```bash
git add index.html modern-law.html studies.html yuga-events.html texts-hub.html
git commit -m "Add Modern Law, Studies, Yuga Events, Texts Hub pages"
git push origin main
```
GitHub Pages will auto-redeploy.

---

### URL Structure After Deployment

```
https://nyay-mitra.live/                   → Homepage (modified)
https://nyay-mitra.live/modern-law.html    → Modern Indian Law System
https://nyay-mitra.live/studies.html       → Sacred Studies
https://nyay-mitra.live/yuga-events.html   → Yuga Events
https://nyay-mitra.live/texts-hub.html     → Hindu Epics & Texts Hub
```

---

### Optional: Clean URLs (No .html Extension)

If you want `nyay-mitra.live/modern-law` instead of `/modern-law.html`, add a `_redirects` file (Netlify) or `vercel.json` (Vercel):

**Netlify `_redirects`:**
```
/modern-law     /modern-law.html    200
/studies        /studies.html       200
/yuga-events    /yuga-events.html   200
/texts-hub      /texts-hub.html     200
```

**Vercel `vercel.json`:**
```json
{
  "rewrites": [
    { "source": "/modern-law",  "destination": "/modern-law.html" },
    { "source": "/studies",     "destination": "/studies.html" },
    { "source": "/yuga-events", "destination": "/yuga-events.html" },
    { "source": "/texts-hub",   "destination": "/texts-hub.html" }
  ]
}
```

---

### Pre-Launch Checklist

- [ ] Back up existing `index.html` before replacing
- [ ] Test all 5 files locally by opening them in a browser
- [ ] Check that the **"Explore Modern Indian Law →"** button on the homepage links correctly
- [ ] Verify nav links work on mobile (hamburger/collapse not needed — nav hides on <900px already)
- [ ] Check accordion on `modern-law.html` opens and closes
- [ ] Check dharma bar animations on `yuga-events.html` trigger on scroll
- [ ] Verify all external links (Sacred-texts.com, Archive.org, Vedabase) open in new tabs
- [ ] Run a Lighthouse accessibility check (all pages use semantic HTML, aria-label not needed given existing design)

---

### Notes on Constraints Followed

- **Zero modification** to existing homepage content — only appended new section + nav items
- **Design system preserved** — identical CSS variables, font stack, clip-paths, animation timings, and component patterns
- **Client-side routing** — simple `.html` file links, works on any host
- **Accessibility** — semantic `<nav>`, `<section>`, `<footer>`, `<h1>`–`<h3>` hierarchy; button contrast >4.5:1 against dark background; keyboard navigable (all interactive elements are native `<a>` or `<button>`)
- **Responsive** — all new pages inherit the same mobile breakpoints (`max-width: 900px`, `480px`)
- **No login credentials required** — all changes are purely additive static files

---

*Built for Nyay Mitra · यतो धर्मस्ततो जयः*
