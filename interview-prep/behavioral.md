# Behavioral Interview Questions

> These are questions about your actual experience. Answer using the STAR method:
> **S**ituation → **T**ask → **A**ction → **R**esult

---

## About Your Work

**Q: Tell me about yourself.**

I'm a software engineer based in Nepal with about 2 years of experience building backend systems and data pipelines. At Maitri Services I've worked on LLM post-processing microservices, Airflow ETL pipelines, and clinical NLP systems for healthcare data. Before that at Insight Workshop I built REST APIs for an educational platform. I studied Computer Engineering at Tribhuvan University.

What excites me right now is the intersection of engineering and product thinking — with AI tools accelerating how fast software can be built, I care as much about what to build as how to build it.

---

**Q: Walk me through a project you're most proud of.**

The LLM post-processing service at Maitri. It's a Celery microservice that consumes LLM-extracted medical code results from SQS, validates them with Pydantic, filters by HCC rules, and writes to PostgreSQL.

What made it challenging: the data involved real patient records, so correctness was critical. I had to handle: malformed LLM output, duplicate messages (at-least-once SQS delivery), race conditions when multiple workers processed the same patient, and batch processing for cost efficiency.

Result: a reliable pipeline that processes thousands of patient records daily, with DLQ monitoring to catch edge cases. 116 commits — it grew with the product.

---

**Q: Describe a technically difficult bug you solved.**

In the SLM service, we had a subtle data integrity bug — patients were occasionally receiving HCC codes from the wrong organization. Intermittent, hard to reproduce.

I traced it through DB query logs, wrote a script to find mismatched records, and eventually isolated it: the patient filter query joined on `patient_id + year + hcc_version` but not `organization_id`. In edge cases where two organizations had the same patient ID in the same year, results bled across orgs.

The fix was one line — adding `organization_id` to the filter. But finding it took a full day of systematic investigation. I also wrote a regression test and added a DB constraint to catch similar bugs at the schema level.

---

**Q: Tell me about a time you improved performance significantly.**

A billing report Airflow DAG was taking 45 minutes. Profiled it with `cProfile` — 90% of time was in Excel generation, writing row by row with `openpyxl`.

Rewrote the Excel write to batch the entire dataset as a list of lists first, then write in one pass. Also added S3 caching — skip regeneration if the report for the same date already exists.

Result: 45 minutes → 4 minutes. Also reduced storage costs because idempotent re-runs no longer regenerated identical files.

---

**Q: Describe a time you had to learn something new quickly.**

When I started at Maitri, I had to get up to speed on Apache Airflow, Celery, and medical coding concepts (HCC codes, ICD-10) simultaneously — while contributing to production code.

I spent the first week reading architecture docs and tracing data flow across 6 repos before writing any code. I picked up Airflow by studying existing DAGs in the codebase and reading the official docs for anything unclear. For HCC coding, I asked the domain expert on the team targeted questions rather than trying to become an expert myself.

By week three I was shipping features. The lesson: understand the system boundaries first, then go deep on what you need.

---

**Q: Tell me about a time you disagreed with a technical decision.**

In the coding platform, there was a plan to add a complex caching layer for a slow endpoint before investigating why it was slow.

I pushed back — proposed profiling first to understand the root cause. It turned out to be a missing DB index, not a caching problem. Adding an index fixed the issue without introducing cache invalidation complexity.

I try to frame pushback with evidence rather than opinion. "I think we should check X before Y, here's why" lands better than "I disagree with this approach."

---

**Q: How do you handle working on a large codebase you're not familiar with?**

I have a three-step approach:
1. Read any architecture documentation and README
2. Trace one end-to-end request or data flow through the code
3. Look at recent git history to understand what's actively changing

At Maitri I was onboarded to six repos simultaneously. I started by mapping data flow across services (what talks to what, what queues go where) before reading any implementation code. That mental map made individual files much easier to understand.

---

**Q: Describe a situation where you had to work with incomplete requirements.**

Building the HCC ingestion scripts for the 2026 coding year. The spec was incomplete — we had the source data files but the ingestion logic for some edge cases wasn't documented.

I built the core ingestion path first (clear from existing 2025 scripts), then surfaced specific questions about the edge cases to the domain expert rather than assuming. I implemented an "optional ingestion" flag so unclear cases could be excluded initially and re-included once confirmed.

Shipping something working with known gaps is better than shipping something broken that tries to handle everything.

---

## Career & Goals

**Q: Why are you interested in this role?**

Tailor per company. General structure:
- What specifically about their work connects to what you've built (pipelines, AI, healthcare, etc.)
- What you'll learn or how you'll grow
- Why now (2 years of experience, ready for more scope)

---

**Q: Where do you see yourself in 3-5 years?**

I want to grow into a role where I'm shaping what gets built, not just how. With AI changing how fast software can be created, I believe the most valuable engineers are those who think in products — who understand user problems, design the right system, and ship it end to end. I'm actively building that capability alongside my technical depth.

---

**Q: What are your strengths?**

1. Systematic debugging — I trace problems to root causes rather than applying patches
2. End-to-end ownership — I'm comfortable owning a feature from schema design to deployment
3. Learning velocity — I've shipped production code across 6 unfamiliar codebases in 2 years

---

**Q: What are your weaknesses?**

I can go deep on problems and lose track of time — I'll keep investigating a bug past the point of diminishing returns. I've been working on timeboxing investigation (set a 1-hour limit, then escalate or ask for help). I've also been deliberately practicing explaining technical decisions in non-technical terms, since that becomes more important as you work with more stakeholders.

---

**Q: Why are you leaving your current role?**

Looking for broader scope — I want to work on systems that affect more users and solve more complex problems. I've built strong foundations in data pipelines and LLM integration; I'm ready for an environment where I can go deeper on product impact and technical leadership.

*(Adapt honestly to your actual situation.)*

---

**Q: What kind of environment do you work best in?**

I do best with clear problem statements and autonomy on implementation. I like async communication for deep work and sync time for ambiguous design decisions. I value teams that write things down and do code review — both make me better.

---

## Questions to Ask Interviewers

*Always have 3-4 questions ready.*

1. What does the first 90 days look like for someone joining this team?
2. What's the biggest technical challenge the team is working through right now?
3. How does the team balance feature work vs technical debt?
4. What does a successful engineer on this team look like 6 months in?
5. How does the team use AI tools in day-to-day development?

---
