import pandas as pd
import geopandas
from datetime import datetime

perimeters_url = "/vsicurl/https://cwfis.cfs.nrcan.gc.ca/downloads/hotspots/perimeters.shp"

data = geopandas.read_file(perimeters_url)

timestamp = datetime.now()
data["timestamp"] = timestamp

data.columns = data.columns.str.strip()
    
data.to_csv(f'data/perimeters/{str(timestamp).replace(":", "").replace("+0000", "")}.csv', mode='w')