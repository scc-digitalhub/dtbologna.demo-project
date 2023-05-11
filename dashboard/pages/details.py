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

st.header('Details data')
selected_spire = st.selectbox(
    "Please select a spire",
    data_spire['codice'].astype(int)
)

cur_data = data_spire[data_spire['codice'] == selected_spire]
if len(cur_data) > 0:

    cur_spire = cur_data.iloc[0]

    st.caption("Details")
    col1, col2 = st.columns([2, 10])
    with col1:
        name = "### #{}".format(selected_spire)
        st.write(name)

    with col2:
        address = "### {} *direzione* {}".format(
            cur_spire['Nome via'], cur_spire['direzione'])
        st.write(address)

    st.caption("Position")
    st.map(cur_data)

    st.caption("Raw data")
    st.json(cur_spire.to_json())

    # data
    cur_measures = data_measures[data_measures['codice spira']
                                 == cur_spire['codice spira']]
    cur_measures['timestamp'] = pd.to_datetime(
        cur_measures['time'], format='%Y%m%d %H:%M:%S')

    today = datetime.date.today()
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(30)
    end_date = today
    start_time = datetime.time(00, 00)
    end_time = datetime.time(23, 59)

    dcol1, dcol2 = st.columns(2)
    with dcol1:
        start_date = st.date_input("Start date", now - datetime.timedelta(30))
        start_time = st.time_input('start time', start_time)
    with dcol2:
        end_date = st.date_input("End date", today)
        end_time = st.time_input('end time', end_time)

    start_timestamp = datetime.datetime.combine(start_date, start_time)
    end_timestamp = datetime.datetime.combine(end_date, end_time)

    st.write("Interval {}  -> {}".format(start_timestamp, end_timestamp))

    idf = cur_measures[(cur_measures['timestamp'] >= start_timestamp)
                       & (cur_measures['timestamp'] <= end_timestamp)]

    # measures
    st.caption("Raw measures")

    st.dataframe(idf)

    # graph
    st.line_chart(idf, x='time', y='value')
