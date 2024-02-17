import altair as alt
import pandas as pd
import streamlit as st
from millify import millify

# Make most out of the space available
st.set_page_config(layout="wide")

# Open dataset as a pandas dataframe
df = pd.read_csv(
    "./SeoulBikeData.csv",
    encoding="unicode_escape",
    parse_dates=["Date"],
    date_format="%d/%m/%Y",
)


def normalize_column(col) -> None:
    max_value = df[col].max()
    df["Normalized" + " " + col] = df[col].div(max_value)


# Metrics and a line chart for rented bike count
container1 = st.container()
col11, col12 = container1.columns([0.15, 0.85])
# Per day grouping
grp = df.groupby("Date").sum().reset_index()

with col11:
    total_rented_bikes = df["Rented Bike Count"].sum()
    hours_ridden = df["Hour"].sum()
    st.metric(
        label="Total Bikes Rented", value=millify(total_rented_bikes, precision=2)
    )
    st.metric(label="Max Bikes Rented Per Day", value=grp["Rented Bike Count"].max())
with col12:
    st.line_chart(grp, x="Date", y="Rented Bike Count")

# Bar chart & a pie chart for Seasons
container2 = st.container(border=True)
col21, col22 = container2.columns([0.6, 0.4])
with col21:
    st.bar_chart(df, x="Seasons", y="Rented Bike Count")
with col22:
    grp_by_seasons = df.groupby("Seasons")["Rented Bike Count"].sum().reset_index()
    print(grp_by_seasons)
    ac = (
        alt.Chart(grp_by_seasons)
        .mark_arc()
        .encode(
            theta="Rented Bike Count",
            color="Seasons",
        )
    )
    st.altair_chart(ac)

# Scatter plot for rainfall and snowfall in normalized form
container3 = st.container(border=True)
with container3:
    normalize_column("Rainfall(mm)")
    normalize_column("Snowfall (cm)")
    bubble_size = st.slider("Bubble Size", 0, 200, 50)
    st.scatter_chart(
        df,
        x="Rented Bike Count",
        y=["Normalized Rainfall(mm)", "Normalized Snowfall (cm)"],
        size=bubble_size,
        color=["#348abd", "#e24a33"],
    )
# Scatter plot for rainfall only
container3_1 = st.container()
with container3_1:
    st.scatter_chart(df, x="Rainfall(mm)", y="Rented Bike Count")

# Bar chart representing distribution according to holiday
container4 = st.container(border=True)
col41, col42, col43 = container4.columns(3)
with col41:
    st.bar_chart(df, x="Holiday", y="Rented Bike Count")
# Scatter plot: Wind speed & Solar Radiation distribution
with col42:
    st.scatter_chart(
        df,
        x="Wind speed (m/s)",
        y="Rented Bike Count",
    )
with col43:
    st.scatter_chart(
        df,
        x="Solar Radiation (MJ/m2)",
        y="Rented Bike Count",
    )

# Bubble plot represting 3 attributes
container5 = st.container(border=True)
with container5:
    ac = (
        alt.Chart(df, height=600)
        .mark_point()
        .encode(x="Humidity(%)", y="Visibility (10m)", size="Solar Radiation (MJ/m2)")
    )
    st.altair_chart(ac, use_container_width=True)

# Group by hour and sum
grp_by_hour = df.groupby("Hour")["Rented Bike Count"].sum().reset_index()
container6 = st.container()
with container6:
    st.line_chart(grp_by_hour, x="Hour", y="Rented Bike Count")
