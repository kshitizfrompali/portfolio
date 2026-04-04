# Portfolio Website & CV — Design Spec

**Date:** 2026-04-04
**Author:** Kshitiz Khanal
**Status:** Approved

---

## Overview

A personal portfolio website for Kshitiz Khanal, a Software Engineer with AI/Data experience targeting both Backend/Data Engineer and AI/ML Engineer roles. The site presents professional background, skills, experience, and a downloadable CV — all in a single static site with no build step or framework.

---

## Goals

- Present Kshitiz as a credible, hireable software engineer with AI/data strengths
- Provide a downloadable, print-ready CV (PDF via browser print)
- Look distinctive and professionally designed — not generic AI-generated aesthetics
- Work as pure static files, hostable anywhere (GitHub Pages, Netlify, etc.)

---

## Tech Stack

- **Pure HTML/CSS/JS** — no framework, no build step, no dependencies
- **Frontend-design skill** must be applied during implementation: distinctive typography (no Inter/Arial/Roboto), bold aesthetic execution, CSS animations, cohesive CSS variable-based theming
- Two HTML pages share CSS via external stylesheets

---

## File Structure

```
portfolio/
├── index.html       # Main single-page portfolio
├── resume.html      # Standalone printable CV page
├── style.css        # Dark navy theme, shared styles
└── resume.css       # Clean print-optimized CV styles
```

---

## Design Direction

**Theme:** Dark navy + tag chips + card-based layout (Option C from brainstorming)

**Aesthetic:** Technical, distinctive, refined dark. Think deep space / engineering precision — not startup purple gradients. Deep navy (`#0f172a`) background, sharp contrast accents (electric blue or teal), skill chips, and a vertical timeline for experience. Staggered scroll-reveal animations on load.

**Typography:** Pair a distinctive display font (e.g., Syne, Outfit, Space Mono for code accents) with a clean body font (e.g., DM Sans, Geist). Never use Inter, Roboto, or Arial.

**Motion:** Staggered fade-in on page load for hero elements. Subtle hover effects on nav links, skill chips, and experience cards. Scroll-reveal for sections below the fold.

---

## Pages

### index.html — Portfolio

#### 1. Nav (sticky)
- Left: `Kshitiz Khanal` (name as wordmark)
- Right: smooth-scroll links — `About · Skills · Experience · Resume · Contact`
- Sticky on scroll, subtle backdrop blur

#### 2. Hero / About
- Full-width section, dark navy gradient background
- Large display: **Kshitiz Khanal**
- Subtitle: `Software Engineer · AI / Data`
- Bio:
  > Software Engineer with experience building data pipelines, LLM-powered microservices, and clinical NLP systems. I've worked across the backend stack — from orchestrating Airflow DAGs and Celery task queues to integrating large language models into healthcare workflows. I enjoy solving data-heavy problems and shipping systems that work reliably at scale.
- CTA buttons: `LinkedIn ↗` and `Email Me`
  - LinkedIn: https://www.linkedin.com/in/kshitizkhanal05/
  - Email: khanalkshitiz05@gmail.com

#### 3. Skills
- Section heading: `Skills`
- Tag/chip grid, grouped by category with a small label above each group:
  - **Languages:** Python
  - **Data & Pipelines:** SQL, Apache Airflow, PostgreSQL
  - **Queuing:** Celery, SQS, RabbitMQ
  - **AI / NLP:** spaCy, stanza, LLM integration
  - **Frameworks:** Django, Flask, FastAPI
  - **Cloud:** AWS

#### 4. Experience
- Section heading: `Experience`
- Vertical timeline (left border line + cards)
- **Card 1 — Most Recent:**
  - Company: **Maitri Services Pvt. Ltd.**
  - Title: Software Engineer
  - Duration: March 2024 – Present
  - Bullets:
    - Built and maintained an LLM based processing microservice for batch HCC medical code extraction using Django,Celery, SQS, and PostgreSQL
    - Developed multiple Apache Airflow DAGs for ETL, billing, and multi-tenant reporting pipelines
    - Implemented clinical NLP pipelines using spaCy and stanza for medical text extraction and negation detection
    - Integrated AWS S3/SQS and Google Cloud Storage/Vision for document processing workflows

- **Card 2:**
  - Company: **Insight Workshop Pvt. Ltd.**
  - Title: Software Engineer
  - Duration: June 2023 – March 2024
  - Bullets:
    - Built REST APIs for an educational platform using Python, Django REST Framework, and PostgreSQL
    - Designed data models and implemented role-based access control (RBAC)

#### 5. Resume
- Section heading: `Resume`
- "Download PDF" button at top right of section — opens `resume.html?print=1` in a new tab, which auto-triggers `window.print()`
- `<iframe>` embedding `resume.html` — full preview of the CV below the button
- iframe height: fixed at 900px with internal scroll

#### 6. Contact
- Section heading: `Contact`
- Minimal layout, centered
- Email: khanalkshitiz05@gmail.com (mailto link)
- LinkedIn: https://www.linkedin.com/in/kshitizkhanal05/ (external link)
- No contact form — keep it simple

---

### resume.html — Printable CV

Standalone page designed for printing to PDF. Loads `resume.css` only.

**Content:**
- **Header:** Kshitiz Khanal | Software Engineer | khanalkshitiz05@gmail.com | linkedin.com/in/kshitizkhanal05/
- **Summary:** Same bio as portfolio
- **Skills:** Listed inline by category (same groups as portfolio)
- **Experience:**
  - Maitri Services Pvt. Ltd. — Software Engineer (March 2024 – Present) + all bullets
  - Insight Workshop Pvt. Ltd. — Software Engineer (June 2023 – March 2024) + all bullets
- **Education:**
  - Bachelor of Computer Engineering
  - Institute of Engineering, Tribhuvan University — Kathmandu, Nepal
  - November 2018 – April 2023
  - Relevant Coursework: Big Data, Database Systems, Data Structures & Algorithms, Operating Systems, Cloud Computing, Software Engineering

**Print behavior:**
- `@media print` CSS hides everything except resume content
- Clean white background, black text, ATS-readable layout
- Target: 1–2 pages when printed

**Download trigger:**
- When opened with `?print=1` query param, auto-triggers `window.print()` via inline JS
- "Download PDF" button on `index.html` opens `resume.html?print=1` in new tab

---

## Out of Scope

- Projects section (not requested)
- Blog
- Contact form (backend required)
- Dark/light mode toggle
- Analytics

---

## Success Criteria

- [ ] Site loads as static files with no server needed
- [ ] All sections render correctly on desktop (primary target)
- [ ] CV preview visible in iframe on index.html
- [ ] "Download PDF" opens browser print dialog for resume.html
- [ ] Design is visually distinctive — passes frontend-design skill standards (not generic AI aesthetics)
- [ ] Typography uses non-generic fonts loaded from Google Fonts or similar
- [ ] Smooth-scroll navigation works
- [ ] Links to LinkedIn and email are correct and functional
