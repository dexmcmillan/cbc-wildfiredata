import pandas as pd
import datawrappergraphics
import glob
import datetime as dt

csvfiles = glob.glob("data/*.csv")

dfs = []

for file in csvfiles:
    df = pd.read_csv(file)
    
    dfs.append(df)
    
data = pd.concat(dfs)

data["timestamp"] = pd.to_datetime(data["timestamp"]).dt.tz_convert(None)

print(data)

data = data.loc[~data["agency"].isin(["ak", "conus", "pc"]), :]

data["stage_of_control"] = data["stage_of_control"].str.strip().replace({
    "OC": "Out of control",
    "UC": "Under control",
    "EX": "Extinguished",
    "BH": "Being held"
})

data["province/territory"] = data["agency"].replace({
    "sk": "Saskatchewan",
    "ab": "Alberta",
    "bc": "British Columbia",
    "on": "Ontario",
    "ns": "Nova Scotia",
    "yt": "Yukon",
    "nt": "Northwest Territories",
    "qc": "Quebec",
    "mb": "Manitoba",
    "nl": "Newfoundland and Labrador",
    "pe": "Prince Edward Island"
})

pivot = data.pivot(columns="firename", index="timestamp", values="hectares")
# pivot = round(pivot.pct_change()*100, 2)

chart = datawrappergraphics.Chart("0XCbi").data(pivot)

meta_obj = {k: "#cccccc" for k in pivot.columns}

chart.metadata["metadata"]["visualize"]["custom-colors"] = meta_obj

chart.set_metadata()