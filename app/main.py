import plotly.express as px
import streamlit as st

from dashboard_data import (
    get_daily_event_activity,
    get_event_counts_by_type,
    load_events_dataframe,
    load_weather_dataframe,
)


st.set_page_config(
    page_title="DataSense AI",
    layout="wide",
)


st.title("DataSense AI")
st.caption(
    "Interactive analytics for product events "
    "and weather data."
)


events_df = load_events_dataframe()
weather_df = load_weather_dataframe()


product_tab, weather_tab = st.tabs(
    [
        "Product Events",
        "Weather Forecasts",
    ]
)


with product_tab:

    st.header("Product Events")

    if events_df.empty:
        st.warning(
            "No product event data found. "
            "Run: python app/ingestion.py"
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


            st.subheader("Event Data")

            st.dataframe(
                filtered_events,
                width="stretch",
                hide_index=True,
            )            



with weather_tab:

    st.header("Weather Forecasts")

    if weather_df.empty:

        st.warning(
            "No weather data found. "
            "Run: python app/weather_ingestion.py"
        )

    else:

        metric_1, metric_2, metric_3 = st.columns(3)

        metric_1.metric(
            "Forecast Points",
            len(weather_df),
        )

        metric_2.metric(
            "Average Temperature",
            f"{weather_df['temperature_c'].mean():.1f} °C",
        )

        metric_3.metric(
            "Total Precipitation",
            (
                f"{weather_df['precipitation_mm'].sum():.1f} mm"
            ),
        )            


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


        st.subheader("Weather Data")

        st.dataframe(
            weather_df,
            width="stretch",
            hide_index=True,
        )