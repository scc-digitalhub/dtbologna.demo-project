
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
