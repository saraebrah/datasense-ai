# DataSense AI

DataSense AI is a 4-month learning project focused on building an AI-powered data assistant.

## Project Goal

Build an application that can:

- ingest CSV data
- ingest public API data
- store data in PostgreSQL
- analyze data with SQL and Python
- visualize insights
- generate AI-powered summaries and answers

## Tech Stack

- Python
- PostgreSQL
- Docker
- Streamlit
- Pandas
- Plotly
- Git/GitHub


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
