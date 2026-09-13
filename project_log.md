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


## Week 4

### Goal

Build the first real data ingestion pipeline by loading CSV data into PostgreSQL.

### What I Built

- Created a reusable sample product-events dataset.
- Added a real `events` table.
- Added batch event insertion to the repository layer.
- Created a CSV ingestion module.
- Added basic input validation.
- Converted Pandas data into database-ready records.
- Added duplicate protection using `event_id`.
- Verified imported data directly using SQL.

### What I Learned

- How raw data moves from a file into PostgreSQL.
- Why input data should be validated before loading.
- How application data is converted into database records.
- How batch database inserts work.
- Why ingestion pipelines should be safe to rerun.
- The meaning of idempotency in a data pipeline.


## Week 5

### Goal

Build an ingestion pipeline that retrieves external data from a public API and stores it in PostgreSQL.

### What I Built

- Added the Requests HTTP library.
- Made API calls from Python.
- Added a reusable API client module.
- Used a geocoding API to convert city names into coordinates.
- Retrieved weather forecasts from a public API.
- Converted JSON API responses into database records.
- Added a weather forecast table.
- Added database upsert logic.
- Loaded API data into PostgreSQL.
- Verified API data directly using SQL.

### What I Learned

- How HTTP GET requests work.
- How query parameters are passed to APIs.
- How JSON API responses become Python objects.
- Why network requests need timeouts.
- Why HTTP errors should be checked explicitly.
- How one API response can provide input to another API.
- How to transform external JSON into an internal data model.
- The difference between insert-only ingestion and upsert ingestion.
- Why forecasts should be updated rather than duplicated.



## Week 7

### Goal

Turn the existing backend into the first usable DataSense AI dashboard.

### What I Built

- Connected Streamlit directly to PostgreSQL-backed data.
- Added a dashboard data-preparation layer.
- Added product-event KPI cards.
- Added interactive event filtering.
- Added Plotly event visualizations.
- Added daily product activity visualization.
- Added interactive event tables.
- Added weather KPI cards.
- Added temperature and precipitation visualizations.
- Added weather data tables.
- Added empty-data handling.

### What I Learned

- How a user interface retrieves data through a repository layer.
- How database rows are converted into Pandas DataFrames.
- How Streamlit reruns an application when widget state changes.
- How Streamlit widgets can control dashboard data.
- How to create KPI cards.
- How Plotly figures integrate with Streamlit.
- How to separate data preparation from UI code.
- Why user-facing applications need useful empty states.


## Week 8

### Goal

Turn CSV ingestion into a user-facing product workflow instead of requiring terminal commands.

### What I Built

- Refactored CSV ingestion into reusable functions.
- Separated DataFrame validation from file loading.
- Added stronger CSV validation.
- Added duplicate-ID validation.
- Added Streamlit CSV upload.
- Added upload previews.
- Added explicit user confirmation before database writes.
- Connected uploaded data to the existing PostgreSQL ingestion layer.
- Added success and error feedback.
- Added automatic dashboard refresh after ingestion.
- Added downloadable sample CSV guidance.
- Verified terminal ingestion still works.

### What I Learned

- How to reuse business logic across multiple interfaces.
- Why ingestion functions should operate on data rather than UI-specific objects.
- How to handle uploaded files in Streamlit.
- How `try` / `except` prevents user input from crashing an application.
- Why data should be validated before database writes.
- Why users should preview data before performing destructive or persistent actions.
- How Streamlit reruns can refresh application state after a database change.
- The difference between application logic and interface logic.

### Issues / Questions

- No unresolved issues or questions documented yet.


## Week 9

### Goal

Add the first AI-powered analytical feature to DataSense AI.

### What I Built

- Set up a locally running language model.
- Added a reusable LLM client.
- Added structured event-summary context.
- Added a prompt-building layer.
- Generated natural-language analysis from calculated metrics.
- Added AI summary generation to Streamlit.
- Used session state to preserve generated summaries.
- Added failure handling for unavailable model services.
- Connected AI analysis to dashboard filters.

### What I Learned

- How an application communicates with a language model through an API.
- Why model communication should be isolated behind a client module.
- The difference between deterministic calculation and generative interpretation.
- Why AI should receive structured, grounded context.
- How prompt design influences model output.
- Why prompts do not completely eliminate hallucination.
- How dashboard state can determine the context sent to an AI model.
- How to handle AI-service failures without breaking the rest of an application.

### Issues / Questions

- No unresolved issues or questions documented yet.


## Week 10

### Goal

Introduce automated testing and improve the application architecture through a purposeful class-based refactor.

### What I Built

- Added pytest.
- Started using the tests directory.
- Added ingestion validation tests.
- Added dashboard transformation tests.
- Added AI-context tests.
- Refactored the LLM client from functions into a class.
- Added configurable LLM client state.
- Added mocked HTTP tests.
- Verified LLM client behavior without calling Ollama.
- Added a repeatable full test suite.

### What I Learned

- The Arrange / Act / Assert testing pattern.
- Why invalid input should also be tested.
- How pytest discovers tests.
- The difference between unit tests and integration tests.
- Why external dependencies make tests harder.
- What mocking is and why it is useful.
- How to verify HTTP calls without making real requests.
- Why classes are useful when state and behavior naturally belong together.
- Why not every function should be converted into a class.
- How automated tests make refactoring safer.

### Issues / Questions

- Plain `pytest` fails during test collection because of the current import paths. Running `PYTHONPATH=app python -m pytest` from the project root passes all 11 tests; consistent imports remain a follow-up improvement.
