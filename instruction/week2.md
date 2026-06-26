# Week 2 — Docker & PostgreSQL

> **Prerequisites**
>
> * Week 1 completed
> * Docker Desktop installed
> * VS Code installed
> * Python virtual environment working
> * `psycopg` and `python-dotenv` installed
>
> Throughout this guide:
>
> * **Bash** commands are run in the **VS Code Terminal**.
> * **Python** and configuration files are edited in the **VS Code Editor**.

---

# Week Goal

By the end of Week 2, I should have:

* PostgreSQL running inside Docker.
* A reusable Docker Compose configuration.
* A PostgreSQL database container.
* Environment variables stored in a `.env` file.
* A Python module that connects to PostgreSQL.
* A table created from Python.
* Test data inserted and retrieved from PostgreSQL.
* A Pull Request merged into `main`.

---

# Time Budget

| Task                  | Estimated Time |
| --------------------- | -------------: |
| Docker + PostgreSQL   |        2 hours |
| Docker Compose        |         1 hour |
| Environment Variables |     30 minutes |
| Python Database Layer |        2 hours |
| SQL Test              |         1 hour |
| Documentation + Git   |      1.5 hours |

**Total:** ~8 hours

---

# Deliverable

By the end of this week you should be able to demonstrate:

```bash
docker ps
```

showing PostgreSQL running,

and

```bash
python app/database.py
```

showing something similar to:

```text
Database connection successful.

Latest rows:

(1, 'week_2_connection_test')
```

---

# Architecture After Week 2

```text
                DataSense AI

           Python Application
                    │
                    │ psycopg
                    ▼
             PostgreSQL Database
                    ▲
                    │
             Docker Container
```

This is the first time our application will communicate with another service.

---

# Learning Objectives

This week you are **not** trying to become an expert in Docker or PostgreSQL.

The objective is simply to understand:

* how a database runs,
* how Python connects to it,
* and how data is stored permanently.

---

# Step 1 — Create a Feature Branch

## Goal

Create a dedicated branch for this week's work.

## Why

Every feature should be developed independently before being merged into `main`.

---

## Action

Run:

```bash
git checkout main
git pull origin main
git checkout -b feature/postgres-docker-setup
```

---

## Verify

Run:

```bash
git branch
```

Expected output:

```text
* feature/postgres-docker-setup
  main
```

---

## Success Criteria

You are currently working on:

```text
feature/postgres-docker-setup
```

---

# Step 2 — Verify Docker

## Goal

Confirm Docker is installed and working.

## Why

Everything this week depends on Docker.

---

## Action

Run:

```bash
docker --version
docker compose version
```

Expected output:

```text
Docker version xx.x.x

Docker Compose version xx.x.x
```

Now run:

```bash
docker run hello-world
```

If this is the first time you've run this command, Docker will download a tiny image before executing it.

Expected output ends with:

```text
Hello from Docker!
```

---

## Success Criteria

Docker successfully starts and runs the test container.

---

# Step 3 — Create docker-compose.yml

## Goal

Create the configuration that tells Docker how to start PostgreSQL.

## Why

Instead of remembering a long `docker run` command every time, we keep everything inside one configuration file.

---

## Action

Create the file:

```bash
touch docker-compose.yml
```

Open it in VS Code.

Paste:

```yaml
services:
  postgres:
    image: postgres:17

    container_name: datasense_postgres

    environment:
      POSTGRES_USER: datasense_user
      POSTGRES_PASSWORD: datasense_password
      POSTGRES_DB: datasense_db

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## What Each Section Does

### image

```yaml
image: postgres:17
```

Downloads the official PostgreSQL image.

---

### container_name

```yaml
container_name: datasense_postgres
```

Gives the container a predictable name instead of Docker generating one.

---

### environment

```yaml
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

Creates the initial database credentials.

---

### ports

```yaml
5432:5432
```

Allows your Mac to communicate with PostgreSQL running inside Docker.

---

### volumes

```yaml
postgres_data
```

Keeps your database even if the container stops.

---

## Verify

Run:

```bash
cat docker-compose.yml
```

Confirm the contents match exactly.

---

## Success Criteria

`docker-compose.yml` exists in the root of the project.

---

# Step 4 — Start PostgreSQL

## Goal

Launch PostgreSQL.

## Why

The configuration exists; now we use it to start the database.

---

## Action

Run:

```bash
docker compose up -d
```

The first run may take a few minutes while Docker downloads the PostgreSQL image.

---

## Verify

Run:

```bash
docker ps
```

Expected output should include:

```text
datasense_postgres
```

---

## Success Criteria

The PostgreSQL container is running.

---

# Stop Here

At this point you have completed the first milestone.

Before continuing to the Python code, verify that:

* [ ] Feature branch created
* [ ] Docker verified
* [ ] `docker-compose.yml` created
* [ ] PostgreSQL container running

If everything works, continue with the next section of this document.
