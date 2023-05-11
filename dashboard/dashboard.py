import streamlit as st
import pandas as pd
import numpy as np
import mlrun
import datetime
import pydeck as pdk
import pytz

DATASET_SPIRE_URI = "../dataset-spire.parquet"
DATASET_MEASURES_URI = "../dataset-measures.parquet"

DATASET_DATA_KEY = "store://datasets/demobo/download-data-downloader_dataset#0:latest"
DATASET_SPIRE_KEY = (
    "store://datasets/demobo/process-spire-process_dataset-spire#0:latest"
)
DATASET_MEASURES_KEY = (
    "store://datasets/demobo/process-measures-process_dataset-measures#0:latest"
)


@st.cache_data
def load_data(uri):
    print("loading data for {}".format(uri))
    data = pd.read_parquet(uri)
    return data


@st.cache_data
def fetch_data(key):
    print("loading mlrun data item for {}".format(key))
    return mlrun.get_dataitem(key).as_df()


def map_data(df):
    print("prepare data for map")
    df["longitude"] = df["longitudine"]
    df["latitude"] = df["latitudine"]
    df["key"] = df["codice spira"].astype(str)

    return df


# mlrun.set_environment(MLRUN_API, username="jovyan")
st.title("Spire dashboard")

# load data
data_load_state = st.text("Loading data...")
data_spire = map_data(load_data(DATASET_SPIRE_URI))
data_measures = load_data(DATASET_MEASURES_URI)
# data_spire = map_data(fetch_data(DATASET_SPIRE_KEY))
# data_measures = fetch_data(DATASET_MEASURES_KEY)

data_measures["timestamp"] = pd.to_datetime(
    data_measures["time"], format="%Y%m%d %H:%M:%S"
)

# display
data_load_state.text("All data loaded.")

st.subheader("Measures data")
count = len(data_measures)
latest_timestamp = data_measures["timestamp"].max()
first_timestamp = data_measures["timestamp"].min()
st.write("count: {}".format(count))
st.write("last updated: {}".format(latest_timestamp))
st.write("date interval available {} -> {}".format(first_timestamp, latest_timestamp))


selected_timestamp = latest_timestamp
last_date = datetime.datetime.fromtimestamp(
    selected_timestamp.timestamp(), tz=pytz.timezone("UTC")
)
first_date = datetime.datetime.fromtimestamp(
    first_timestamp.timestamp(), tz=pytz.timezone("UTC")
)
st.divider()
selected_date = st.date_input(
    "Select date",
    last_date.date(),
    max_value=last_date.date(),
    min_value=first_date.date(),
)
selected_time = st.time_input("time", last_date.time(), step=3600)

st.write("Selected date {}: {}".format(selected_date, selected_time))

selected_timestamp = datetime.datetime.combine(selected_date, selected_time)

if selected_timestamp != None:
    data_samples = data_measures[data_measures["timestamp"] == selected_timestamp]
    data_samples["key"] = data_samples["codice spira"].astype(str)

    df_spire = data_spire[["key", "longitudine", "latitudine", "Nome via"]].set_index(
        "key"
    )
    df_samples = data_samples[["key", "value"]].set_index("key")

    chart_data = df_spire.join(df_samples).reset_index(drop=False).dropna()
    chart_data_ex = chart_data[chart_data["value"] < 100]

    st.caption("2D scatterplot")
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=44.49,
                longitude=11.35,
                zoom=11,
                pitch=0,
                auto_highlight=True,
            ),
            tooltip={"text": "{Nome via}: {value}"},
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=chart_data,
                    get_position="[longitudine, latitudine]",
                    get_radius=50,
                    pickable=True,
                    auto_highlight=True,
                    get_fill_color=["(value * 255) / 1000", 90, 100, 255],
                ),
            ],
        )
    )

    st.caption("3D Columns plot")
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=44.49,
                longitude=11.35,
                zoom=11,
                pitch=50,
                auto_highlight=True,
            ),
            tooltip={"text": "{Nome via}: {value}"},
            layers=[
                pdk.Layer(
                    "ColumnLayer",
                    data=chart_data,
                    get_position="[longitudine, latitudine]",
                    radius=30,
                    elevation_scale=1,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                    auto_highlight=True,
                    get_elevation="value",
                    get_fill_color=["(value * 255) / 1000", 90, 100, 255],
                ),
            ],
        )
    )

    st.subheader("Raw data")
    st.dataframe(data_samples)
