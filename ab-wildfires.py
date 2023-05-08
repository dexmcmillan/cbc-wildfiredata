import geopandas
import pandas as pd
import requests

active_fires_ab = "https://services.arcgis.com/Eb8P5h4CJk8utIBz/ArcGIS/rest/services/Active_Wildfire_Perimeters_Simplified_view/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token="

data = geopandas.read_file(active_fires_ab)

print(data)
timestamp = pd.to_datetime(requests.get(active_fires_ab).headers["Last-Modified"])
data["FIRENUMBER"] = timestamp

data.columns = data.columns.str.strip()
data["FIRENUMBER"] = data["FIRENUMBER"].astype(str).str.strip()
    
data.to_csv(f'data/alberta/ab-{str(timestamp).replace(":", "").replace("+0000", "")}.csv', mode='w')