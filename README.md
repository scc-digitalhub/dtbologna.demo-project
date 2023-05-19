# DigitalTwin Bologna - Demo project

A demo project for a simple data pipeline over traffic measures.

## Overview

The demo implements a simple project which will:

- fetch traffic data from an external source
- analyze and transform measures
- produce usable datasets
- expose services based on such datasets: API, Dashboard

Additionally, the ML component will:

- train a ML model to predict traffic flows
- develop an ML API
- expose an interactive console towards the ML API

Please open `docs/` to find additional documentation and a presentation.

## Technologies

The project is based on the DigitalHub stack and uses:

- MLRun for ML workflows
- Minio (S3) for artifact storage
- PostgresSQL for operational data storage
- Nuclio as serverless environment
- Streamlit as dashboard framework
- Jupyter Notebook as interactive dev environment

## Project structure

The project code is fully stored in the git repository:

- `project.yaml` describes the project
- `demo.ipynb` is the notebook
- `pipeline.py` is the main project workflow
- `src/` contains the source code
- `dashboard/` contains the dashboard code

## Traffic flow project

The project leverages the open data reporting vehicular traffic in the city of Bologna (available from <https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets/rilevazione-flusso-veicoli-tramite-spire-anno-2023>) to develop both _data services_ and _ML services_.

The general steps are:

1. Collect the data and store the raw datasets
2. Process the datasets to apply transformations and obtain suitable data
3. Expose processed datasets as _data services_ to enable programmatic consumption
4. Expose a user-friendly _data dashboard_ to enable data exploration and visualization for non-technical users
5. Train, evaluate and deploy a predictive ML model

### 1. Collect the data

The first step in the workflow is data collection: from the remote repository a dedicated _function_ will download the CSV, check the raw material and then persist a valid data artifact inside the storage.

```python
import mlrun
import pandas as pd
import requests

URL = "https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets/rilevazione-flusso-veicoli-tramite-spire-anno-2023/exports/csv?lang=it&timezone=Europe%2FRome&use_labels=true&delimiter=%3B"

@mlrun.handler(outputs=["dataset"])
def downloader():
    # download raw
    filename = "raw.csv"
    with requests.get(URL) as r:
        with open(filename, "wb") as f:
            f.write(r.content)

    # read and rewrite to normalize and export as data
    df = pd.read_csv(filename, sep=";")
    return df
```

As we can see from code, there is no need to handle I/O, connections and persistance. The function is pure business code.

### 2. Process the data

From the raw material downloaded at step 1. two different dedicated functions will:

- extract information about the _spire_ (for example `id`,`geolocation`,`address`, `name`...)
- extract measures for traffic as recorded by _spire_ (e.g. `time`,`value`)

The function code is again focusing only on the business part, which is handling the transformations.

### 3. Expose datasets as API

TBD

### 4. Dashboard

The dashboard is developed in Python by using the Streamlit framework, which enables us in writing a developer friendly script which will expose a series of data and interactive widgets via a nice web interface.

The code in `dashboard` implements 3 different views, which will expose :

- a general dashboard with current and generic information
- a general view on the various _spire_ and their location and status
- a detailed **interactive** view for every _spira_, with current and historical data

The dashboard is exposed as _data service_ via the creation of a custom image, which is then deployed and exposed in Kubernetes by the platform.

The function descriptor is as follows

```


```

### 5. ML predictive model

TBD
