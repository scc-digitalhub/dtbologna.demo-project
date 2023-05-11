import streamlit as st
import pandas as pd
import numpy as np
import mlrun
import datetime
import pydeck as pdk

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


st.title("Spire overview")

# load data
data_load_state = st.text("Loading data...")
data_spire = map_data(load_data(DATASET_SPIRE_URI))
# data_spire = map_data(fetch_data(DATASET_SPIRE_KEY))


# display
data_load_state.text("All data loaded.")


st.write("Found {} sensors".format(len(data_spire)))

st.subheader("Map data")
st.map(data_spire)


st.subheader("Raw data")
st.dataframe(data_spire)
