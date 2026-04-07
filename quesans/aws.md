# AWS Interview Questions

> ⭐ = Frequently asked | 🔥 = Trending 2024-25

---

## Core Services

**Q: What is Amazon S3?** ⭐
Object storage — store and retrieve any amount of data as objects (files) in buckets. Highly durable (11 nines), scalable, cheap. Used at Maitri for storing raw medical documents, processed Excel reports, and Airflow DAG outputs. Not a filesystem — no directories, no random writes.

---

**Q: What is the difference between S3 storage classes?**
Standard: frequent access. Standard-IA: infrequent access (cheaper, retrieval fee). Glacier: archival (very cheap, minutes/hours to retrieve). Intelligent-Tiering: auto-moves objects between tiers based on access patterns. Use lifecycle policies to auto-transition old reports to cheaper storage.

---

**Q: What is Amazon SQS?** ⭐
Managed message queue. Standard: at-least-once delivery, best-effort ordering, unlimited throughput. FIFO: exactly-once, strict order, 3000 msg/sec. I used Standard SQS in the SLM service — LLM extraction results queued for post-processing workers.

---

**Q: What is the difference between SQS Standard and FIFO?** ⭐
Standard: higher throughput, at-least-once delivery, ordering not guaranteed. FIFO: exactly-once, strict ordering, max 3000 msg/sec. Use FIFO when order matters (financial transactions) or when duplicates would cause problems. Most use cases work fine with Standard + idempotent consumers.

---

**Q: What is a Dead Letter Queue (DLQ)?** ⭐
A queue where messages go after failing `maxReceiveCount` times. Isolates poison pills from the main queue. Monitor DLQ depth — messages there indicate bugs. Inspect to find root cause, fix, then replay to main queue. Configured this at Maitri with `maxReceiveCount=3`.

---

**Q: What is visibility timeout in SQS?**
After a consumer reads a message, it's hidden for the visibility timeout duration. If the consumer doesn't delete it before timeout, the message reappears for another consumer. Set to more than your max processing time to avoid unintended re-processing.

---

**Q: What is Amazon EC2?** ⭐
Virtual servers in the cloud. You choose instance type (CPU, RAM, network), OS, and storage. Pay per hour or per second. Scale by adding instances (horizontal). Celery workers, Airflow, and application servers often run on EC2.

---

**Q: What is the difference between EC2 instance types?**
- **t3/t4g**: burstable — good for variable workloads (web servers, light workers)
- **c5/c6**: compute-optimized — CPU-intensive (ML inference, encoding)
- **r5/r6**: memory-optimized — large datasets in memory (in-memory DBs, big analytics)
- **p3/p4**: GPU — ML training

---

**Q: What is AWS Lambda?** ⭐ 🔥
Serverless compute — run code in response to events without managing servers. Scales to zero (no idle cost), scales up automatically. Cold start latency is the main downside. Good for: API backends, S3 event triggers, cron jobs, webhook handlers.

---

**Q: What is the difference between Lambda and EC2?**
Lambda: stateless, event-driven, auto-scales to zero, 15-min max runtime, pay per invocation. EC2: persistent, full control, long-running processes, pay per hour. For short-lived event-driven tasks: Lambda. For long-running workers (Celery): EC2.

---

**Q: What is Amazon RDS?**
Managed relational database service. Handles backups, patching, multi-AZ failover. Supports PostgreSQL, MySQL, Oracle. Reduces ops burden vs self-managed DB on EC2. Use RDS for application databases; use Redshift for analytics/data warehouse.

---

**Q: What is AWS IAM?** ⭐
Identity and Access Management — controls who (users, roles, services) can do what on which AWS resources. Principle of least privilege: grant only the permissions needed. EC2 instances use IAM roles to access S3 or SQS without hardcoding credentials.

---

**Q: What is an IAM role vs an IAM user?**
User: long-lived credentials (access key + secret) for a person or app. Role: temporary credentials assumed by services, Lambda, EC2, or cross-account access. Prefer roles over users — credentials rotate automatically, no secrets to manage.

---

**Q: What is AWS Secrets Manager?** ⭐
Stores credentials (DB passwords, API keys) encrypted. Supports automatic rotation. Better than environment variables — no secret in code or config files, full audit log, access control via IAM. Retrieve at startup using AWS SDK.

---

**Q: What is the difference between Secrets Manager and Parameter Store?**
Secrets Manager: built for secrets — encryption, auto-rotation, higher cost. Parameter Store (SSM): general config store — free tier for standard parameters, supports encryption. Use Secrets Manager for DB passwords and API keys. Use Parameter Store for non-secret config.

---

## Networking

**Q: What is a VPC?** ⭐
Virtual Private Cloud — your own isolated network within AWS. Contains subnets, route tables, internet gateways, NAT gateways. Production resources go in private subnets (no direct internet access). Load balancers and bastion hosts go in public subnets.

---

**Q: What is the difference between a public and private subnet?**
Public subnet: has a route to an Internet Gateway — resources can have public IPs. Private subnet: no direct internet route — uses NAT Gateway for outbound traffic only. DB and app servers go in private subnets for security.

---

**Q: What is a security group?** ⭐
Virtual firewall for EC2 instances/RDS. Stateful — return traffic is automatically allowed. Rules: allow specific ports from specific IPs or other security groups. DB security group: allow 5432 only from app server security group.

---

**Q: What is AWS CloudWatch?** ⭐
Monitoring and observability service. Collects logs, metrics, and events. Set alarms on metrics (CPU > 80%, SQS queue depth > 1000, DLQ depth > 0). Trigger notifications (SNS → email/Slack) or auto-scaling on alarms.

---

## Architecture

**Q: What is an Application Load Balancer (ALB)?** ⭐
Layer 7 load balancer — routes HTTP/HTTPS traffic to EC2, containers, or Lambda based on URL path, headers, or host. Handles SSL termination. Health checks route traffic away from unhealthy instances. Integrates with Auto Scaling.

---

**Q: What is Auto Scaling?** ⭐
Automatically adds or removes EC2 instances based on CloudWatch metrics (CPU, SQS queue depth, custom metrics). Scale out on load, scale in when idle. Define min/max/desired instance count. Essential for cost optimization and handling traffic spikes.

---

**Q: What is S3 event notification?** 🔥
S3 can trigger events when objects are created/deleted. Routes to SQS, SNS, or Lambda. Common pattern: file uploaded to S3 → SQS message → worker processes it. Used in document processing pipelines.

---

**Q: What is the difference between SNS and SQS?** ⭐
SNS: pub/sub — one message, multiple subscribers (email, Lambda, SQS, HTTP). Fan-out pattern. SQS: queue — one consumer group processes each message once. SNS + SQS together: SNS fans out to multiple SQS queues, each consumed by different services.

---

**Q: How do you secure an S3 bucket?** ⭐
1. Block all public access (AWS setting)
2. Bucket policy: deny access except from specific IAM roles
3. Enable versioning (recover deleted files)
4. Enable encryption (SSE-S3 or SSE-KMS)
5. Enable access logging
6. Never make a bucket public unless it's intentionally a CDN origin

---

**Q: What is CloudFront?** 🔥
AWS CDN — caches content at edge locations globally, reduces latency. For a portfolio site: CloudFront in front of S3 serves HTML/CSS/JS from the edge nearest to the user. Also handles SSL certificate management via AWS Certificate Manager.

---
