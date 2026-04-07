# Celery, Message Queues & Async Processing Interview Questions

> ⭐ = Frequently asked | 🔥 = Trending 2024-25

---

## Basic

**Q: What is a message queue and why use one?** ⭐
A message queue decouples producers (who send work) from consumers (who do work). The producer puts a message on the queue and continues — it doesn't wait for the consumer. Enables async processing, load leveling, retry logic, and horizontal scaling. Examples: RabbitMQ, SQS, Kafka.

---

**Q: What is Celery?** ⭐
A distributed task queue for Python. You define tasks as Python functions, call `.delay()` or `.apply_async()` to queue them, and Celery workers pick them up and execute them — possibly on different machines. Supports retries, scheduling, routing, and monitoring.

---

**Q: What is a Celery broker?**
The message transport — stores the task queue. Celery supports Redis, RabbitMQ, and SQS as brokers. The broker holds tasks until a worker picks them up. Redis is simplest. RabbitMQ supports complex routing. SQS is managed and AWS-native.

---

**Q: What is a Celery result backend?**
Stores task results so callers can retrieve them later. Redis or Django DB are common backends. Not always needed — if you don't need the return value, disable the result backend for performance.

---

**Q: What is the difference between `.delay()` and `.apply_async()`?**
`.delay()` is shorthand for `.apply_async()` with no extra options. `.apply_async()` lets you set eta (scheduled time), countdown (delay in seconds), queue routing, expiry, and retry policy.

---

**Q: What is RabbitMQ?** ⭐
An open-source message broker implementing AMQP. Supports exchanges (topic, direct, fanout), routing keys, queues, dead-letter exchanges, and acknowledgements. More powerful routing than SQS. Used as Celery broker in the coding platform at Maitri.

---

**Q: What is Amazon SQS?** ⭐
AWS managed message queue. Two types: Standard (at-least-once, best-effort ordering) and FIFO (exactly-once, strict ordering, lower throughput). No broker to manage. I used Standard SQS in the SLM service for LLM batch processing — simple, scalable, and AWS-native.

---

## Intermediate

**Q: What is "at-least-once delivery" and how does it affect your tasks?** ⭐
A message may be delivered more than once (e.g. if a worker crashes after processing but before acknowledging). Your task must be **idempotent** — running it twice produces the same result. In the HCC extraction service I checked if a record already existed before inserting to handle duplicates safely.

---

**Q: What is exactly-once delivery and is it truly achievable?** 🔥
SQS FIFO + deduplication ID provides near-exactly-once. Kafka transactions provide exactly-once semantics. But true end-to-end exactly-once is very hard — network failures can cause re-deliveries even with strong guarantees. Design for idempotency rather than relying on delivery guarantees.

---

**Q: What is a Dead Letter Queue (DLQ)?** ⭐
A queue where messages go after failing a set number of times (`maxReceiveCount`). Used to isolate poison pills — malformed messages that always cause the worker to crash. Monitor DLQ depth as a signal for bugs. In the SLM service I configured a DLQ with `maxReceiveCount=3` and an alarm on DLQ depth.

---

**Q: How do you handle a poison pill message?**
Set a `maxReceiveCount` + DLQ. After N failures, message moves to DLQ automatically. Inspect DLQ messages to find the root cause. Fix the worker, then replay messages from DLQ back to the main queue.

---

**Q: What is `ack_late` in Celery and when do you use it?**
By default Celery acknowledges the task immediately when received (before execution). With `ack_late=True`, the task is acknowledged only after it completes successfully. If the worker dies mid-task, the message goes back to the queue and gets retried. Use when tasks are critical and must not be lost, and when tasks are idempotent.

---

**Q: How do you route tasks to specific Celery queues?**
Define queues and route task types to them in `CELERY_TASK_ROUTES`. Start workers listening on specific queues with `-Q queue_name`. In SLM services I had a `llm_processing` queue (fewer workers, more memory) and a `db_writes` queue (many workers, lightweight).

```python
CELERY_TASK_ROUTES = {
    'tasks.run_llm': {'queue': 'llm_processing'},
    'tasks.write_results': {'queue': 'db_writes'},
}
```

---

**Q: What is the difference between Celery's `retry()` and automatic retries?**
`retry()` in the task body gives you full control — set countdown, max_retries, exc. Automatic retries (`autoretry_for`, `max_retries`, `retry_backoff`) handle retries based on exception type without boilerplate.

```python
@app.task(autoretry_for=(SQSClientError,), max_retries=3, retry_backoff=True)
def process_extraction(payload):
    ...
```

---

**Q: What is Celery Beat?**
Celery Beat is a scheduler that sends periodic tasks to the queue. Like cron, but managed by Celery. Define schedules in `CELERY_BEAT_SCHEDULE`. Runs as a separate process. At Maitri I used Beat to trigger nightly data ingestion tasks.

---

**Q: What is a visibility timeout in SQS?**
After a worker picks up a message, it's hidden from other workers for the visibility timeout (default 30s). If the worker doesn't delete it before timeout, the message becomes visible again and another worker picks it up. Set timeout to exceed your max task runtime to avoid duplicate processing.

---

**Q: How do you scale Celery workers?** ⭐
Horizontally: add more worker machines. Per worker: increase `--concurrency` (processes) or use `--pool=gevent` for I/O-bound tasks (many concurrent coroutines per worker). Use dedicated queues + dedicated workers per task type to allocate resources appropriately.

---

**Q: What is the prefetch multiplier in Celery?**
Controls how many tasks a worker fetches at once. Default is 4 — worker fetches 4 tasks before processing any. For long-running tasks, set `worker_prefetch_multiplier=1` so each worker holds only one task at a time — prevents one slow worker from hoarding tasks.

---

## Advanced

**Q: How do you monitor Celery in production?** 🔥
Flower (web UI for real-time monitoring). Prometheus + Celery metrics exporter for Grafana dashboards. Queue depth monitoring in SQS (CloudWatch) or RabbitMQ management UI. Alert on: queue depth growing (workers can't keep up), task failure rate, task runtime exceeding SLA.

---

**Q: What is the difference between Celery and Kafka?** 🔥 (Senior, data engineering)
Celery: task queue, messages consumed once, ephemeral. Good for distributed task processing.
Kafka: event log, messages retained and replayable, multiple consumer groups can read independently. Good for event streaming, audit trails, fan-out to multiple services.
Use Celery when you need to run a Python function asynchronously. Use Kafka when you need event sourcing, replay, or multiple independent consumers.

---

**Q: How do you handle distributed transactions across services using a message queue?** 🔥 (Microservices, senior)
Saga pattern — break the distributed transaction into local transactions with compensating actions. Choreography: each service publishes events and reacts to others' events. Orchestration: a central coordinator sends commands. For the SLM service I used a simple choreography pattern — extraction results published to SQS, processing service consumed and wrote to DB, if write failed it published a failure event for retry.

---

**Q: What is the outbox pattern?** 🔥 (Senior, microservices)
Prevents dual-write problems (DB write + message publish might not be atomic). Write both the business data and the message to an "outbox" table in the same DB transaction. A separate poller reads the outbox and publishes to the queue. Guarantees at-least-once delivery without distributed transactions.

---

**Q: How would you implement rate limiting on Celery tasks?** (Senior)
Use `celery_throttle` or a Redis-based rate limiter. Set `rate_limit` on the task (`'10/m'` = 10 per minute). Use token bucket in Redis for finer control. Needed when downstream APIs have rate limits (e.g. calling an LLM API at most N calls/minute).

---

**Q: What happens when a Celery worker runs out of memory?**
The worker process is killed by the OS (OOM killer). Unacknowledged tasks return to the queue (if `ack_late=True`). Use `worker_max_memory_per_child` to restart workers after they use too much memory — prevents memory leaks from accumulating. Monitor worker memory usage in production.

---
