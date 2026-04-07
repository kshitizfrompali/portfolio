# System Design Interview Questions

> ⭐ = Frequently asked | 🔥 = Trending 2024-25 | 🏢 = Reported at specific companies

---

## Fundamentals

**Q: What is horizontal vs vertical scaling?** ⭐
**Vertical**: add more resources to one machine (bigger CPU, more RAM). Simple but has limits and creates a single point of failure.
**Horizontal**: add more machines. Requires stateless services and a load balancer. More complex but scales further and is fault-tolerant.

---

**Q: What is a load balancer?** ⭐
Distributes incoming requests across multiple servers. Prevents any one server from being overwhelmed. Can do health checks and route around failed servers. Layer 4 (TCP) or Layer 7 (HTTP — can route by URL, headers). AWS ALB is a common choice.

---

**Q: What is a CDN?**
Content Delivery Network — serves static assets (images, CSS, JS) from edge servers near the user. Reduces latency and origin server load. For a portfolio site, Cloudflare or AWS CloudFront would serve HTML/CSS from the nearest edge.

---

**Q: What is a cache and when do you use it?** ⭐
A fast-access store (usually in-memory, e.g. Redis) for frequently read data. Reduces DB load and latency. Use when: reads >> writes, data doesn't change often, recomputing is expensive. Cache invalidation (knowing when to expire data) is the hard problem.

---

**Q: What is eventual consistency?** ⭐
In distributed systems, after a write, replicas may not be immediately consistent — they'll become consistent eventually. Trade-off against strong consistency. Read replicas in PostgreSQL have eventual consistency — writes go to primary, reads from replica may be slightly stale.

---

**Q: What is a microservices architecture?** ⭐ 🔥
Breaking an application into small, independently deployable services each handling one domain. Benefits: independent scaling, independent deployment, technology flexibility. Costs: network overhead, distributed debugging, data consistency challenges. The ECLAT system at Maitri was a microservices architecture — NLP service, SLM service, coding platform, Airflow all separate.

---

**Q: What is an API gateway?** 🔥
A single entry point for clients that routes requests to appropriate microservices. Handles auth, rate limiting, SSL termination, and request logging centrally. AWS API Gateway or Kong are common choices.

---

**Q: What is the CAP theorem?** ⭐
A distributed system can guarantee at most 2 of 3: **Consistency** (all nodes see the same data), **Availability** (every request gets a response), **Partition Tolerance** (system works despite network failures). In practice, network partitions happen, so you choose between CP (consistent, may be unavailable during partition) or AP (available, may return stale data). PostgreSQL is CP. DynamoDB is AP by default.

---

## Design Problems

**Q: Design a system to process medical documents at scale.** ⭐ (similar to Maitri architecture)

1. **Ingestion**: documents uploaded to S3, S3 event triggers SQS message
2. **Queue**: SQS standard queue with DLQ for failures
3. **Processing workers**: Celery workers pull from SQS, download from S3, run NLP extraction (spaCy/stanza)
4. **Validation**: Pydantic schema validation on extracted results
5. **Storage**: write structured results to PostgreSQL; raw documents stay in S3
6. **Monitoring**: queue depth alarm, DLQ alarm, worker health checks
7. **Scale**: add workers horizontally when queue depth grows

---

**Q: Design a URL shortener.** ⭐ (Google, Amazon, Stripe — classic)

Components:
- **API**: POST `/shorten` → returns short code. GET `/{code}` → redirects.
- **ID generation**: random 7-char base62 code (~3.5 trillion combinations). Use UUID or distributed ID generator (Snowflake) to avoid collisions.
- **Storage**: key-value store (Redis for hot lookups, DynamoDB or PostgreSQL for persistence). Schema: `{code: url, created_at, expires_at}`
- **Redirect**: 301 (permanent, browser caches) or 302 (temporary, always hits server for analytics)
- **Scale**: cache hot URLs in Redis (most traffic is to a small % of links). CDN for redirect responses.

---

**Q: Design a data pipeline for ETL.** ⭐ (Data engineering)

1. **Extract**: pull from source (DB, API, S3, webhooks) on schedule or trigger
2. **Transform**: clean, validate, enrich data (handle nulls, type casting, joins)
3. **Load**: write to target (data warehouse, PostgreSQL, S3)
4. **Orchestration**: Airflow DAG manages dependencies and retries
5. **Idempotency**: use `execution_date` as partition key; upsert instead of insert
6. **Monitoring**: alert on pipeline failure, data quality checks (row count, null rate)
7. **Lineage**: track what data came from where (great_expectations, dbt)

---

**Q: Design a notification system (email + chat).** (similar to Airflow failure notifications at Maitri)

1. **Producer**: any service publishes to a `notifications` queue with payload: `{type, recipient, template, data}`
2. **Router**: worker reads queue, routes to appropriate sender (email: SMTP/SES, chat: Google Chat webhook, Slack API)
3. **Template engine**: Jinja2 templates for message body
4. **Deduplication**: track sent notifications in Redis — don't send the same alert twice in 5 minutes
5. **Retry**: automatic retries with exponential backoff for transient failures
6. **Audit log**: store all sent notifications in DB for debugging

---

**Q: Design a multi-tenant SaaS platform.** 🔥 (startups, SaaS companies)

**Tenant isolation options**:
- Separate databases: strongest isolation, expensive, hard to manage many tenants
- Separate schemas (PostgreSQL): good isolation, used `django-tenants`, scales to hundreds of tenants
- Shared schema + `tenant_id`: cheapest, scales to millions of tenants, risk of data leaks if queries forget `tenant_id`

**Routing**: middleware extracts tenant from subdomain/JWT, sets DB connection to correct schema.

**Auth**: each tenant has its own user pool. JWTs include `tenant_id` claim.

**Billing**: track usage per tenant (API calls, storage, records).

**Migrations**: run per-tenant. `django-tenants` does this automatically.

---

**Q: Design a system for batch LLM processing.** 🔥 (AI companies)

1. **Input queue**: SQS with documents to process (patient notes, contracts, etc.)
2. **Batch coordinator**: groups documents into batches (reduce API calls), sends to LLM API
3. **LLM API**: async batch endpoint (OpenAI Batch API or Claude's batch) for cost savings
4. **Output queue**: results published to SQS when complete
5. **Post-processor**: validates output schema (Pydantic), idempotent DB writes
6. **DLQ**: malformed LLM output sent to DLQ for review
7. **Cost control**: token usage tracking, budget alerts, auto-pause if cost spikes

This is essentially the SLM service architecture at Maitri.

---

**Q: How would you design a rate limiter?** ⭐ (Stripe, Twilio, API companies)

Algorithms:
- **Token bucket**: add tokens at fixed rate, consume on request. Allows bursts.
- **Sliding window**: count requests in the last N seconds using Redis sorted set.
- **Fixed window**: count requests per time bucket — simple but allows burst at boundary.

Implementation: Redis with `INCR` + `EXPIRE` for fixed window. Sorted set with `ZRANGEBYSCORE` for sliding window.

Store per: user_id, IP, API key. Return 429 with `Retry-After` header when limit exceeded.

---

**Q: Design a system for real-time health monitoring of Airflow pipelines.** (similar to Maitri ops)

1. **Metrics collection**: Airflow StatsD emitter → Prometheus
2. **Dashboards**: Grafana dashboards for DAG success rate, task duration, queue depth
3. **Alerting**: alert on: task failure rate > threshold, DAG duration > SLA, worker count drops
4. **Notifications**: PagerDuty or Google Chat webhook for on-call
5. **Log aggregation**: ELK stack or CloudWatch for task logs
6. **SLA tracking**: track execution time per DAG, alert if P95 exceeds target

---

## Design Principles

**Q: What is idempotency and why does it matter in distributed systems?** ⭐
An operation is idempotent if executing it multiple times has the same effect as executing it once. Critical in distributed systems where retries and at-least-once delivery are common. Make writes idempotent with upserts. Use idempotency keys for API endpoints (Stripe uses this).

---

**Q: What is the circuit breaker pattern?** 🔥
Wraps calls to an external service. Tracks failure rate. When failures exceed a threshold, "opens" the circuit — subsequent calls fail immediately without hitting the service (gives it time to recover). After a timeout, tries again ("half-open"). Prevents cascade failures.

---

**Q: What is the saga pattern?** 🔥 (microservices)
Managing distributed transactions across services. Each step has a compensating transaction (undo). If step 3 fails, steps 1 and 2 are compensated. Two styles: choreography (services react to events) and orchestration (central coordinator issues commands).

---

**Q: What is eventual consistency and how do you handle it in your API?** ⭐
After a write, replicas may briefly return stale data. Handle with:
1. Read-your-writes consistency (route the user's reads to the primary after their write)
2. Version vectors / timestamps (tell clients data version)
3. Optimistic locking (reject updates on stale versions)

---

**Q: What is the difference between synchronous and asynchronous APIs?** ⭐
Sync: client waits for response. Simple but blocks on slow operations. Async: client sends request, gets an ID, polls for result or receives a webhook. Better for long-running operations. LLM calls are often async — send prompt, get job ID, poll for completion.

---
