# Python Interview Questions

> ⭐ = Frequently asked at top companies | 🔥 = Trending in 2024-25 interviews

---

## Basic

**Q: What are Python's built-in data types?**
int, float, str, bool, list, tuple, dict, set, frozenset, bytes, NoneType.

---

**Q: What is the difference between a list and a tuple?** ⭐
List is mutable (can change after creation), tuple is immutable. Tuples are faster and hashable (can be dict keys or set members). Use tuples for fixed data like coordinates or DB rows, lists for collections you'll modify.

---

**Q: What is a dictionary and how does lookup work?**
A dict is a hash map. Lookup is O(1) average — the key is hashed to find the bucket. Worst case O(n) on hash collisions (rare in practice).

---

**Q: What is the difference between `==` and `is`?**
`==` checks value equality. `is` checks identity (same object in memory). `None` checks should always use `is None`, not `== None`.

---

**Q: What are `*args` and `**kwargs`?**
`*args` captures extra positional arguments as a tuple. `**kwargs` captures extra keyword arguments as a dict. Useful for writing flexible APIs and decorators.

```python
def log(level, *args, **kwargs):
    print(f"[{level}]", *args, kwargs)
```

---

**Q: What is a list comprehension? When should you not use one?**
Concise syntax for building lists: `[x*2 for x in range(10) if x % 2 == 0]`. Avoid when the logic is complex enough that a regular loop is clearer — readability trumps brevity.

---

**Q: What is the difference between `append` and `extend` on a list?**
`append` adds one item (even if it's a list). `extend` iterates the argument and adds each element.

```python
a = [1, 2]
a.append([3, 4])   # [1, 2, [3, 4]]
a.extend([3, 4])   # [1, 2, 3, 4]
```

---

**Q: How does Python manage memory?**
Reference counting + cyclic garbage collector. When an object's reference count hits zero it's freed. The `gc` module handles reference cycles. Memory for small ints (-5 to 256) and short strings is interned (cached).

---

**Q: What is the difference between `deepcopy` and `copy`?** ⭐
`copy.copy()` shallow copy — nested objects still share memory. `copy.deepcopy()` recursively copies everything. Bug-prone when using shallow copy on dicts with nested lists.

---

**Q: What are Python's scope rules (LEGB)?**
Local → Enclosing → Global → Built-in. Python searches in that order when resolving a name. `global` and `nonlocal` keywords override this.

---

## Intermediate

**Q: What is a decorator and how does it work?** ⭐ (Google, Amazon, Stripe)
A decorator is a function that wraps another function to add behavior. It takes a function, returns a modified function. `@functools.wraps` preserves metadata.

```python
import functools

def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == times - 1:
                        raise
        return wrapper
    return decorator
```

---

**Q: What is a generator and how does it differ from a list?** ⭐
Generators produce values lazily using `yield` — only one value in memory at a time. Lists materialize everything. Use generators for large datasets or infinite sequences.

```python
def stream_batches(data, size):
    for i in range(0, len(data), size):
        yield data[i:i+size]
```

---

**Q: What is the difference between `@staticmethod` and `@classmethod`?**
`@staticmethod`: no access to class or instance. `@classmethod`: receives class (`cls`) as first arg — useful for factory methods.

```python
class Patient:
    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['name'])

    @staticmethod
    def validate_id(pid):
        return isinstance(pid, int) and pid > 0
```

---

**Q: What is Python's GIL and when does it matter?** ⭐ (Meta, Netflix)
Global Interpreter Lock — only one thread runs Python bytecode at a time. For CPU-bound tasks (image processing, heavy computation) threads don't give real parallelism — use `multiprocessing`. For I/O-bound tasks (DB, network, queues) threads work fine because GIL is released during I/O waits. Celery workers are I/O-bound so GIL isn't a bottleneck.

---

**Q: What is `asyncio` and when would you use it?** 🔥 (FastAPI, Stripe, startups)
`asyncio` is Python's async concurrency model using an event loop. `async def` + `await` for coroutines. Best for I/O-bound work with many concurrent connections (web servers, WebSockets). FastAPI is built on it. Don't use it for CPU-bound work — still blocked by GIL.

```python
async def fetch_patient(session, pid):
    async with session.get(f"/patients/{pid}") as resp:
        return await resp.json()
```

---

**Q: Explain context managers and the `with` statement.** ⭐
Context managers handle setup and teardown via `__enter__` and `__exit__`. Used for file handles, DB connections, locks. You can write your own with `contextlib.contextmanager`.

```python
from contextlib import contextmanager

@contextmanager
def db_transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
```

---

**Q: What is `functools.lru_cache` and when would you use it?** 🔥
Memoization decorator — caches return values by input arguments. Good for expensive pure functions called with the same args repeatedly.

```python
@functools.lru_cache(maxsize=128)
def get_hcc_description(code):
    return db.query(HCC).filter_by(code=code).first()
```

---

**Q: What is the difference between a module and a package?**
A module is a single `.py` file. A package is a directory with `__init__.py` that groups modules. Packages can be nested. Used to organize code by domain.

---

**Q: What is `__init__.py` and is it required?**
It marks a directory as a package and runs on import. In Python 3.3+ it's not required (namespace packages), but still needed for proper package behavior and init logic.

---

**Q: What is monkey patching and why is it risky?**
Replacing or modifying code at runtime (e.g. replacing a class method). Useful in tests (mocking), dangerous in production — hides real code flow, causes unexpected behavior when multiple patches conflict.

---

**Q: What are Python's dunder (magic) methods?** ⭐
Special methods with double underscores: `__init__`, `__str__`, `__repr__`, `__len__`, `__eq__`, `__hash__`, `__enter__`, `__exit__`, `__iter__`, `__next__`. Used to define how objects behave with built-in operations.

---

**Q: What is the difference between `__str__` and `__repr__`?**
`__str__` is the human-readable string (used by `print`). `__repr__` is the developer-facing representation (used in REPL, logs). `__repr__` should ideally return something that can recreate the object.

---

## Advanced

**Q: What is a metaclass?** (Google, Senior-level)
A metaclass is the class of a class. It controls how classes are created. `type` is the default metaclass. Django's ORM uses metaclasses to register model fields automatically when a class is defined.

---

**Q: How does Python's garbage collector handle reference cycles?** 🔥
Reference counting can't handle cycles (A → B → A). Python's `gc` module uses mark-and-sweep to detect and clean cycles. Runs periodically or can be triggered with `gc.collect()`. Objects with `__del__` in cycles were problematic before Python 3.4 (fixed in PEP 442).

---

**Q: What is the descriptor protocol?** (Senior, Django internals)
Descriptors implement `__get__`, `__set__`, `__delete__`. Used by Django ORM to define model fields, `property`, `classmethod`, `staticmethod`. When you access `model.field`, Django's field descriptor intercepts it and returns the column value.

---

**Q: What is `__slots__` and when should you use it?**
`__slots__` restricts instance attributes to a fixed set, skipping the per-instance `__dict__`. Reduces memory by ~40% for objects with many instances (e.g. data transfer objects, dataclass alternatives).

```python
class HCCCode:
    __slots__ = ['code', 'description', 'year']
    def __init__(self, code, description, year):
        self.code = code
        self.description = description
        self.year = year
```

---

**Q: How does Python's import system work?** ⭐
`import` searches `sys.modules` first (cache). If not found, searches `sys.path` (current dir, PYTHONPATH, site-packages). Loads the module, executes it, caches it. Circular imports can cause `ImportError` — fix by moving imports inside functions.

---

**Q: What are dataclasses and when do they beat plain classes?** 🔥
`@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` from field annotations. Cleaner than writing boilerplate. Add `frozen=True` for immutability. Pydantic is a more powerful alternative for validation.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class PatientKey:
    patient_id: int
    year: int
    hcc_version: str
```

---

**Q: What is the difference between threading, multiprocessing, and asyncio?** ⭐ (Meta, Amazon)
- **threading**: shared memory, GIL limits CPU parallelism, good for I/O-bound
- **multiprocessing**: separate processes, real CPU parallelism, higher memory overhead, good for CPU-bound
- **asyncio**: single thread, cooperative multitasking, best for many concurrent I/O operations with low overhead

---

**Q: What is Pydantic and how does it compare to dataclasses?** 🔥 (FastAPI companies, startups)
Pydantic validates data at runtime using type hints — raises `ValidationError` with clear messages on bad input. Dataclasses don't validate. Pydantic v2 (written in Rust) is significantly faster. I used Pydantic in the SLM service to validate every LLM output before writing to DB.

---

**Q: What is `typing.Protocol` and when do you use it over ABCs?** 🔥
`Protocol` enables structural subtyping (duck typing with static checking) — a class doesn't need to explicitly inherit, just implement the right methods. Lighter than ABCs, plays well with type checkers like mypy.

```python
from typing import Protocol

class Extractable(Protocol):
    def extract(self, text: str) -> list[str]: ...
```

---

**Q: How do you profile Python code to find bottlenecks?**
`cProfile` for function-level profiling. `line_profiler` for line-by-line. `memory_profiler` for memory. `py-spy` for sampling without code changes (production-safe). I used `cProfile` to find that an Excel write loop in an Airflow DAG was the bottleneck — replaced with a batch write and cut runtime 10x.

---
