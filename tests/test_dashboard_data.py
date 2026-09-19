import pandas as pd

from app.dashboard_data import (
    build_event_qa_context,
    build_event_summary_context,
    get_daily_event_activity,
    get_event_counts_by_type,
)

def create_sample_events_dataframe():
    return pd.DataFrame(
        {
            "event_id": [
                "evt_001",
                "evt_002",
                "evt_003",
                "evt_004",
            ],
            "user_id": [
                "user_001",
                "user_001",
                "user_002",
                "user_002",
            ],
            "event_name": [
                "login",
                "login",
                "signup",
                "login",
            ],
            "event_timestamp": pd.to_datetime(
                [
                    "2026-08-01T09:00:00",
                    "2026-08-01T10:00:00",
                    "2026-08-02T09:00:00",
                    "2026-08-02T10:00:00",
                ]
            ),
            "value": [
                None,
                None,
                None,
                None,
            ],
        }
    )


def test_event_counts_by_type():
    df = create_sample_events_dataframe()

    result = get_event_counts_by_type(df)

    counts = dict(
        zip(
            result["event_name"],
            result["event_count"],
        )
    )

    assert counts["login"] == 3
    assert counts["signup"] == 1


def test_daily_event_activity():
    df = create_sample_events_dataframe()

    result = get_daily_event_activity(df)

    assert len(result) == 2

    assert result["event_count"].tolist() == [
        2,
        2,
    ]


def test_event_summary_context():
    df = create_sample_events_dataframe()

    context = build_event_summary_context(df)

    assert context["total_events"] == 4
    assert context["unique_users"] == 2
    assert context["event_types"] == 2

    assert context["event_counts"]["login"] == 3
    assert context["event_counts"]["signup"] == 1


def test_empty_dataframe_returns_no_summary_context():
    df = create_sample_events_dataframe().iloc[0:0]

    context = build_event_summary_context(df)

    assert context is None


def test_event_qa_context():

    df = create_sample_events_dataframe()

    context = build_event_qa_context(df)

    assert context["total_events"] == 4

    assert context["unique_users"] == 2

    assert context["event_counts"]["login"] == 3

    assert context["event_counts"]["signup"] == 1

    assert (
        context["events_per_user"]["user_001"]
        == 2
    )


def test_empty_dataframe_returns_no_qa_context():

    df = (
        create_sample_events_dataframe()
        .iloc[0:0]
    )

    context = build_event_qa_context(df)

    assert context is None