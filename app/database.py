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