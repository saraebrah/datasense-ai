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