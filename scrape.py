import pandas as pd
import requests

active_fires = "https://cwfis.cfs.nrcan.gc.ca/downloads/activefires/activefires.csv"

data = pd.read_csv(active_fires)
timestamp = pd.to_datetime(requests.get(active_fires).headers["Last-Modified"])
data["timestamp"] = timestamp

data.columns = data.columns.str.strip()
data["firename"] = data["firename"].str.strip()
    
data.to_csv(f'data/{str(timestamp).replace(":", "").replace("+0000", "")}.csv', mode='w')