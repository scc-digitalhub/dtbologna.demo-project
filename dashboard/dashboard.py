import streamlit as st
import pandas as pd
import numpy as np
import mlrun
import datetime

# DATASET_SPIRE_URI = "store://datasets/demobo/process-spire-process_dataset-spire#0:latest"
DATASET_SPIRE_URI = "../dataset-spire.parquet"
DATASET_MEASURES_URI = "../dataset-measures.parquet"


@st.cache_data
def load_data(uri):
    print("loading data for {}".format(uri))
    data = pd.read_parquet(uri)
    return data


def map_data(df):
    print("prepare data for map")
    df['longitude'] = df['longitudine']
    df['latitude'] = df['latitudine']
    return df


st.title('Spire parcheggi')

# load data
data_load_state = st.text('Loading data...')
data_spire = map_data(load_data(DATASET_SPIRE_URI))
data_measures = load_data(DATASET_MEASURES_URI)

# display
data_load_state.text('All data loaded.')

st.subheader('Raw data')
st.dataframe(data_spire)
st.dataframe(data_measures)

st.subheader('Map data')

st.map(data_spire)

st.divider()
