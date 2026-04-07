# FastAPI & Flask Interview Questions

> ⭐ = Frequently asked | 🔥 = Trending 2024-25

---

## Flask

**Q: What is Flask?** ⭐
A Python micro web framework. Minimal core — routing, request/response, templates. Everything else (auth, ORM, validation) you add yourself. Good for APIs, microservices, and small apps where Django would be overkill.

---

**Q: What is a Flask Blueprint?**
A way to organize a Flask app into modular components. Each blueprint has its own routes, templates, and static files. Registered on the app with a URL prefix. Used to split a growing app into logical modules (auth, patients, billing).

---

**Q: How does Flask handle request context?**
Flask uses context locals (`g`, `request`, `session`) that are thread-local (or greenlet-local with gevent). `request` contains incoming request data. `g` is a scratch space for per-request data (e.g. current user). Automatically set up when a request enters and torn down after.

---

**Q: What is Flask-SQLAlchemy vs Django ORM?**
Flask-SQLAlchemy wraps SQLAlchemy — more explicit, more powerful, but more verbose. Django ORM is tightly integrated with Django — less flexible but easier to use with migrations and admin. For Flask services I prefer SQLAlchemy directly (or SQLModel for Pydantic integration).

---

**Q: How do you handle errors in Flask?**
Register error handlers with `@app.errorhandler(code)`. Return JSON for APIs. Always handle 400 (bad request), 404 (not found), 500 (server error). In production, log the exception and return a sanitized error message — never leak stack traces.

```python
@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': str(e)}), 400
```

---

**Q: What is Flask's application factory pattern?**
Creating the Flask app inside a function (`create_app()`) rather than at module level. Allows creating multiple app instances (e.g. for testing with different configs). Used in larger Flask projects to avoid circular imports.

---

## FastAPI

**Q: What is FastAPI and why is it popular?** ⭐ 🔥
FastAPI is a modern Python web framework built on Starlette (async) and Pydantic (validation). Key features: automatic request/response validation via type hints, auto-generated OpenAPI docs, async support, very high performance (comparable to Node.js). Most popular choice for new Python APIs in 2024-25.

---

**Q: What is the difference between Flask and FastAPI?** ⭐ 🔥
FastAPI: async-first, automatic validation/serialization via Pydantic, built-in OpenAPI docs, dependency injection system. Flask: sync by default (async with extensions), more mature ecosystem, no built-in validation. For new APIs, FastAPI is the better default. For existing Flask projects, migration is straightforward.

---

**Q: How does FastAPI use Pydantic for validation?** ⭐
Type hint request bodies with Pydantic models. FastAPI automatically validates incoming JSON, returns 422 with error details on invalid input, and serializes response models. Zero boilerplate.

```python
from pydantic import BaseModel

class PatientCreate(BaseModel):
    patient_id: int
    year: int
    hcc_code: str

@app.post("/patients")
async def create_patient(patient: PatientCreate):
    # patient is already validated
    return {"id": patient.patient_id}
```

---

**Q: What is FastAPI's dependency injection?** 🔥
FastAPI's `Depends()` injects dependencies into route handlers — DB sessions, auth, config. Dependencies can depend on other dependencies. Scoped per request — automatically cleaned up.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/patients/{pid}")
async def get_patient(pid: int, db: Session = Depends(get_db)):
    return db.query(Patient).get(pid)
```

---

**Q: What is the difference between `async def` and `def` in FastAPI?** 🔥
`async def`: non-blocking, runs in the event loop — use when making async I/O calls (httpx, databases, async ORMs). `def`: runs in a thread pool — FastAPI handles this automatically. If you use `def` with sync libraries (like SQLAlchemy sync), FastAPI offloads it to a thread pool so it doesn't block the event loop.

---

**Q: What is background tasks in FastAPI?**
`BackgroundTasks` lets you run tasks after returning a response — without blocking the client. Good for sending emails, logging, or triggering async jobs. For heavier work, use Celery instead.

```python
@app.post("/extract")
async def trigger_extraction(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_extraction, payload)
    return {"status": "queued"}
```

---

**Q: How does FastAPI generate API documentation?**
Automatically generates OpenAPI (Swagger) at `/docs` and ReDoc at `/redoc` from your route definitions, Pydantic models, and type hints. No extra code needed. Extremely useful for API consumers and testing.

---

**Q: What is path vs query vs body parameters in FastAPI?**
Path: `@app.get("/patients/{patient_id}")` — in the URL. Query: `?year=2025` — appended to URL, optional with defaults. Body: Pydantic model as function argument — JSON request body. FastAPI infers which is which from position and type hints.

---

**Q: How do you handle authentication in FastAPI?** ⭐ 🔥
OAuth2 with JWT using `OAuth2PasswordBearer`. FastAPI provides security schemes that integrate with OpenAPI docs. Dependency injection makes it clean — one `get_current_user` dependency used across all protected routes.

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY)
    return payload
```

---

**Q: What is CORS and how do you configure it in FastAPI/Flask?** ⭐
Cross-Origin Resource Sharing — browser security policy that blocks requests from a different origin. Configure allowed origins, methods, and headers on the server.

FastAPI:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["https://myapp.com"])
```

---

**Q: How do you write tests for a FastAPI app?** 🔥
Use `TestClient` (synchronous wrapper around the async app). Works with pytest.

```python
from fastapi.testclient import TestClient
client = TestClient(app)

def test_create_patient():
    response = client.post("/patients", json={"patient_id": 1, "year": 2025, "hcc_code": "HCC19"})
    assert response.status_code == 200
```

---

**Q: What is the difference between FastAPI and Django REST Framework?** 🔥
DRF: mature, Django ecosystem, more conventions, good for complex Django projects. FastAPI: modern, async-first, automatic validation, OpenAPI docs, better performance, less boilerplate. Choose DRF if already on Django. Choose FastAPI for new projects, microservices, or ML APIs.

---
