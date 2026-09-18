import plotly.express as px
import streamlit as st

from ai_summary import generate_event_summary
from dashboard_data import (
    build_event_qa_context,
    build_event_summary_context,
    get_daily_event_activity,
    get_event_counts_by_type,
    load_events_dataframe,
    load_weather_dataframe,
)

from ingestion import (
    ingest_events_dataframe,
    load_csv,
)

from qa_service import answer_event_question

st.set_page_config(
    page_title="DataSense AI",
    layout="wide",
)


st.title("DataSense AI")
st.caption(
    "Interactive analytics for product events "
    "and weather data."
)


# ---------------------------------------------------------
# Persistent messages
# ---------------------------------------------------------

if "ingestion_message" in st.session_state:
    st.success(
        st.session_state.pop("ingestion_message")
    )


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

events_df = load_events_dataframe()
weather_df = load_weather_dataframe()


# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------

product_tab, weather_tab = st.tabs(
    [
        "Product Events",
        "Weather Forecasts",
    ]
)


# =========================================================
# PRODUCT EVENTS TAB
# =========================================================

with product_tab:

    st.header("Product Events")

    # -----------------------------------------------------
    # CSV Upload
    # -----------------------------------------------------

    with st.expander(
        "Upload Product Events",
        expanded=False,
    ):

        sample_csv = """event_id,user_id,event_name,event_timestamp,value
evt_example_001,user_example,signup,2026-08-01T09:00:00,
evt_example_002,user_example,login,2026-08-01T09:05:00,
"""

        st.download_button(
            label="Download Sample CSV",
            data=sample_csv,
            file_name="product_events_sample.csv",
            mime="text/csv",
        )

        st.caption(
            "Required columns: "
            "event_id, user_id, event_name, "
            "event_timestamp, value"
        )

        st.caption(
            "event_id must uniquely identify "
            "each event."
        )

        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
        )

        if uploaded_file is not None:

            try:
                uploaded_df = load_csv(
                    uploaded_file
                )

            except Exception as error:
                st.error(
                    f"Unable to read CSV: {error}"
                )

            else:
                st.success(
                    "CSV validation successful."
                )

                st.write(
                    f"Rows detected: {len(uploaded_df)}"
                )

                st.subheader(
                    "Upload Preview"
                )

                st.dataframe(
                    uploaded_df.head(10),
                    width="stretch",
                    hide_index=True,
                )

                ingest_button = st.button(
                    "Ingest Data",
                    type="primary",
                )

                if ingest_button:

                    try:
                        ingest_events_dataframe(
                            uploaded_df
                        )

                    except Exception as error:
                        st.error(
                            f"Ingestion failed: {error}"
                        )

                    else:
                        st.session_state[
                            "ingestion_message"
                        ] = (
                            "CSV processed successfully. "
                            "Existing event IDs were not duplicated."
                        )

                        st.rerun()

    # -----------------------------------------------------
    # Product Dashboard
    # -----------------------------------------------------

    if events_df.empty:

        st.warning(
            "No product event data found. "
            "Upload a CSV above or run: "
            "python app/ingestion.py"
        )

    else:

        event_types = sorted(
            events_df["event_name"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_event_types = st.multiselect(
            "Event types",
            options=event_types,
            default=event_types,
        )

        filtered_events = events_df[
            events_df["event_name"].isin(
                selected_event_types
            )
        ]

        # KPI cards
        metric_1, metric_2, metric_3 = st.columns(3)

        metric_1.metric(
            "Total Events",
            len(filtered_events),
        )

        metric_2.metric(
            "Unique Users",
            filtered_events["user_id"].nunique(),
        )

        metric_3.metric(
            "Event Types",
            filtered_events["event_name"].nunique(),
        )

        if filtered_events.empty:

            st.info(
                "Select at least one event type "
                "to display analytics."
            )

        else:

            # -------------------------------------------------
            # AI Insights
            # -------------------------------------------------

            st.subheader("AI Insights")

            generate_summary_button = st.button(
                "Generate AI Summary",
            )

            if generate_summary_button:

                context = build_event_summary_context(
                    filtered_events
                )

                if context is None:

                    st.warning(
                        "No event data available "
                        "to summarize."
                    )

                else:

                    with st.spinner(
                        "Generating AI summary..."
                    ):

                        try:
                            summary = (
                                generate_event_summary(
                                    context
                                )
                            )

                        except Exception as error:
                            st.error(
                                f"AI summary failed: "
                                f"{error}"
                            )

                        else:
                            st.session_state[
                                "event_ai_summary"
                            ] = summary

            if (
                "event_ai_summary"
                in st.session_state
            ):

                st.markdown(
                    st.session_state[
                        "event_ai_summary"
                    ]
                )

            st.markdown("---")

            st.subheader(
                "Ask About Your Data"
            )

            event_question = st.text_input(
                "Ask a question about the filtered event data",
                placeholder=(
                    "e.g. Which event type "
                    "is most common?"
                ),
            )

            ask_question_button = st.button(
                "Ask DataSense",
            )

            if ask_question_button:

                try:
                    qa_context = (
                        build_event_qa_context(
                            filtered_events
                        )
                    )

                    with st.spinner(
                        "Analyzing your question..."
                    ):

                        answer = (
                            answer_event_question(
                                qa_context,
                                event_question,
                            )
                        )

                except Exception as error:

                    st.error(
                        f"Unable to answer question: "
                        f"{error}"
                    )

                else:

                    st.session_state[
                        "event_qa_answer"
                    ] = answer

                    st.session_state[
                        "event_qa_question"
                    ] = event_question


            if (
                "event_qa_answer"
                in st.session_state
            ):

                st.markdown("#### Answer")

                st.write(
                    st.session_state[
                        "event_qa_answer"
                    ]
                )        

            # -------------------------------------------------
            # Events by Type
            # -------------------------------------------------

            event_counts = get_event_counts_by_type(
                filtered_events
            )

            event_chart = px.bar(
                event_counts,
                x="event_name",
                y="event_count",
                title="Events by Type",
                labels={
                    "event_name": "Event Type",
                    "event_count": "Number of Events",
                },
            )

            st.plotly_chart(
                event_chart,
                width="stretch",
            )

            # -------------------------------------------------
            # Daily Activity
            # -------------------------------------------------

            daily_activity = (
                get_daily_event_activity(
                    filtered_events
                )
            )

            activity_chart = px.line(
                daily_activity,
                x="event_date",
                y="event_count",
                markers=True,
                title="Daily Product Activity",
                labels={
                    "event_date": "Date",
                    "event_count": "Events",
                },
            )

            st.plotly_chart(
                activity_chart,
                width="stretch",
            )

            # -------------------------------------------------
            # Raw Event Data
            # -------------------------------------------------

            st.subheader("Event Data")

            st.dataframe(
                filtered_events,
                width="stretch",
                hide_index=True,
            )


# =========================================================
# WEATHER FORECASTS TAB
# =========================================================

with weather_tab:

    st.header("Weather Forecasts")

    if weather_df.empty:

        st.warning(
            "No weather data found. "
            "Run: python app/weather_ingestion.py"
        )

    else:

        # KPI cards
        metric_1, metric_2, metric_3 = st.columns(3)

        metric_1.metric(
            "Forecast Points",
            len(weather_df),
        )

        metric_2.metric(
            "Average Temperature",
            (
                f"{weather_df['temperature_c'].mean():.1f} °C"
            ),
        )

        metric_3.metric(
            "Total Precipitation",
            (
                f"{weather_df['precipitation_mm'].sum():.1f} mm"
            ),
        )

        # Temperature chart
        temperature_chart = px.line(
            weather_df,
            x="forecast_time",
            y="temperature_c",
            markers=True,
            title="Temperature Forecast",
            labels={
                "forecast_time": "Forecast Time",
                "temperature_c": "Temperature (°C)",
            },
        )

        st.plotly_chart(
            temperature_chart,
            width="stretch",
        )

        # Precipitation chart
        precipitation_chart = px.bar(
            weather_df,
            x="forecast_time",
            y="precipitation_mm",
            title="Precipitation Forecast",
            labels={
                "forecast_time": "Forecast Time",
                "precipitation_mm": "Precipitation (mm)",
            },
        )

        st.plotly_chart(
            precipitation_chart,
            width="stretch",
        )

        # Raw weather data
        st.subheader("Weather Data")

        st.dataframe(
            weather_df,
            width="stretch",
            hide_index=True,
        )