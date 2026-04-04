# Portfolio Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a distinctive static portfolio website (index.html) with a printable CV page (resume.html) for Kshitiz Khanal, a Software Engineer with AI/Data experience.

**Architecture:** Four static files — `index.html` (single-page portfolio), `resume.html` (printable CV), `style.css` (shared dark navy theme), `resume.css` (print-optimized CV styles). No build step, no framework, no dependencies except Google Fonts. The frontend-design skill MUST be applied: distinctive typography, cohesive CSS variable system, subtle animations. No generic aesthetics (no Inter/Roboto/Arial, no purple gradients).

**Tech Stack:** HTML5, CSS3 (custom properties, grid, flexbox, @keyframes), vanilla JS (smooth scroll, print trigger, scroll-reveal), Google Fonts (Syne + DM Sans)

---

## File Map

| File | Responsibility |
|------|---------------|
| `style.css` | CSS variables, typography, reset, nav, hero, skills, experience, resume section, contact, animations |
| `index.html` | Single-page portfolio — all sections |
| `resume.css` | Print-optimized CV layout, @media print rules |
| `resume.html` | Standalone printable CV — auto-triggers print on `?print=1` |

---

## Task 1: CSS Foundation — Variables, Typography, Reset

**Files:**
- Create: `style.css`

- [ ] **Step 1: Write the CSS foundation**

Create `style.css` with this exact content:

```css
/* ── Google Fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Design Tokens ────────────────────────────────────────── */
:root {
  --bg:          #0a0f1e;
  --surface:     #111827;
  --surface-2:   #1e2a3a;
  --border:      #1e3a5f;
  --accent:      #38bdf8;
  --accent-dim:  #0ea5e9;
  --accent-glow: rgba(56, 189, 248, 0.15);
  --text:        #e2e8f0;
  --text-muted:  #64748b;
  --text-dim:    #94a3b8;
  --chip-bg:     rgba(56, 189, 248, 0.08);
  --chip-border: rgba(56, 189, 248, 0.25);

  --font-display: 'Syne', sans-serif;
  --font-body:    'DM Sans', sans-serif;

  --radius:    8px;
  --radius-lg: 16px;
  --max-width: 900px;
  --nav-h:     64px;
  --section-gap: 100px;
}

/* ── Reset ────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font-body);
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
}
a { color: inherit; text-decoration: none; }
ul { list-style: none; }
img { display: block; max-width: 100%; }

/* ── Layout ───────────────────────────────────────────────── */
.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 24px;
}

section {
  padding: var(--section-gap) 0;
}

.section-label {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 12px;
}

.section-title {
  font-family: var(--font-display);
  font-size: clamp(28px, 4vw, 40px);
  font-weight: 800;
  color: var(--text);
  margin-bottom: 48px;
  line-height: 1.15;
}
```

- [ ] **Step 2: Verify in browser**

Open `style.css` — no errors in browser devtools. The file should parse cleanly. (We'll wire it to index.html in Task 2.)

---

## Task 2: index.html Skeleton + Sticky Nav

**Files:**
- Create: `index.html`
- Modify: `style.css` (append nav styles)

- [ ] **Step 1: Create index.html skeleton**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Kshitiz Khanal — Software Engineer</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>

  <!-- NAV -->
  <nav class="nav" id="nav">
    <div class="container nav__inner">
      <a href="#" class="nav__name">Kshitiz Khanal</a>
      <ul class="nav__links">
        <li><a href="#about">About</a></li>
        <li><a href="#skills">Skills</a></li>
        <li><a href="#experience">Experience</a></li>
        <li><a href="#resume">Resume</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </div>
  </nav>

  <!-- SECTIONS (placeholders — filled in later tasks) -->
  <section id="about"></section>
  <section id="skills"></section>
  <section id="experience"></section>
  <section id="resume"></section>
  <section id="contact"></section>

  <script src="main.js"></script>
</body>
</html>
```

- [ ] **Step 2: Append nav styles to style.css**

```css
/* ── Nav ──────────────────────────────────────────────────── */
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: var(--nav-h);
  z-index: 100;
  background: rgba(10, 15, 30, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s;
}
.nav.scrolled { border-bottom-color: var(--border); }

.nav__inner {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav__name {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 17px;
  color: var(--text);
  letter-spacing: -0.3px;
}

.nav__links {
  display: flex;
  gap: 32px;
}
.nav__links a {
  font-size: 14px;
  font-weight: 400;
  color: var(--text-dim);
  transition: color 0.2s;
  position: relative;
}
.nav__links a::after {
  content: '';
  position: absolute;
  left: 0; bottom: -2px;
  width: 0; height: 1px;
  background: var(--accent);
  transition: width 0.2s;
}
.nav__links a:hover { color: var(--accent); }
.nav__links a:hover::after { width: 100%; }
```

- [ ] **Step 3: Create main.js with nav scroll behavior**

Create `main.js`:

```js
// Nav scrolled state
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 10);
});
```

- [ ] **Step 4: Open index.html in browser, verify**

Open `index.html` directly in browser (file:// URL). You should see:
- Dark background
- Fixed nav bar at top with "Kshitiz Khanal" on left, links on right
- Nav border appears after scrolling down
- Links hover with accent underline

- [ ] **Step 5: Commit**

```bash
cd /home/kshitiz/research/portfolio
git init
git add index.html style.css main.js
git commit -m "feat: project scaffold, CSS foundation, sticky nav"
```

---

## Task 3: Hero / About Section

**Files:**
- Modify: `index.html` (fill `#about` section)
- Modify: `style.css` (append hero styles)

- [ ] **Step 1: Replace the `#about` section in index.html**

Replace `<section id="about"></section>` with:

```html
<section id="about" class="hero">
  <div class="container hero__inner">
    <div class="hero__eyebrow reveal">Based in Nepal</div>
    <h1 class="hero__name reveal">Kshitiz<br>Khanal</h1>
    <p class="hero__subtitle reveal">Software Engineer &nbsp;·&nbsp; AI / Data</p>
    <p class="hero__bio reveal">
      Software Engineer with experience building data pipelines, LLM-powered
      microservices, and clinical NLP systems. I've worked across the backend
      stack — from orchestrating Airflow DAGs and Celery task queues to
      integrating large language models into healthcare workflows. I enjoy
      solving data-heavy problems and shipping systems that work reliably at scale.
    </p>
    <div class="hero__ctas reveal">
      <a href="https://www.linkedin.com/in/kshitizkhanal05/" target="_blank" rel="noopener" class="btn btn--primary">
        LinkedIn ↗
      </a>
      <a href="mailto:khanalkshitiz05@gmail.com" class="btn btn--ghost">
        Email Me
      </a>
    </div>
  </div>
  <div class="hero__grid-bg" aria-hidden="true"></div>
</section>
```

- [ ] **Step 2: Append hero styles to style.css**

```css
/* ── Hero ─────────────────────────────────────────────────── */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding-top: var(--nav-h);
  overflow: hidden;
}

.hero__grid-bg {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(56,189,248,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,189,248,0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 80% 60% at 50% 50%, black, transparent);
  pointer-events: none;
}

.hero__inner { position: relative; z-index: 1; padding: 80px 24px; }

.hero__eyebrow {
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 20px;
}

.hero__name {
  font-family: var(--font-display);
  font-size: clamp(64px, 10vw, 110px);
  font-weight: 800;
  line-height: 0.95;
  letter-spacing: -2px;
  color: var(--text);
  margin-bottom: 20px;
}

.hero__subtitle {
  font-family: var(--font-display);
  font-size: clamp(16px, 2vw, 20px);
  font-weight: 400;
  color: var(--text-dim);
  margin-bottom: 28px;
  letter-spacing: 0.5px;
}

.hero__bio {
  max-width: 560px;
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-dim);
  margin-bottom: 40px;
}

.hero__ctas { display: flex; gap: 16px; flex-wrap: wrap; }

/* ── Buttons ──────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  border-radius: var(--radius);
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  cursor: pointer;
  border: 1px solid transparent;
}
.btn--primary {
  background: var(--accent);
  color: #0a0f1e;
  border-color: var(--accent);
}
.btn--primary:hover {
  background: var(--accent-dim);
  border-color: var(--accent-dim);
  transform: translateY(-1px);
  box-shadow: 0 8px 24px var(--accent-glow);
}
.btn--ghost {
  background: transparent;
  color: var(--text);
  border-color: var(--border);
}
.btn--ghost:hover {
  border-color: var(--accent);
  color: var(--accent);
  transform: translateY(-1px);
}
```

- [ ] **Step 3: Open index.html in browser, verify**

- Large name renders in Syne font
- Grid dot pattern visible in background
- "LinkedIn ↗" button is sky-blue, "Email Me" is ghost
- Bio text is readable
- Buttons hover with lift + glow

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: hero/about section with dark navy grid background"
```

---

## Task 4: Skills Section

**Files:**
- Modify: `index.html` (fill `#skills` section)
- Modify: `style.css` (append skills styles)

- [ ] **Step 1: Replace `#skills` section in index.html**

Replace `<section id="skills"></section>` with:

```html
<section id="skills">
  <div class="container">
    <p class="section-label reveal">What I work with</p>
    <h2 class="section-title reveal">Skills</h2>
    <div class="skills-grid reveal">

      <div class="skill-group">
        <span class="skill-group__label">Languages</span>
        <div class="chips">
          <span class="chip">Python</span>
        </div>
      </div>

      <div class="skill-group">
        <span class="skill-group__label">Data &amp; Pipelines</span>
        <div class="chips">
          <span class="chip">SQL</span>
          <span class="chip">Apache Airflow</span>
          <span class="chip">PostgreSQL</span>
        </div>
      </div>

      <div class="skill-group">
        <span class="skill-group__label">Queuing</span>
        <div class="chips">
          <span class="chip">Celery</span>
          <span class="chip">SQS</span>
          <span class="chip">RabbitMQ</span>
        </div>
      </div>

      <div class="skill-group">
        <span class="skill-group__label">AI / NLP</span>
        <div class="chips">
          <span class="chip">spaCy</span>
          <span class="chip">stanza</span>
          <span class="chip">LLM Integration</span>
        </div>
      </div>

      <div class="skill-group">
        <span class="skill-group__label">Frameworks</span>
        <div class="chips">
          <span class="chip">Django</span>
          <span class="chip">Flask</span>
          <span class="chip">FastAPI</span>
        </div>
      </div>

      <div class="skill-group">
        <span class="skill-group__label">Cloud</span>
        <div class="chips">
          <span class="chip">AWS</span>
          <span class="chip">Google Cloud</span>
        </div>
      </div>

    </div>
  </div>
</section>
```

- [ ] **Step 2: Append skills styles to style.css**

```css
/* ── Skills ───────────────────────────────────────────────── */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 32px;
}

.skill-group__label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 12px;
}

.chips { display: flex; flex-wrap: wrap; gap: 8px; }

.chip {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 500;
  background: var(--chip-bg);
  border: 1px solid var(--chip-border);
  color: var(--accent);
  transition: all 0.2s;
  cursor: default;
}
.chip:hover {
  background: rgba(56,189,248,0.15);
  border-color: var(--accent);
  transform: translateY(-1px);
}
```

- [ ] **Step 3: Verify in browser**

- Six skill groups render in a responsive grid
- Chips are rounded, sky-blue, with subtle border
- Hover lifts chips slightly

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: skills section with chip grid"
```

---

## Task 5: Experience Section

**Files:**
- Modify: `index.html` (fill `#experience` section)
- Modify: `style.css` (append experience styles)

- [ ] **Step 1: Replace `#experience` section in index.html**

Replace `<section id="experience"></section>` with:

```html
<section id="experience">
  <div class="container">
    <p class="section-label reveal">Where I've worked</p>
    <h2 class="section-title reveal">Experience</h2>
    <div class="timeline">

      <div class="timeline__item reveal">
        <div class="timeline__meta">
          <span class="timeline__date">Mar 2024 — Present</span>
        </div>
        <div class="timeline__card">
          <div class="timeline__header">
            <h3 class="timeline__company">Maitri Services Pvt. Ltd.</h3>
            <span class="timeline__role">Software Engineer</span>
          </div>
          <ul class="timeline__bullets">
            <li>Built and maintained an LLM post-processing microservice for batch HCC medical code extraction using Celery, SQS, and PostgreSQL</li>
            <li>Developed 25+ Apache Airflow DAGs for ETL, billing, and multi-tenant reporting pipelines</li>
            <li>Implemented clinical NLP pipelines using spaCy and stanza for medical text extraction and negation detection</li>
            <li>Integrated AWS S3/SQS and Google Cloud Storage/Vision for document processing workflows</li>
            <li>Built a Django + Celery multi-tenant medical coding platform consuming LLM extraction queues</li>
          </ul>
        </div>
      </div>

      <div class="timeline__item reveal">
        <div class="timeline__meta">
          <span class="timeline__date">Jun 2023 — Mar 2024</span>
        </div>
        <div class="timeline__card">
          <div class="timeline__header">
            <h3 class="timeline__company">Insight Workshop Pvt. Ltd.</h3>
            <span class="timeline__role">Software Engineer</span>
          </div>
          <ul class="timeline__bullets">
            <li>Built REST APIs for an educational platform using Python, Django REST Framework, and PostgreSQL</li>
            <li>Designed data models and implemented role-based access control (RBAC)</li>
          </ul>
        </div>
      </div>

    </div>
  </div>
</section>
```

- [ ] **Step 2: Append experience styles to style.css**

```css
/* ── Experience / Timeline ────────────────────────────────── */
.timeline { position: relative; }
.timeline::before {
  content: '';
  position: absolute;
  left: 0; top: 8px; bottom: 0;
  width: 1px;
  background: linear-gradient(to bottom, var(--accent), transparent);
}

.timeline__item {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 32px;
  padding-left: 28px;
  margin-bottom: 48px;
  position: relative;
}
.timeline__item::before {
  content: '';
  position: absolute;
  left: -4px; top: 10px;
  width: 9px; height: 9px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 12px var(--accent-glow);
}

.timeline__meta { padding-top: 4px; }

.timeline__date {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.timeline__card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 28px 32px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.timeline__card:hover {
  border-color: rgba(56,189,248,0.3);
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.timeline__header { margin-bottom: 16px; }

.timeline__company {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}

.timeline__role {
  font-size: 13px;
  color: var(--accent);
  font-weight: 500;
}

.timeline__bullets {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.timeline__bullets li {
  font-size: 14.5px;
  color: var(--text-dim);
  line-height: 1.65;
  padding-left: 16px;
  position: relative;
}
.timeline__bullets li::before {
  content: '▸';
  position: absolute;
  left: 0;
  color: var(--accent);
  font-size: 11px;
  top: 3px;
}
```

- [ ] **Step 3: Verify in browser**

- Two timeline cards render with a left accent line and glowing dots
- Maitri card has 5 bullet points, Insight Workshop has 2
- Card hover shows accent border glow

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: experience section with vertical timeline"
```

---

## Task 6: Resume Section (iframe + Download)

**Files:**
- Modify: `index.html` (fill `#resume` section)
- Modify: `style.css` (append resume section styles)

Note: `resume.html` is built in Task 7. The iframe will show a blank page until then — that's expected.

- [ ] **Step 1: Replace `#resume` section in index.html**

Replace `<section id="resume"></section>` with:

```html
<section id="resume">
  <div class="container">
    <p class="section-label reveal">Print-ready</p>
    <div class="resume-header reveal">
      <h2 class="section-title" style="margin-bottom:0">Resume</h2>
      <a href="resume.html?print=1" target="_blank" rel="noopener" class="btn btn--primary">
        ⬇ Download PDF
      </a>
    </div>
    <div class="resume-frame reveal">
      <iframe
        src="resume.html"
        title="Kshitiz Khanal — Resume"
        width="100%"
        height="900"
        style="border:none;border-radius:var(--radius);background:#fff;"
      ></iframe>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Append resume section styles to style.css**

```css
/* ── Resume Section ───────────────────────────────────────── */
.resume-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.resume-frame {
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
```

- [ ] **Step 3: Verify in browser**

- "Resume" heading and "⬇ Download PDF" button appear side by side
- iframe renders (white box — resume.html doesn't exist yet, that's fine)
- "Download PDF" button is accent-blue

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: resume section with iframe preview and download button"
```

---

## Task 7: Contact Section

**Files:**
- Modify: `index.html` (fill `#contact` section)
- Modify: `style.css` (append contact + footer styles)

- [ ] **Step 1: Replace `#contact` section in index.html**

Replace `<section id="contact"></section>` with:

```html
<section id="contact" class="contact">
  <div class="container">
    <p class="section-label reveal">Get in touch</p>
    <h2 class="section-title reveal">Contact</h2>
    <p class="contact__desc reveal">
      Open to new opportunities. Reach out via email or connect on LinkedIn.
    </p>
    <div class="contact__links reveal">
      <a href="mailto:khanalkshitiz05@gmail.com" class="contact__link">
        <span class="contact__icon">✉</span>
        khanalkshitiz05@gmail.com
      </a>
      <a href="https://www.linkedin.com/in/kshitizkhanal05/" target="_blank" rel="noopener" class="contact__link">
        <span class="contact__icon">in</span>
        linkedin.com/in/kshitizkhanal05
      </a>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <p>© 2026 Kshitiz Khanal</p>
  </div>
</footer>
```

- [ ] **Step 2: Append contact + footer styles to style.css**

```css
/* ── Contact ──────────────────────────────────────────────── */
.contact { text-align: center; }

.contact__desc {
  font-size: 16px;
  color: var(--text-dim);
  margin-bottom: 40px;
  max-width: 480px;
  margin-left: auto;
  margin-right: auto;
}

.contact__links {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.contact__link {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  font-weight: 500;
  color: var(--text-dim);
  padding: 14px 28px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  transition: all 0.2s;
  min-width: 300px;
  justify-content: center;
}
.contact__link:hover {
  border-color: var(--accent);
  color: var(--accent);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px var(--accent-glow);
}

.contact__icon {
  font-size: 14px;
  font-weight: 700;
  width: 24px;
  text-align: center;
}

/* ── Footer ───────────────────────────────────────────────── */
.footer {
  padding: 32px 0;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 13px;
  color: var(--text-muted);
}
```

- [ ] **Step 3: Verify in browser**

- Contact section shows email + LinkedIn as card-style links
- Centered layout
- Footer renders below with copyright

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: contact section and footer"
```

---

## Task 8: Scroll-Reveal Animations

**Files:**
- Modify: `style.css` (append reveal styles)
- Modify: `main.js` (add IntersectionObserver)

- [ ] **Step 1: Append reveal animation styles to style.css**

```css
/* ── Reveal Animations ────────────────────────────────────── */
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger children in hero */
.hero .reveal:nth-child(1) { transition-delay: 0.05s; }
.hero .reveal:nth-child(2) { transition-delay: 0.15s; }
.hero .reveal:nth-child(3) { transition-delay: 0.25s; }
.hero .reveal:nth-child(4) { transition-delay: 0.35s; }
.hero .reveal:nth-child(5) { transition-delay: 0.45s; }
```

- [ ] **Step 2: Add IntersectionObserver to main.js**

Append to `main.js`:

```js
// Scroll-reveal
const revealEls = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(el => {
    if (el.isIntersecting) {
      el.target.classList.add('visible');
      revealObserver.unobserve(el.target);
    }
  });
}, { threshold: 0.12 });

revealEls.forEach(el => revealObserver.observe(el));
```

- [ ] **Step 3: Verify in browser**

- Refresh the page: hero elements fade in with stagger (eyebrow → name → subtitle → bio → buttons)
- Scroll down: Skills, Experience, Contact sections fade in as they enter viewport
- No flicker or layout shift

- [ ] **Step 4: Commit**

```bash
git add style.css main.js
git commit -m "feat: scroll-reveal animations with staggered hero entrance"
```

---

## Task 9: resume.html + resume.css (Printable CV)

**Files:**
- Create: `resume.html`
- Create: `resume.css`

- [ ] **Step 1: Create resume.css**

```css
/* ── Resume / Print Styles ────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  line-height: 1.6;
  color: #111;
  background: #fff;
  padding: 48px 56px;
  max-width: 820px;
  margin: 0 auto;
}

/* Header */
.r-header {
  border-bottom: 2px solid #0f172a;
  padding-bottom: 16px;
  margin-bottom: 24px;
}
.r-name {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: #0f172a;
  margin-bottom: 4px;
}
.r-title { font-size: 14px; color: #334155; margin-bottom: 6px; }
.r-contact {
  font-size: 12px;
  color: #475569;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}
.r-contact a { color: #0ea5e9; }

/* Section */
.r-section { margin-bottom: 22px; }
.r-section-title {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #0ea5e9;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 4px;
  margin-bottom: 12px;
}

/* Summary */
.r-summary { font-size: 13px; color: #334155; line-height: 1.7; }

/* Skills */
.r-skills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px 24px;
}
.r-skill-row { font-size: 12px; color: #334155; }
.r-skill-row strong { color: #0f172a; font-weight: 600; }

/* Experience */
.r-job { margin-bottom: 16px; }
.r-job-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 2px;
}
.r-job-company { font-weight: 700; font-size: 14px; color: #0f172a; }
.r-job-date { font-size: 11px; color: #64748b; }
.r-job-title { font-size: 12px; color: #0ea5e9; margin-bottom: 8px; }
.r-bullets { padding-left: 0; }
.r-bullets li {
  font-size: 12.5px;
  color: #334155;
  margin-bottom: 5px;
  padding-left: 14px;
  position: relative;
  line-height: 1.5;
}
.r-bullets li::before {
  content: '▸';
  position: absolute;
  left: 0;
  color: #0ea5e9;
  font-size: 10px;
  top: 2px;
}

/* Education */
.r-edu-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 2px;
}
.r-edu-degree { font-weight: 700; font-size: 13px; color: #0f172a; }
.r-edu-date { font-size: 11px; color: #64748b; }
.r-edu-inst { font-size: 12px; color: #334155; margin-bottom: 4px; }
.r-edu-courses { font-size: 11.5px; color: #64748b; }

/* Print */
@media print {
  body { padding: 0; }
  @page { margin: 18mm 16mm; size: A4; }
}
```

- [ ] **Step 2: Create resume.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Kshitiz Khanal — Resume</title>
  <link rel="stylesheet" href="resume.css" />
</head>
<body>

  <!-- HEADER -->
  <header class="r-header">
    <div class="r-name">Kshitiz Khanal</div>
    <div class="r-title">Software Engineer · AI / Data</div>
    <div class="r-contact">
      <span><a href="mailto:khanalkshitiz05@gmail.com">khanalkshitiz05@gmail.com</a></span>
      <span><a href="https://www.linkedin.com/in/kshitizkhanal05/">linkedin.com/in/kshitizkhanal05</a></span>
      <span>Kathmandu, Nepal</span>
    </div>
  </header>

  <!-- SUMMARY -->
  <div class="r-section">
    <div class="r-section-title">Summary</div>
    <p class="r-summary">
      Software Engineer with experience building data pipelines, LLM-powered microservices, and clinical NLP systems.
      Skilled across the backend stack — from orchestrating Airflow DAGs and Celery task queues to integrating large
      language models into healthcare workflows. Strong focus on reliability, data-intensive systems, and scalable architecture.
    </p>
  </div>

  <!-- SKILLS -->
  <div class="r-section">
    <div class="r-section-title">Skills</div>
    <div class="r-skills-grid">
      <div class="r-skill-row"><strong>Languages:</strong> Python</div>
      <div class="r-skill-row"><strong>Data &amp; Pipelines:</strong> SQL, Apache Airflow, PostgreSQL</div>
      <div class="r-skill-row"><strong>Queuing:</strong> Celery, SQS, RabbitMQ</div>
      <div class="r-skill-row"><strong>AI / NLP:</strong> spaCy, stanza, LLM Integration</div>
      <div class="r-skill-row"><strong>Frameworks:</strong> Django, Flask, FastAPI</div>
      <div class="r-skill-row"><strong>Cloud:</strong> AWS, Google Cloud</div>
    </div>
  </div>

  <!-- EXPERIENCE -->
  <div class="r-section">
    <div class="r-section-title">Experience</div>

    <div class="r-job">
      <div class="r-job-header">
        <span class="r-job-company">Maitri Services Pvt. Ltd.</span>
        <span class="r-job-date">Mar 2024 — Present</span>
      </div>
      <div class="r-job-title">Software Engineer</div>
      <ul class="r-bullets">
        <li>Built and maintained an LLM post-processing microservice for batch HCC medical code extraction using Celery, SQS, and PostgreSQL</li>
        <li>Developed 25+ Apache Airflow DAGs for ETL, billing, and multi-tenant reporting pipelines</li>
        <li>Implemented clinical NLP pipelines using spaCy and stanza for medical text extraction and negation detection</li>
        <li>Integrated AWS S3/SQS and Google Cloud Storage/Vision for document processing workflows</li>
        <li>Built a Django + Celery multi-tenant medical coding platform consuming LLM extraction queues</li>
      </ul>
    </div>

    <div class="r-job">
      <div class="r-job-header">
        <span class="r-job-company">Insight Workshop Pvt. Ltd.</span>
        <span class="r-job-date">Jun 2023 — Mar 2024</span>
      </div>
      <div class="r-job-title">Software Engineer</div>
      <ul class="r-bullets">
        <li>Built REST APIs for an educational platform using Python, Django REST Framework, and PostgreSQL</li>
        <li>Designed data models and implemented role-based access control (RBAC)</li>
      </ul>
    </div>
  </div>

  <!-- EDUCATION -->
  <div class="r-section">
    <div class="r-section-title">Education</div>
    <div class="r-edu-header">
      <span class="r-edu-degree">Bachelor of Computer Engineering</span>
      <span class="r-edu-date">Nov 2018 — Apr 2023</span>
    </div>
    <div class="r-edu-inst">Institute of Engineering, Tribhuvan University · Kathmandu, Nepal</div>
    <div class="r-edu-courses">
      Relevant Coursework: Big Data, Database Systems, Data Structures &amp; Algorithms, Operating Systems,
      Cloud Computing, Software Engineering
    </div>
  </div>

  <script>
    // Auto-trigger print when opened with ?print=1
    if (new URLSearchParams(window.location.search).get('print') === '1') {
      window.addEventListener('load', () => window.print());
    }
  </script>

</body>
</html>
```

- [ ] **Step 3: Verify resume.html in browser**

Open `resume.html` directly in browser:
- Clean white CV layout renders
- Name, contact, summary, skills grid, two experience entries, education all present
- Print dialog triggers when you open `resume.html?print=1`

Verify iframe in `index.html`:
- CV preview shows inside the iframe in the Resume section

- [ ] **Step 4: Commit**

```bash
git add resume.html resume.css
git commit -m "feat: resume.html printable CV with auto-print trigger"
```

---

## Task 10: Final Polish + Spec Checklist

**Files:**
- Modify: `style.css` (any remaining gaps)
- Modify: `index.html` (any remaining gaps)

- [ ] **Step 1: Run spec checklist**

Open `index.html` in browser and verify each item:

| Check | Status |
|-------|--------|
| Site loads as static files (no server needed) | verify |
| All sections render: About, Skills, Experience, Resume, Contact | verify |
| Nav links smooth-scroll to correct sections | verify |
| CV preview visible in iframe | verify |
| "Download PDF" opens print dialog for resume.html | verify |
| Typography uses Syne + DM Sans (not Inter/Arial) | verify |
| LinkedIn link goes to correct URL | verify |
| Email mailto link works | verify |
| Chips hover with lift | verify |
| Experience cards hover with accent glow | verify |
| Hero elements stagger-fade on load | verify |
| Sections fade in on scroll | verify |

- [ ] **Step 2: Fix any issues found**

Address any broken items from the checklist above before proceeding.

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "feat: portfolio website complete — all sections verified"
```

---

## Out of Scope

- Mobile responsive layout (not requested)
- Projects section
- Blog
- Contact form
- Dark/light mode toggle
- Analytics
