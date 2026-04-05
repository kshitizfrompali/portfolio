# Docker & Linux Interview Questions

> ⭐ = Frequently asked | 🔥 = Trending 2024-25

---

## Linux

**Q: What is the difference between a process and a thread?** ⭐
A process has its own memory space, file descriptors, and PID. Threads share memory within a process. Creating a process is heavier (fork) but isolated. Threads are lighter but share state (need synchronization). Python's `multiprocessing` uses processes; `threading` uses threads.

---

**Q: What is a file descriptor?**
An integer handle to an open file, socket, or pipe. Every process gets stdin (0), stdout (1), stderr (2) by default. `ulimit -n` sets the max open file descriptors — a common bottleneck for high-connection services.

---

**Q: What does `ps aux` show?**
Running processes: user, PID, CPU%, MEM%, command. `ps aux | grep celery` to find Celery workers. `kill -9 PID` to force-kill a process.

---

**Q: What is a signal in Linux?**
A notification sent to a process. `SIGTERM` (15): graceful shutdown request. `SIGKILL` (9): immediate kill, can't be caught. `SIGINT` (2): Ctrl+C. Celery workers handle `SIGTERM` gracefully — finish current task then stop.

---

**Q: What is `grep`, `awk`, and `sed`?** ⭐
`grep`: search text by pattern. `awk`: process column-delimited text. `sed`: stream editor for find/replace. In practice: `grep "ERROR" airflow.log | awk '{print $5}'` to extract error timestamps.

---

**Q: What is `cron`?**
System scheduler — runs commands at specified times. Syntax: `minute hour day month weekday command`. Airflow Beat or Kubernetes CronJobs replace cron for application-level scheduling in modern stacks.

---

**Q: What is a symlink?**
A symbolic link — a file that points to another file or directory. `ln -s /path/to/target link_name`. Useful for pointing config files to environment-specific locations.

---

**Q: What is `/etc/hosts` and when would you edit it?**
Local DNS override. Maps hostnames to IPs. Useful in development to point `api.myapp.local` to `127.0.0.1` without a real DNS setup. In Docker Compose, service names are resolved via Docker's internal DNS — similar concept.

---

**Q: What is `chmod` and `chown`?**
`chmod`: change file permissions (read/write/execute for user/group/others). `chmod 755 script.sh` — owner can read/write/execute, others can read/execute. `chown`: change file owner. Important when files created by root in a Docker container need to be accessible by the app user.

---

**Q: What is a pipe (`|`) in Linux?**
Connects stdout of one command to stdin of the next. `cat access.log | grep "ERROR" | wc -l` — count error lines in a log file. Fundamental for composing CLI tools.

---

**Q: What is `systemd`?**
Linux init system and service manager. Manages background services (start on boot, restart on crash, log aggregation). `systemctl start/stop/status service_name`. In production, Celery workers often run as systemd services.

---

**Q: What is the difference between `SIGTERM` and `SIGKILL`?** ⭐
`SIGTERM`: polite shutdown request — process can catch it, clean up, and exit gracefully. Docker `docker stop` sends SIGTERM first. `SIGKILL`: force kill — can't be caught or ignored, immediate termination, no cleanup. Use SIGKILL only as last resort (risk of data corruption, open transactions).

---

**Q: What does `df -h` and `du -sh` do?**
`df -h`: disk free — shows filesystem usage (how full each mounted disk is). `du -sh path`: disk usage of a directory. Essential for debugging "disk full" issues on production servers.

---

## Docker

**Q: What is Docker and what problem does it solve?** ⭐
Docker packages an application and its dependencies into a portable container image. Solves "works on my machine" — the same image runs identically on dev, staging, and production. Lighter than VMs (shares the host kernel).

---

**Q: What is the difference between an image and a container?** ⭐
Image: read-only template (built from a Dockerfile). Container: a running instance of an image — adds a writable layer on top. You can run many containers from one image.

---

**Q: What is a Dockerfile?** ⭐
A text file with instructions to build an image. Key instructions: `FROM` (base image), `RUN` (execute command), `COPY` (copy files), `ENV` (environment variables), `EXPOSE` (document port), `CMD`/`ENTRYPOINT` (default command).

---

**Q: What is Docker Compose?** ⭐
Tool for defining and running multi-container applications with a YAML file. `docker-compose up` starts all services. Used for local development — define app, DB, Redis, Celery worker as services. Each service gets a hostname resolvable by others.

---

**Q: What is the difference between `CMD` and `ENTRYPOINT` in a Dockerfile?**
`ENTRYPOINT`: the fixed executable that always runs (e.g. `python`). `CMD`: default arguments to ENTRYPOINT (can be overridden at `docker run`). Together: `ENTRYPOINT ["python"]` + `CMD ["manage.py", "runserver"]`.

---

**Q: What are Docker volumes and why use them?** ⭐
Volumes persist data outside the container's writable layer — data survives container restarts and deletion. Use for DB data, uploaded files, logs. Three types: named volumes (managed by Docker), bind mounts (map host directory), tmpfs (in-memory).

---

**Q: What is a multi-stage build?** 🔥
Use multiple `FROM` in one Dockerfile — build in one stage (with compiler, build deps), copy only the artifact to a minimal final image. Reduces production image size dramatically.

```dockerfile
FROM python:3.12 AS builder
RUN pip install --user -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["python", "app.py"]
```

---

**Q: What is the difference between `docker stop` and `docker kill`?** ⭐
`docker stop`: sends SIGTERM, waits 10s for graceful shutdown, then sends SIGKILL. `docker kill`: sends SIGKILL immediately. Always use `docker stop` to allow containers to clean up (close DB connections, finish tasks).

---

**Q: How do you reduce Docker image size?** 🔥
1. Use slim/alpine base images
2. Multi-stage builds
3. Minimize layers (`RUN` chaining with `&&`)
4. `.dockerignore` to exclude unnecessary files
5. Don't install dev dependencies in production image
6. Clean up apt cache: `rm -rf /var/lib/apt/lists/*`

---

**Q: What is `docker network` and how do containers communicate?** ⭐
Docker creates virtual networks. Containers on the same network communicate by service name (DNS). `bridge` network (default): containers on the same host. `host` network: container shares host networking. `overlay`: multi-host networking (Swarm/Kubernetes).

---

**Q: What is the Docker layer cache and how does it affect build speed?** 🔥
Each Dockerfile instruction creates a layer. Docker caches layers — if a layer's instruction and inputs haven't changed, it reuses the cached layer. Order matters: put rarely-changed instructions first. Put `COPY requirements.txt` + `RUN pip install` before `COPY . .` so the dependency layer is cached across code changes.

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt   # cached if requirements.txt unchanged
COPY . .                               # invalidates cache only on code change
```

---

**Q: How do you pass secrets to a Docker container securely?** 🔥
Never bake secrets into the image. Options:
1. Environment variables at runtime: `docker run -e API_KEY=$API_KEY`
2. Docker secrets (Swarm): mounted as files at `/run/secrets/`
3. AWS Secrets Manager / HashiCorp Vault: fetch at startup
4. `.env` file mounted as volume (not committed to git)

---

**Q: What is `docker exec` and when do you use it?**
Run a command inside a running container: `docker exec -it container_name bash`. Used for debugging — inspect files, run DB migrations, check logs inside the container. Equivalent to SSHing into a server.

---

**Q: What is the difference between Docker and Kubernetes?**
Docker: container runtime — creates and runs containers on one machine. Kubernetes: container orchestration — manages containers across many machines, handles scheduling, scaling, self-healing, service discovery, rolling deployments. Docker Compose is for local dev; Kubernetes is for production clusters.

---
