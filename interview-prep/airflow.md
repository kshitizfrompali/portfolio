# Apache Airflow Interview Questions

> ⭐ = Frequently asked | 🔥 = Trending 2024-25 | 🏢 = Reported at specific companies

---

## Basic

**Q: What is Apache Airflow?** ⭐
A workflow orchestration platform. You define pipelines as DAGs (Directed Acyclic Graphs) in Python. Airflow handles scheduling, dependency management, retries, logging, and monitoring. Used for ETL, ML training pipelines, report generation, and data ingestion.

---

**Q: What is a DAG?** ⭐
Directed Acyclic Graph — a workflow definition. Nodes = tasks. Directed edges = dependencies (task A must finish before task B). Acyclic = no circular dependencies. The DAG itself contains no business logic — tasks do the work.

---

**Q: What is a task in Airflow?**
A single unit of work. Implemented as an Operator (PythonOperator, BashOperator, SQLExecuteQueryOperator, etc.). Each task runs independently, can be retried, and has its own log.

---

**Q: What is the Airflow Scheduler?**
The scheduler reads DAG files, determines which tasks are ready to run (dependencies met, schedule time reached), and queues them for the Executor. Runs continuously in the background.

---

**Q: What is a DAG run?**
An instantiation of a DAG at a specific `execution_date`. Each scheduled run is a separate DAG run. Multiple DAG runs can run concurrently (controlled by `max_active_runs`).

---

**Q: What is `execution_date` in Airflow?**
The logical date the DAG run represents — not necessarily when it runs. For a daily DAG, the execution_date is the start of the interval. A DAG scheduled for 2025-01-01 runs at the end of that day (or start of the next), with execution_date = 2025-01-01. Important for idempotent logic.

---

**Q: What Operators have you used?**
- `PythonOperator`: run a Python callable
- `BashOperator`: run a shell command
- `SQLExecuteQueryOperator`: run SQL on a DB
- `S3ToRedshiftOperator`: load from S3
- Custom operators for business-specific tasks (Google Sheets updates, chat notifications)

---

## Intermediate

**Q: How do you pass data between tasks in Airflow?** ⭐
XCom (cross-communication). Tasks push values with `ti.xcom_push(key, value)`, downstream tasks pull with `ti.xcom_pull(task_ids, key)`. For large data, never put data in XCom — store in S3/DB and pass only the reference key. XCom data is stored in the Airflow metadata DB, which has size limits.

---

**Q: What is a dynamic DAG?** ⭐ (Data engineering roles)
A DAG generated programmatically — e.g. one DAG per client or per dataset. Loop over a config, create DAG objects. At Maitri I replaced 12 near-identical billing DAGs with a factory that generated per-organization DAGs from YAML config, reducing code by 90%.

```python
for org in load_org_config():
    dag_id = f"billing__{org['id']}"
    globals()[dag_id] = create_billing_dag(org)
```

---

**Q: What is the difference between `schedule_interval` and `timetable`?** 🔥
`schedule_interval` is a cron string or timedelta. `timetable` (Airflow 2.2+) is a plugin-based scheduling abstraction — supports custom schedules like "business days only" or "first Monday of month". Prefer timetables for complex schedules.

---

**Q: How do you handle failures and alerts in Airflow?** ⭐
Per-task: `retries`, `retry_delay`, `on_failure_callback`. Per-DAG: `on_failure_callback`, `sla_miss_callback`. I built Google Chat webhook notifications as failure callbacks — on-call gets an immediate alert with the task name, DAG, and error message when a billing pipeline fails.

---

**Q: What are Airflow sensors?**
A type of operator that waits for a condition to be true before proceeding. `S3KeySensor` waits for a file in S3. `ExternalTaskSensor` waits for another DAG's task. `SqlSensor` waits for a DB condition. Use `poke_interval` and `timeout` to avoid blocking workers indefinitely — or use `mode='reschedule'` to release the worker slot while waiting.

---

**Q: What is the difference between `poke` and `reschedule` mode in sensors?**
`poke` (default): worker slot held continuously while polling. `reschedule`: worker slot released between polls, slot reacquired to check. Use `reschedule` for long-wait sensors to avoid consuming worker slots unnecessarily.

---

**Q: What are Airflow Connections and Variables?**
**Connections**: stored credentials for external systems (DB, S3, APIs) — referenced in operators by `conn_id`. **Variables**: global key-value config stored in Airflow UI/DB. Use Variables for config that changes across environments (URLs, thresholds) without touching code.

---

**Q: What is the Airflow metadata database?**
PostgreSQL (or MySQL) database where Airflow stores DAG runs, task instances, XComs, connections, variables, logs metadata. Should be separate from your application DB. Never use SQLite in production — it doesn't support concurrent writes.

---

**Q: What is `max_active_runs` and `max_active_tasks`?**
`max_active_runs`: how many DAG runs can be active simultaneously. `max_active_tasks`: how many tasks across all runs can run at once. Used to prevent overloading downstream systems.

---

**Q: What is a SubDAG and why is it generally discouraged?** 🔥
SubDAGs group tasks into a nested DAG for reuse. Discouraged because they create deadlocks (SubDAG occupies a worker slot while its tasks also need slots), are complex to debug, and have known bugs. Use `TaskGroup` instead for visual grouping.

---

**Q: What is TaskGroup and how does it differ from SubDAG?** 🔥
`TaskGroup` is a UI grouping mechanism — doesn't create a nested DAG, no extra worker slots, no deadlock risk. Just a visual organizer in the Graph view. Preferred over SubDAGs in Airflow 2.x.

---

## Advanced

**Q: What is the CeleryExecutor and how does it scale?** ⭐
CeleryExecutor uses a Celery worker pool to run tasks. Workers pull tasks from a broker (RabbitMQ, Redis). Scale by adding more worker machines — each runs `airflow celery worker`. Used in production at Maitri to handle concurrent multi-org billing DAGs.

---

**Q: What is the KubernetesExecutor?** 🔥 (Cloud-native data teams)
Spins up a Kubernetes pod per task, then terminates it. Perfect isolation — each task gets its own environment and resources. No idle workers sitting around. Slower to start (pod startup latency) but scales to zero. Preferred for bursty, heterogeneous workloads.

---

**Q: How do you make an Airflow DAG idempotent?** ⭐ (Senior, data engineering)
Every task should produce the same result if re-run with the same `execution_date`. Use upserts (`INSERT ... ON CONFLICT`) instead of inserts. Check if output already exists before computing. Use `execution_date` as partition key when writing to storage. In billing DAGs I check S3 for existing output before regenerating.

---

**Q: What is data-aware scheduling in Airflow 2.4+?** 🔥
Datasets — a task can declare what data it produces and what data it consumes. A DAG can be triggered when a dataset is updated by another DAG, rather than on a time schedule. Decouples pipelines and reduces latency compared to sensor polling.

---

**Q: How do you test Airflow DAGs?** 🔥
1. **Import test**: `from my_dag import dag` — catches syntax errors
2. **DAG integrity test**: assert no cycles, all tasks exist
3. **Unit test operators**: test the Python callable in isolation
4. **Integration test**: use `airflow dags test dag_id execution_date` to run locally

```python
def test_dag_loads():
    from my_dag import dag
    assert dag is not None
    assert len(dag.tasks) == 5
```

---

**Q: What is Airflow's backfill feature?**
Runs a DAG for historical dates that were missed or need reprocessing. `airflow dags backfill dag_id --start-date 2025-01-01 --end-date 2025-01-31`. Requires DAGs to be idempotent. Be careful with `max_active_runs` to avoid overwhelming downstream systems.

---

**Q: How do you manage Airflow DAG versioning?**
Store DAGs in git. Use CI/CD to sync the DAG folder to Airflow workers on merge. Tag DAG IDs with version if you need to run old and new simultaneously. Carefully manage in-flight runs before deploying breaking changes.

---

**Q: What causes Airflow scheduler lag and how do you fix it?** (Senior/platform)
Scheduler parses all DAG files continuously. Large number of DAGs or complex files slow parsing. Fixes: use `dag_discovery_safe_mode=False`, reduce file parsing parallelism, split large DAG files, avoid expensive imports at module level in DAG files (import inside functions/callables instead).

---
