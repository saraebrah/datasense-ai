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
# Step 5 — Verify PostgreSQL Is Running

## Goal

Verify that PostgreSQL inside the Docker container is working correctly before writing any Python code.

## Why

Before connecting from Python, we want to ensure PostgreSQL itself is healthy. This helps isolate problems. If something fails later, we'll know whether it's the database or our Python code.

---

## Action

Run:

```bash
docker exec -it datasense_postgres psql -U datasense_user -d datasense_db
```

If successful, you should see something similar to:

```text
datasense_db=#
```

This means you are now inside PostgreSQL's interactive shell (`psql`).

---

## Verify

Run:

```sql
SELECT version();
```

Expected output:

```text
PostgreSQL 17.x ...
```

This confirms the database is running and accepting SQL commands.

---

## Exit PostgreSQL

Run:

```sql
\q
```

You should return to your normal terminal.

---

## Success Criteria

* [ ] Successfully entered PostgreSQL
* [ ] Successfully executed a SQL query
* [ ] Successfully exited PostgreSQL

---

# Step 6 — Create the Environment Configuration

## Goal

Store the database connection details outside the source code.

## Why

Applications often have different environments (development, testing, production). Keeping configuration separate from code makes the application easier to maintain and avoids hardcoding sensitive information.

---

## Action

Create the file:

```bash
touch .env
```

Open it in VS Code.

Paste:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=datasense_db
DB_USER=datasense_user
DB_PASSWORD=datasense_password
```

---

## Verify

Run:

```bash
cat .env
```

Verify that the contents match exactly.

---

## Verify Git

Run:

```bash
git status
```

You should **NOT** see `.env`.

If you do, stop here and let me know. We will update `.gitignore` before continuing.

---

## Success Criteria

* [ ] `.env` created
* [ ] Variables added correctly
* [ ] `.env` is ignored by Git

---

# Step 7 — Create the Database Module

## Goal

Create the project's first reusable database module.

## Why

Rather than creating a one-time test script, we'll build a reusable module that future parts of the application can import.

This follows better software design and prepares us for future weeks.

---

## Action

Create the file:

```bash
touch app/database.py
```

Open it in VS Code.

Paste:

```python
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def main():
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS test_events (
                    id SERIAL PRIMARY KEY,
                    event_name TEXT NOT NULL
                );
            """)

            cur.execute("""
                INSERT INTO test_events (event_name)
                VALUES (%s);
            """, ("week_2_connection_test",))

            cur.execute("""
                SELECT id, event_name
                FROM test_events
                ORDER BY id DESC
                LIMIT 5;
            """)

            rows = cur.fetchall()

    print("Database connection successful.\n")
    print("Latest rows:\n")

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
```

---

## Understanding the Code

### `load_dotenv()`

Loads the variables stored inside `.env` into the Python process.

---

### `get_connection()`

Creates and returns a connection to PostgreSQL using the values from `.env`.

---

### `CREATE TABLE`

Creates the table only if it doesn't already exist.

This means you can safely run the script multiple times.

---

### `INSERT`

Adds one test row.

---

### `SELECT`

Retrieves the latest five rows so we can verify that everything worked.

---

## Success Criteria

* [ ] `database.py` created
* [ ] No syntax errors
* [ ] File saved

<!-- Continue appending below Step 7 -->

# Step 8 — Run the Database Module

## Goal

Verify that Python can connect to PostgreSQL, create a table, insert data, and retrieve it.

## Why

This is the final proof that all components are working together:

* Python
* Environment variables
* PostgreSQL
* Docker

---

## Action

Run:

```bash
python app/database.py
```

---

## Expected Output

Something similar to:

```text
Database connection successful.

Latest rows:

(1, 'week_2_connection_test')
```

If you have run the script multiple times, you will see multiple rows.

---

## Verify

Confirm that:

* No errors are displayed.
* The table is created automatically.
* A new row is inserted.
* The inserted row is displayed.

---

## Success Criteria

* [ ] Python connects to PostgreSQL.
* [ ] Table created successfully.
* [ ] Row inserted successfully.
* [ ] Row retrieved successfully.

---

# Stop Here

Do **not** continue to the documentation or Git steps yet.

Run the script and send me the output (or any error).

We'll review it together before proceeding to the final part of Week 2.

# Step 9 — Update README.md

## Goal

Document how to run PostgreSQL and test the database connection.

## Why

README.md should help another person understand how to run the project.

---

## Action

Open `README.md`.

Add this section:

````markdown
## Local PostgreSQL Setup

This project uses PostgreSQL running inside Docker.

### Start PostgreSQL

```bash
docker compose up -d
```

### Check Running Containers

```bash
docker ps
```

You should see:

```text
datasense_postgres
```

### Connect To PostgreSQL Manually

```bash
docker exec -it datasense_postgres psql -U datasense_user -d datasense_db
```

Exit PostgreSQL with:

```sql
\q
```

### Test Python Database Connection

```bash
python app/database.py
```

Expected output:

```text
Database connection successful.
```
````

---

## Success Criteria

* [ ] README includes PostgreSQL setup instructions.
* [ ] README explains how to run the database test.

---

# Step 10 — Update project_log.md

## Goal

Record what was built and learned in Week 2.

## Why

The project log tracks your learning, decisions, and progress.

---

## Action

Open `project_log.md`.

Add this section:

```markdown
## Week 2

### Goal

Set up PostgreSQL using Docker and connect to it from Python.

### What I Built

- Created `docker-compose.yml`.
- Started PostgreSQL inside Docker.
- Verified PostgreSQL using `psql`.
- Created a `.env` file for database configuration.
- Created `app/database.py`.
- Connected Python to PostgreSQL using `psycopg`.
- Created a test table from Python.
- Inserted and retrieved test rows from PostgreSQL.

### What I Learned

- Docker can run services like PostgreSQL without installing them directly on my Mac.
- Docker Compose stores container configuration in a reusable file.
- PostgreSQL stores data persistently using a Docker volume.
- `.env` files keep configuration separate from code.
- Python can connect to PostgreSQL using `psycopg`.
- `CREATE TABLE`, `INSERT`, and `SELECT` are the basic SQL operations used in this test.

### Issues / Questions

- Add any issues or questions here.
```

---

## Success Criteria

* [ ] Week 2 section added to `project_log.md`.

---

# Step 11 — Check Git Status

## Goal

Review all changed files before committing.

## Why

Always inspect changes before committing.

---

## Action

Run:

```bash
git status
```

Expected changed/untracked files may include:

```text
docker-compose.yml
app/database.py
README.md
project_log.md
docs/week-02-docker-postgresql.md
```

You should **not** see:

```text
.env
```

If `.env` appears, stop and fix `.gitignore` before continuing.

---

# Step 12 — Commit Changes

## Goal

Save Week 2 work in Git.

---

## Action

Run:

```bash
git add .
git commit -m "Add PostgreSQL Docker setup"
```

---

## Success Criteria

Commit succeeds.

---

# Step 13 — Push Feature Branch

## Goal

Send your feature branch to GitHub.

---

## Action

Run:

```bash
git push origin feature/postgres-docker-setup
```

---

# Step 14 — Open Pull Request

## Goal

Merge Week 2 work into `main`.

---

## Action

On GitHub, open a Pull Request:

```text
feature/postgres-docker-setup → main
```

PR title:

```text
Add PostgreSQL Docker setup
```

PR description:

````markdown
## Summary

Adds PostgreSQL running in Docker and verifies Python can connect to it.

## Changes

- Added Docker Compose configuration
- Added PostgreSQL container setup
- Added environment variable configuration
- Added reusable Python database module
- Added database connection test
- Updated README
- Updated project log
- Added Week 2 documentation

## Test

Ran:

```bash
docker ps
python app/database.py
````

Confirmed Python connects to PostgreSQL and retrieves test rows.

````

---

# Step 15 — Merge PR and Update Local Main

## Action

After merging the PR on GitHub, run:

```bash
git checkout main
git pull origin main
````

---

# Definition of Done

Week 2 is complete when:

* [x] PostgreSQL runs inside Docker.
* [x] `docker-compose.yml` exists.
* [x] PostgreSQL can be accessed with `psql`.
* [x] `.env` exists locally.
* [x] `.env` is ignored by Git.
* [x] `app/database.py` connects to PostgreSQL.
* [x] Python creates a table.
* [x] Python inserts a row.
* [x] Python reads rows back.
* [ ] README updated.
* [ ] project_log updated.
* [ ] Week 2 documentation added.
* [ ] Changes committed.
* [ ] Branch pushed.
* [ ] Pull Request merged.
* [ ] Local `main` updated.

---

# Week 2 Demo

At the end of Week 2, I should be able to show:

```bash
docker ps
```

showing `datasense_postgres`, and:

```bash
python app/database.py
```

showing successful database connection and returned rows.

This means DataSense AI now has a working database foundation.
