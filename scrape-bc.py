import geopandas
import pandas as pd
import requests

active_fires_bc = "https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/BCWS_FirePerimeters_PublicView/FeatureServer/0/query?returnGeometry=true&where=FIRE_STATUS%20%3C%3E%20%27Out%27&outSR=4326&outFields=*&inSR=4326&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&geometryPrecision=6&resultType=tile&f=geojson"

data = geopandas.read_file(active_fires_bc, engine="fiona")

timestamp = pd.to_datetime(requests.get(active_fires_bc).headers["Last-Modified"])
data["FIRE_NUMBER"] = timestamp

data.columns = data.columns.str.strip()
data["FIRE_NUMBER"] = data["FIRE_NUMBER"].astype(str).str.strip()
    
data.to_csv(f'data/bc/bc-{str(timestamp).replace(":", "").replace("+0000", "")}.csv', mode='w')