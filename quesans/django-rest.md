# Django & REST API Interview Questions

> ⭐ = Frequently asked | 🔥 = Trending 2024-25 | 🏢 = Reported at specific companies

---

## Basic

**Q: What is Django and what problem does it solve?**
Django is a Python web framework following the MVT pattern (Model-View-Template). It provides ORM, admin, authentication, URL routing, and form handling out of the box. Lets you ship a database-backed web app quickly without wiring everything yourself.

---

**Q: What is the difference between Django and Flask?**
Django is full-featured and opinionated — ORM, admin, auth included. Flask is a micro-framework — minimal core, you add what you need. Use Django for data-heavy apps with DB models. Use Flask (or FastAPI) for APIs where you want full control.

---

**Q: Explain Django's MVT pattern.**
Model: DB layer (ORM). View: business logic, handles request/response. Template: HTML rendering. In DRF the Template layer is replaced by Serializers (JSON output).

---

**Q: What is Django's ORM?** ⭐
Object-Relational Mapper — maps Python classes to DB tables. You write Python to query data instead of SQL. Generates parameterized SQL automatically (prevents injection). Supports PostgreSQL, MySQL, SQLite.

---

**Q: What is a Django migration?** ⭐
A migration is a versioned file that records schema changes (create table, add column, etc.). Django generates them with `makemigrations` and applies with `migrate`. They're committed to git so the whole team's DB stays in sync.

---

**Q: What is the difference between `null=True` and `blank=True` in a model field?**
`null=True`: DB column allows NULL. `blank=True`: Django form validation allows empty string. For strings, prefer `blank=True` without `null=True` (use empty string as "not set"). For non-string fields (int, date), use `null=True` when optional.

---

**Q: What is a ForeignKey and how does Django handle it?**
ForeignKey creates a many-to-one relationship. Django adds a `_id` column to the DB and generates a SQL constraint. Access the related object with `instance.related_field` (lazy load) or `select_related` (join).

---

**Q: What are Django signals?**
Signals let decoupled parts of the app react to events (e.g. `post_save`, `pre_delete`). A signal sender fires, registered receivers run. Useful but easy to overuse — makes code flow hard to trace. Prefer explicit function calls for critical logic.

---

## Intermediate

**Q: What is `select_related` vs `prefetch_related`?** ⭐ (common Django interview)
`select_related`: SQL JOIN, fetches ForeignKey/OneToOne in one query.
`prefetch_related`: separate queries, joins in Python — for ManyToMany or reverse FKs.
Wrong choice = N+1 queries. At Insight Workshop I fixed a slow endpoint by replacing `prefetch_related` with `select_related` on a ForeignKey, cutting queries from 101 to 1.

---

**Q: What is the N+1 problem?** ⭐
Fetching a list of objects then making one DB query per object in a loop. 100 objects = 101 queries. Fix with `select_related`, `prefetch_related`, or rewriting as a single queryset.

```python
# BAD
patients = Patient.objects.all()
for p in patients:
    print(p.organization.name)  # 1 query per patient

# GOOD
patients = Patient.objects.select_related('organization')
```

---

**Q: How does Django REST Framework work?** ⭐
DRF extends Django with serializers (convert models to JSON), ViewSets (CRUD views), Routers (auto URL generation), and authentication/permission classes. You define a ModelSerializer, a ViewSet, register with a Router, and you have a full REST API.

---

**Q: What is a DRF Serializer and what does it do?** ⭐
Serializers convert complex data (querysets, model instances) to Python dicts for JSON rendering, and validate incoming JSON data back to Python objects. `ModelSerializer` auto-generates fields from a model.

---

**Q: What is the difference between `APIView` and `ViewSet` in DRF?**
`APIView`: manual, you write `get()`, `post()` etc. Full control. `ViewSet`: groups CRUD actions, works with Routers for auto-URL generation. `ModelViewSet` gives full CRUD with almost no code.

---

**Q: How does DRF authentication work?** ⭐ (startups, SaaS companies)
Authentication classes identify the user (JWT, session, token, API key). Permission classes decide if the user can do the action. Set globally in `settings.py` or per-view. I used JWT (`djangorestframework-simplejwt`) with custom permission classes for RBAC.

---

**Q: How would you implement role-based access control in DRF?** ⭐
Store roles in DB. Create a custom `BasePermission` that loads the user's roles and checks against an action→role mapping. At Insight Workshop I built this: roles in a `Role` model, users linked via ManyToMany, a permission class checked `request.user.roles.filter(name__in=allowed_roles).exists()`.

---

**Q: What is Django's `transaction.atomic()`?** ⭐
Wraps a block in a DB transaction. If anything inside raises an exception, the whole block rolls back. Use when multiple DB writes must succeed or fail together. In the coding platform, writing LLM results touched three tables — wrapped in `atomic()` to prevent partial writes.

---

**Q: What is `defer()` and `only()` in Django ORM?**
`only('name', 'email')` loads only specified columns. `defer('large_text_field')` loads everything except specified columns. Reduces data transfer for wide tables with large text/blob columns.

---

**Q: How does Django handle database connection pooling?**
Django opens a new connection per thread by default. `CONN_MAX_AGE` keeps connections open across requests. For true pooling use PgBouncer at the infrastructure level or `django-db-geventpool` for async setups.

---

**Q: What is `django-tenants` and how does it achieve tenant isolation?** 🔥
`django-tenants` uses PostgreSQL schemas — each tenant gets its own schema. The middleware reads the subdomain, sets `search_path` to the tenant's schema, so all queries hit only that tenant's tables. Migrations run per-schema. Used this at Maitri for medical data isolation.

---

## Advanced

**Q: How would you optimize a slow Django API endpoint?** ⭐ (Amazon, Stripe, senior roles)
Steps: profile first (Django Debug Toolbar, Silk, or direct query logging). Check for N+1. Add `select_related`/`prefetch_related`. Add DB indexes on filter columns. Use `only()`/`defer()`. Add caching (Redis). For complex aggregations, use raw SQL or materialized views. Move heavy computation to Celery.

---

**Q: What is Django's `Q` object?**
Used for complex queries with OR, AND, NOT conditions.

```python
from django.db.models import Q
Patient.objects.filter(
    Q(status='active') | Q(year=2025)
).exclude(Q(org_id=None))
```

---

**Q: What are Django custom managers and querysets?** ⭐
Managers define the default queryset and add custom query methods. Querysets are chainable. Encapsulate common query logic in the model layer.

```python
class ActivePatientQuerySet(models.QuerySet):
    def for_year(self, year):
        return self.filter(year=year, status='active')

class Patient(models.Model):
    objects = ActivePatientQuerySet.as_manager()
```

---

**Q: How does Django's caching framework work?** 🔥
Django supports multiple cache backends (Redis, Memcached, DB, filesystem). Use `cache.get`/`cache.set` manually, or `@cache_page` for view-level caching, or `cache_control` headers. For per-object caching I use a cache key pattern like `patient:{id}:profile` with a TTL that matches data freshness requirements.

---

**Q: What is `F()` expression in Django ORM?**
Lets you reference a field value in a query without loading it into Python — the operation happens in SQL. Useful for atomic increments and avoiding race conditions.

```python
# Atomic increment without race condition
Patient.objects.filter(id=pid).update(retry_count=F('retry_count') + 1)
```

---

**Q: What is `prefetch_related` with `Prefetch` object?**
`Prefetch` lets you customize the queryset used in prefetching — add filters, order, or store under a custom attribute name.

```python
from django.db.models import Prefetch

patients = Patient.objects.prefetch_related(
    Prefetch('hcc_codes', queryset=HCCCode.objects.filter(year=2025), to_attr='current_hccs')
)
```

---

**Q: What is the difference between `save()` and `update()` in Django ORM?**
`save()` loads the object, modifies Python, writes all fields — triggers signals and validation. `update()` issues a direct SQL UPDATE — faster, bypasses signals and validation. For bulk updates use `update()`. For single-object business logic use `save()`.

---

**Q: How do you write a custom Django management command?**
Create `management/commands/my_command.py` with a class extending `BaseCommand`. Define `handle()`. Good for one-off data migrations, cron-triggered jobs, and CLI tools for ops.

---

**Q: How would you design a paginated API in DRF?** 🔥 (common for senior roles)
Use DRF's built-in pagination classes: `PageNumberPagination` (page=1&page_size=20), `CursorPagination` (cursor-based, better for large datasets — no OFFSET performance problem). For millions of rows, always use cursor pagination since OFFSET slows as the page number grows.

---

**Q: What is the `ContentType` framework in Django?**
Allows generic relationships — a model can relate to any other model using `content_type` + `object_id`. Django admin uses it for log entries. Useful for notification systems, audit trails, or tags that apply to multiple models.

---
