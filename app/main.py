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