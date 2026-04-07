# PostgreSQL & Database Interview Questions

> ⭐ = Frequently asked | 🔥 = Trending 2024-25 | 🏢 = Reported at specific companies

---

## Basic

**Q: What is the difference between SQL and NoSQL databases?**
SQL: structured, fixed schema, ACID transactions, relational. Good for complex queries and data integrity. NoSQL: flexible schema, horizontal scaling, various models (document, key-value, graph). Good for high write volume, unstructured data. PostgreSQL is SQL; MongoDB is NoSQL. For medical data with complex relationships, SQL is the right choice.

---

**Q: What are the ACID properties?** ⭐
- **Atomicity**: transaction is all-or-nothing
- **Consistency**: DB moves from one valid state to another
- **Isolation**: concurrent transactions don't interfere
- **Durability**: committed data survives crashes

---

**Q: What is the difference between `WHERE` and `HAVING`?**
`WHERE` filters rows before grouping. `HAVING` filters groups after `GROUP BY`. You can't use aggregates in `WHERE`.

```sql
-- HAVING: filter groups
SELECT org_id, COUNT(*) as patient_count
FROM patients
GROUP BY org_id
HAVING COUNT(*) > 100;
```

---

**Q: What is an index?** ⭐
A data structure (usually B-tree) that speeds up lookups by avoiding full table scans. Trade-off: faster reads, slower writes (index must be updated). Add indexes on columns used in WHERE, JOIN, and ORDER BY.

---

**Q: What is the difference between `INNER JOIN`, `LEFT JOIN`, and `FULL OUTER JOIN`?** ⭐
- **INNER JOIN**: rows that match in both tables
- **LEFT JOIN**: all rows from left table, matched rows from right (NULL if no match)
- **FULL OUTER JOIN**: all rows from both tables, NULLs where no match

---

**Q: What is a primary key vs a foreign key?**
Primary key: unique identifier for a row, cannot be NULL. Foreign key: references the primary key of another table, enforces referential integrity. Prevents orphan records.

---

**Q: What is `EXPLAIN` and `EXPLAIN ANALYZE`?** ⭐
`EXPLAIN` shows the query plan PostgreSQL will use. `EXPLAIN ANALYZE` actually runs the query and shows real execution times. Use these to diagnose slow queries — look for sequential scans on large tables (should be index scans).

---

**Q: What is a database view?**
A virtual table defined by a SQL query. Doesn't store data (unless materialized). Simplifies complex queries, provides abstraction. You can query a view like a table.

---

## Intermediate

**Q: What is a database transaction and why does it matter?** ⭐
A transaction groups operations so they all succeed or all roll back. Prevents partial writes corrupting data. In the medical coding platform, writing LLM results to three tables was wrapped in one transaction — if one write failed, all rolled back.

---

**Q: What is the N+1 query problem at the DB level?** ⭐ (very common)
Executing one query to get a list, then one query per row. 100 rows = 101 queries. Fix by joining or using `IN`.

```sql
-- BAD: loop over patients, one query each
SELECT * FROM hcc_codes WHERE patient_id = $1;

-- GOOD: one query
SELECT * FROM hcc_codes WHERE patient_id IN (1, 2, 3, ...);
```

---

**Q: What is a composite index and when do you use it?** ⭐
An index on multiple columns. Useful when you always filter on a combination of columns. Column order matters — the index is usable for prefix queries.

```sql
-- Supports: filter by patient_id alone, or patient_id + year
CREATE INDEX idx_patient_year ON hcc_extractions(patient_id, year);
```

---

**Q: What is a partial index?** 🔥
An index with a WHERE clause — only indexes rows matching the condition. Smaller and faster than a full index when you query a subset frequently.

```sql
-- Only index active records
CREATE INDEX idx_active_patients ON patients(org_id) WHERE status = 'active';
```

---

**Q: What is the difference between a materialized view and a regular view?** ⭐
Regular view: runs the query every time. Materialized view: stores the result — fast reads, but data can be stale. Refresh with `REFRESH MATERIALIZED VIEW`. I used this at Maitri for billing summaries — expensive join query, refreshed nightly by Airflow, reduced dashboard load from 8s to 200ms.

---

**Q: What is `VACUUM` in PostgreSQL?**
PostgreSQL uses MVCC — deleted/updated rows are kept as "dead tuples". VACUUM reclaims space. `AUTOVACUUM` runs automatically. If tables have high churn and autovacuum can't keep up, tables bloat and slow down.

---

**Q: What is connection pooling and why does it matter?** ⭐ (Backend, infrastructure roles)
Creating a DB connection is expensive (TCP handshake, auth). Pooling maintains a pool of open connections reused across requests. Without it, traffic spikes create hundreds of connections and overwhelm PostgreSQL. PgBouncer is the standard PostgreSQL pooler. In Django, `CONN_MAX_AGE` reuses connections per thread.

---

**Q: What is `SELECT FOR UPDATE` and when do you use it?**
Locks selected rows so other transactions can't modify them until yours commits. Used to prevent race conditions when multiple workers process the same record.

```sql
SELECT * FROM tasks WHERE status = 'pending' LIMIT 1 FOR UPDATE SKIP LOCKED;
```
`SKIP LOCKED` means skip rows locked by other workers — perfect for Celery-style task queues.

---

**Q: What is the difference between `DELETE`, `TRUNCATE`, and `DROP`?**
`DELETE`: removes rows matching WHERE, can be rolled back, triggers fire. `TRUNCATE`: removes all rows fast, minimal logging, resets sequences. `DROP`: removes the table entirely. For clearing a table before reload, use `TRUNCATE`.

---

**Q: What are window functions?** ⭐ (Data engineering, analytics roles)
Perform calculations across a set of rows related to the current row, without collapsing rows like `GROUP BY`.

```sql
-- Rank patients by extraction count per org
SELECT patient_id, org_id,
       RANK() OVER (PARTITION BY org_id ORDER BY extraction_count DESC) as rank
FROM patient_stats;
```
Common functions: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, `SUM OVER`.

---

**Q: What is `UPSERT` in PostgreSQL?** ⭐
`INSERT ... ON CONFLICT DO UPDATE` — insert if not exists, update if it does. Idempotent writes — safe to run multiple times.

```sql
INSERT INTO hcc_codes (patient_id, code, year)
VALUES ($1, $2, $3)
ON CONFLICT (patient_id, code, year)
DO UPDATE SET updated_at = NOW();
```

---

**Q: What is a CTE (Common Table Expression)?** 🔥
Named subquery defined with `WITH`. Makes complex queries readable. Can be recursive (tree traversal). PostgreSQL 12+ optimizes CTEs inline.

```sql
WITH active_patients AS (
    SELECT id, org_id FROM patients WHERE status = 'active'
),
hcc_counts AS (
    SELECT patient_id, COUNT(*) as cnt FROM hcc_codes GROUP BY patient_id
)
SELECT p.id, h.cnt
FROM active_patients p
JOIN hcc_counts h ON h.patient_id = p.id;
```

---

## Advanced

**Q: What is MVCC and how does PostgreSQL implement it?** 🔥 (Senior, data engineering)
Multi-Version Concurrency Control — readers don't block writers, writers don't block readers. Each row version has `xmin`/`xmax` (transaction IDs). A query sees a snapshot of data from its start time. Old versions accumulate as dead tuples until VACUUM cleans them.

---

**Q: How do you design a schema for multi-tenancy in PostgreSQL?** ⭐ (SaaS, startups)
Three approaches:
1. **Separate databases**: max isolation, expensive
2. **Separate schemas**: good isolation, used with `django-tenants` — each tenant gets their own schema, `search_path` routes queries
3. **Shared schema with `tenant_id`**: cheapest, but requires every query to filter by `tenant_id` and every index to include it

We used separate schemas at Maitri — strongest isolation for medical data.

---

**Q: What is index bloat and how do you fix it?**
Over time, indexes accumulate dead entries from updates/deletes and grow larger than necessary, slowing queries. Run `REINDEX` to rebuild, or use `pg_repack` for online rebuilds without locking the table.

---

**Q: What is the difference between row-level and statement-level triggers?**
Row-level (`FOR EACH ROW`): fires once per affected row. Statement-level (`FOR EACH STATEMENT`): fires once per SQL statement regardless of rows affected. Row-level is more expensive but gives you access to `OLD` and `NEW` row values.

---

**Q: How does PostgreSQL handle concurrent writes to the same row?** ⭐ (Senior backend)
Last writer wins by default (no automatic conflict detection). Use `SELECT FOR UPDATE` for pessimistic locking. Use optimistic locking with a version column — check the version hasn't changed before updating, retry if it has. Celery's `select_for_update(skip_locked=True)` is the typical pattern for distributed task picking.

---

**Q: What are PostgreSQL's isolation levels?** 🔥
- **Read Committed** (default): sees committed data at the time of each statement
- **Repeatable Read**: sees data as of transaction start, prevents non-repeatable reads
- **Serializable**: full serialization, prevents phantom reads, slowest

For most web apps, Read Committed is fine. For financial calculations or audit trails, use Serializable.

---

**Q: How would you handle a large table (100M+ rows) without downtime for adding an index?** (DevOps, senior)
`CREATE INDEX CONCURRENTLY` builds the index without locking the table for writes. Takes longer but doesn't block production traffic. Never run plain `CREATE INDEX` on large tables in production.

---

**Q: What is table partitioning and when do you use it?** 🔥 (Data engineering)
Splitting a large table into smaller physical partitions based on a key (date, range, hash). PostgreSQL 10+ supports declarative partitioning. Queries touching one partition skip others (partition pruning). At Maitri, a patient extraction table was partitioned by year — queries for 2025 data only scan the 2025 partition.

```sql
CREATE TABLE extractions (
    id BIGSERIAL,
    patient_id INT,
    year INT,
    created_at TIMESTAMP
) PARTITION BY RANGE (year);

CREATE TABLE extractions_2025 PARTITION OF extractions
    FOR VALUES FROM (2025) TO (2026);
```

---
