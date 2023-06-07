import geopandas
import pandas as pd
import requests

active_fires_ab = "https://services.arcgis.com/Eb8P5h4CJk8utIBz/arcgis/rest/services/Active_Wildfire_Perimeters_Simplified_view/FeatureServer/0/query?f=json&resultOffset=0&resultRecordCount=4000&where=1=1&orderByFields=OBJECTID&outFields=*&resultType=tile&spatialRel=esriSpatialRelIntersects&geometryType=esriGeometryEnvelope&defaultSR=102100"

data = geopandas.read_file(active_fires_ab, engine="fiona")

timestamp = pd.to_datetime(requests.get(active_fires_ab).headers["Last-Modified"])
data["FIRENUMBER"] = timestamp

data.columns = data.columns.str.strip()
data["FIRENUMBER"] = data["FIRENUMBER"].astype(str).str.strip()
    
data.to_csv(f'data/alberta/ab-{str(timestamp).replace(":", "").replace("+0000", "")}.csv', mode='w')