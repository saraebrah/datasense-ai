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


def create_events_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    event_name TEXT NOT NULL,
                    event_timestamp TIMESTAMP NOT NULL,
                    value NUMERIC
                );
            """)


def insert_events(events):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO events (
                    event_id,
                    user_id,
                    event_name,
                    event_timestamp,
                    value
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (event_id) DO NOTHING;
            """, events)


def count_events():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*)
                FROM events;
            """)

            return cur.fetchone()[0]


def get_latest_product_events(limit=5):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    event_id,
                    user_id,
                    event_name,
                    event_timestamp,
                    value
                FROM events
                ORDER BY event_timestamp DESC
                LIMIT %s;
            """, (limit,))

            return cur.fetchall()


def create_weather_forecasts_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS weather_forecasts (
                    location_id BIGINT NOT NULL,
                    location_name TEXT NOT NULL,
                    country TEXT,
                    latitude DOUBLE PRECISION NOT NULL,
                    longitude DOUBLE PRECISION NOT NULL,
                    forecast_time TIMESTAMP NOT NULL,
                    temperature_c DOUBLE PRECISION,
                    precipitation_mm DOUBLE PRECISION,
                    retrieved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

                    PRIMARY KEY (location_id, forecast_time)
                );
            """)


def upsert_weather_forecasts(forecasts):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO weather_forecasts (
                    location_id,
                    location_name,
                    country,
                    latitude,
                    longitude,
                    forecast_time,
                    temperature_c,
                    precipitation_mm
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

                ON CONFLICT (location_id, forecast_time)
                DO UPDATE SET
                    temperature_c = EXCLUDED.temperature_c,
                    precipitation_mm = EXCLUDED.precipitation_mm,
                    retrieved_at = NOW();
            """, forecasts)


def count_weather_forecasts():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*)
                FROM weather_forecasts;
            """)

            return cur.fetchone()[0]


def get_latest_weather_forecasts(limit=5):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    location_name,
                    country,
                    forecast_time,
                    temperature_c,
                    precipitation_mm
                FROM weather_forecasts
                ORDER BY forecast_time DESC
                LIMIT %s;
            """, (limit,))

            return cur.fetchall()          


def get_all_events():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    event_id,
                    user_id,
                    event_name,
                    event_timestamp,
                    value
                FROM events
                ORDER BY event_timestamp;
            """)

            return cur.fetchall()


def get_all_weather_forecasts():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    location_name,
                    country,
                    forecast_time,
                    temperature_c,
                    precipitation_mm,
                    retrieved_at
                FROM weather_forecasts
                ORDER BY forecast_time;
            """)

            return cur.fetchall()