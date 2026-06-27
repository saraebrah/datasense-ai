# Week 3 — Building a Reusable Database Layer

> **Prerequisites**
>
> * Week 2 completed
> * PostgreSQL running inside Docker
> * `python app/database.py` executes successfully
> * Week 2 merged into `main`

---

# Week Goal

By the end of Week 3, I should have:

* A cleaner database architecture.
* A reusable database layer.
* Smaller, focused Python modules.
* A clear separation between:

  * database connection,
  * database operations,
  * application UI.
* A project structure ready for CSV ingestion in Week 4.

---

# Time Budget

| Task                           | Estimated Time |
| ------------------------------ | -------------: |
| Refactoring                    |        2 hours |
| Database Layer                 |        2 hours |
| Testing                        |         1 hour |
| Documentation                  |         1 hour |
| Git & PR                       |         1 hour |
| Understanding the architecture |         1 hour |

**Total:** ~8 hours

---

# Deliverable

By the end of this week you should be able to run:

```bash
python app/db_demo.py
```

and see:

```text
Database connection successful.

Latest rows:

...
```

At the same time, the original Streamlit application should still work:

```bash
streamlit run main.py
```

Nothing from Week 1 or Week 2 should break.

---

# Architecture After Week 3

```text
                   Streamlit UI
                     main.py
                        │
                        ▼
                 repository.py
                        │
                        ▼
                  database.py
                        │
                        ▼
              PostgreSQL (Docker)
```

Notice something important.

`main.py` is **still** the application's entry point.

We are **not** replacing it.

Instead, we're building a reusable backend underneath it.

Later, the Streamlit UI will call the repository directly.

---

# Learning Objectives

By the end of this week you should understand:

* Why software is split into modules.
* What "single responsibility" means.
* Why reusable functions matter.
* Why separating the UI from the database is good software design.

---

# Step 1 — Create a Feature Branch

## Goal

Create a feature branch for Week 3.

---

## Why

Every week's work should be isolated until it is reviewed and merged.

---

## Action

Run:

```bash
git checkout main
git pull origin main
git checkout -b feature/database-layer
```

---

## Verify

Run:

```bash
git branch
```

Expected:

```text
* feature/database-layer
```

---

## Success Criteria

You are working on:

```text
feature/database-layer
```

---

# Step 2 — Review The Current Project

## Goal

Understand where the project currently stands before changing it.

---

## Action

Run:

```bash
tree -L 2
```

Your project should roughly look like:

```text
datasense-ai/

app/
database.py

data/

docs/

README.md
main.py
project_log.md
docker-compose.yml
```

Notice that `main.py` sits in the project root.

That is intentional.

It is our Streamlit application.

We are **not** touching it this week.

---

# Step 3 — Review database.py

Open:

```text
app/database.py
```

Before changing anything, read through it carefully.

Ask yourself:

> "How many different jobs is this file doing?"

You should identify approximately these responsibilities:

* connecting to PostgreSQL
* creating tables
* inserting data
* retrieving data
* running the program

One file.

Five responsibilities.

That is exactly why we are refactoring.

---

# Challenge

Spend **10 minutes** thinking about this question before reading further.

> If you had to split this file into smaller pieces, how would you do it?

There is no single correct answer.

The purpose of the exercise is to begin thinking like a software engineer rather than simply writing code.

---

# Step 4 — Create New Modules

## Goal

Separate the responsibilities identified above.

---

## Why

Professional software grows.

As it grows, files become difficult to maintain.

Smaller modules make the project easier to understand and easier to extend.

---

## Action

Create two new files:

```bash
touch app/repository.py
touch app/db_demo.py
```

Notice that we are **not** creating another `main.py`.

Your project should now look like:

```text
app/

database.py
repository.py
db_demo.py
```

---

# Why These Files?

## database.py

Responsible only for creating database connections.

Nothing more.

---

## repository.py

Responsible only for interacting with the database.

Examples:

* insert
* update
* delete
* select

Notice something.

There is **no user interface** here.

There is **no Streamlit** here.

Only database operations.

---

## db_demo.py

This is a temporary development script.

Its purpose is simply to verify that our database layer works.

Later in the project, the Streamlit application will call the repository directly, and this file may disappear entirely.

---

# Step 5 — Simplify database.py

Replace the contents of:

```text
app/database.py
```

with:

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
```

---

# Why Is This Better?

Think about what this file now does.

Only one thing.

It creates database connections.

Nothing else.

Suppose six different parts of the application need database access.

Instead of writing:

```python
psycopg.connect(...)
```

six times,

every file simply imports:

```python
from database import get_connection
```

Now imagine that, six months from now, we migrate from PostgreSQL to another database.

Where do we change the connection code?

Only here.

That is the advantage of centralizing responsibility.

---

# Stop Point

Before continuing, verify:

* [ ] Feature branch created.
* [ ] `repository.py` created.
* [ ] `db_demo.py` created.
* [ ] `database.py` simplified.
* [ ] Existing `main.py` left unchanged.

Do **not** delete any Week 2 functionality.

We are about to move it into the repository layer in the next section.
# Step 6 — Create the Repository Layer

## Goal

Move all database operations into one reusable module.

---

## Why

Think of `repository.py` as the only place that knows how to interact with the database.

Future parts of the application should never execute SQL directly.

Instead, they will call repository functions.

---

## Action

Open:

```text
app/repository.py
```

Replace its contents with:

```python
from database import get_connection


def create_test_events_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS test_events (
                    id SERIAL PRIMARY KEY,
                    event_name TEXT NOT NULL
                );
            """)


def insert_test_event(event_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO test_events (event_name)
                VALUES (%s);
            """, (event_name,))


def get_latest_events(limit=5):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, event_name
                FROM test_events
                ORDER BY id DESC
                LIMIT %s;
            """, (limit,))

            return cur.fetchall()
```

---

# Understanding This Module

Notice that every function has one responsibility.

| Function                     | Responsibility    |
| ---------------------------- | ----------------- |
| `create_test_events_table()` | Creates the table |
| `insert_test_event()`        | Inserts one event |
| `get_latest_events()`        | Reads events      |

This makes the code easier to understand and easier to test.

---

# Challenge

Without looking at the code above, answer this question:

> If tomorrow you wanted to delete an event, where would that function belong?

The answer should now feel obvious.

---

# Step 7 — Create db_demo.py

## Goal

Create a small application that uses the repository.

---

## Why

The application should not know SQL.

It should only call functions.

---

Open:

```text
app/db_demo.py
```

Paste:

```python
from repository import (
    create_test_events_table,
    insert_test_event,
    get_latest_events,
)


def main():

    create_test_events_table()

    insert_test_event("week_3_repository_test")

    rows = get_latest_events()

    print("Database connection successful.\n")
    print("Latest rows:\n")

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
```

---

# What Changed?

Compare Week 2 and Week 3.

Week 2:

```text
main()
 │
 ├── SQL
 ├── SQL
 ├── SQL
 └── SQL
```

Week 3:

```text
main()
 │
 ├── create_table()
 ├── insert()
 └── get_events()
```

The SQL disappeared from the application.

That is exactly what we wanted.

---

# Step 8 — Test Everything

Run:

```bash
python app/db_demo.py
```

Expected output:

```text
Database connection successful.

Latest rows:

(3, 'week_3_repository_test')
(2, 'week_2_connection_test')
...
```

Notice something.

We didn't lose the Week 2 data.

The Docker volume preserved it.

---

# Step 9 — Verify Streamlit Still Works

Run:

```bash
streamlit run main.py
```

Verify that the Week 1 page still opens successfully.

This is important.

One of the goals of refactoring is improving code **without breaking existing functionality**.

---

# Step 10 — Update README

Add the following section.

````markdown
## Project Architecture

Current backend structure:

```text
main.py                 # Streamlit application

app/
├── database.py         # PostgreSQL connection
├── repository.py       # Database operations
└── db_demo.py          # Development/testing script
```

The Streamlit application will gradually use the repository layer directly as the project evolves.
````

---

# Step 11 — Update project_log.md

Append:

```markdown
## Week 3

### Goal

Refactor the database code into a reusable architecture.

### What I Built

- Split the database layer into reusable modules.
- Created a repository layer.
- Created a development database demo script.
- Kept the Streamlit UI independent from the backend.

### What I Learned

- Single Responsibility Principle.
- Why SQL should not live inside application code.
- Why reusable modules reduce duplication.
- How a repository layer simplifies future development.

### Reflection

The project now feels like a real software project instead of a collection of scripts.
```

---

# Step 12 — Git

Run:

```bash
git status
```

Review every changed file.

Then:

```bash
git add .
git commit -m "Refactor database layer"
git push origin feature/database-layer
```

Open a Pull Request.

Title:

```text
Refactor database layer
```

Merge into `main`.

Finally:

```bash
git checkout main
git pull origin main
```

---

# Definition of Done

Week 3 is complete when:

* [ ] `database.py` only creates connections.
* [ ] `repository.py` contains all SQL.
* [ ] `db_demo.py` successfully runs.
* [ ] Streamlit application still works.
* [ ] README updated.
* [ ] project log updated.
* [ ] Changes committed.
* [ ] Pull Request merged.
* [ ] Local `main` updated.

---

# Week 3 Review

Congratulations.

This week you didn't add many new features.

Instead, you improved the **quality** of the codebase.

That is one of the biggest differences between beginners and experienced engineers.

Beginners tend to focus on adding functionality.

Experienced engineers spend a surprising amount of time improving structure, readability, and maintainability.

By the end of Week 3, DataSense AI now has a proper backend foundation.

Week 4 will build on this by introducing the first real dataset. Instead of inserting hardcoded values, you'll build a small ingestion pipeline that reads data from a CSV file and stores it in PostgreSQL.

From this point onward, every new feature will be added on top of the architecture you built this week.
