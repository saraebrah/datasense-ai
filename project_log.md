# Project Log

## Week 1

### Goal
Set up the project repository, Python environment, folder structure, and first Streamlit app.

### What I Built
- Created GitHub repository
- Created folder structure
- Set up Python virtual environment
- Created basic Streamlit app

### What I Learned
- Basic Git workflow
- Project structure
- Virtual environment setup


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
- Docker Compose stores container configuration in a reusable file.
- PostgreSQL stores data persistently using a Docker volume.
- `.env` files keep configuration separate from code.
- Python can connect to PostgreSQL using `psycopg`.


## Week 3

### Goal

Refactor the database code into a reusable architecture.

### What I Built

- Split the database layer into reusable modules.
- Created a repository layer.
- Created a development database demo script.
- Kept the Streamlit UI independent from the backend.

### What I Learned

- Single Responsibility Principle (SRP). A file, class, or function should have one job.
- Why SQL should not live inside application code.
- Why reusable modules reduce duplication.
- How a repository layer simplifies future development.

### Reflection

The project now feels like a real software project instead of a collection of scripts.
