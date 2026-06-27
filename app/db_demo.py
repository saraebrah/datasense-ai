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