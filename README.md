# DataSense AI

DataSense AI is an AI-powered data assistant being built as a hands-on engineering project.

The goal is to build an application capable of ingesting data from multiple sources, storing it in PostgreSQL, analyzing it, visualizing insights, and eventually using AI to answer questions about the data.

The project is developed incrementally over a 4-month roadmap, with each week introducing new capabilities while following professional software engineering practices.

---

# Project Goals

The application will eventually be able to:

* Ingest CSV files
* Ingest public API data
* Store data in PostgreSQL
* Analyze data using SQL and Python
* Visualize insights with interactive dashboards
* Generate AI-powered summaries and answers

---

# Tech Stack

* Python
* PostgreSQL
* Docker
* Streamlit
* Pandas
* Plotly
* Git & GitHub

---

# Current Project Structure

```text
datasense-ai/

app/
├── main.py
├── database.py
├── repository.py
├── ingestion.py
└── db_demo.py

data/
├── raw/
├── processed/
└── samples/
    └── product_events.csv

docs/
notebooks/
sql/
tests/

README.md
project_log.md
docker-compose.yml
requirements.txt
```

---

# Getting Started

## 1. Clone the repository

```bash
git clone <repository-url>
cd datasense-ai
```

## 2. Create and activate the virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Start PostgreSQL

```bash
docker compose up -d
```

Verify it is running:

```bash
docker ps
```

You should see:

```text
datasense_postgres
```

---

# Test the Database Layer

Run:

```bash
python app/db_demo.py
```

Expected output:

```text
Database connection successful.
```

---

# CSV Data Ingestion

The project can ingest product event data from CSV into PostgreSQL. A sample dataset is available at:

```text
data/samples/product_events.csv
```

Run the ingestion pipeline:

```bash
python app/ingestion.py
```

The pipeline:

1. Reads the CSV using Pandas.
2. Validates the required columns.
3. Converts timestamps into datetime values.
4. Creates the PostgreSQL `events` table if needed.
5. Inserts the events.
6. Prevents duplicate events using `event_id`.

The pipeline is idempotent: running it multiple times does not duplicate previously loaded events.

---

# Streamlit Application

Launch the application with:

```bash
streamlit run app/main.py
```

---

# Current Status

✅ Project foundation complete

✅ Docker configured

✅ PostgreSQL running inside Docker

✅ Python connected to PostgreSQL

✅ Reusable database layer implemented

✅ CSV ingestion

⬜ API ingestion

⬜ Analytics engine

⬜ Interactive dashboard

⬜ AI assistant
