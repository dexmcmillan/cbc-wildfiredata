import pandas as pd
import datawrappergraphics
import glob
import datetime as dt
import os

csvfiles = glob.glob("data/*.csv")

dfs = []

for file in csvfiles:
    df = pd.read_csv(file)
    
    dfs.append(df)
    
data = pd.concat(dfs)

data["timestamp"] = pd.to_datetime(data["timestamp"])

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

data["firename"] = data["firename"] + " (" + data["province/territory"] + ")"

data["color"] = data["stage_of_control"].replace({
    "Out of control": "#C42127",
    "Under control": "#29414F",
    "Extinguished": "#cccccc",
    "Being held": "#29414F"
})

most_recent_file = pd.read_csv(max(csvfiles, key=os.path.getctime))

try:
    active_fires_list = most_recent_file.loc[(data["stage_of_control"] != "OC"), "firename"]
except IndexError:
    active_fires_list = []

out_of_control = len(data.loc[data["firename"].isin(active_fires_list), "firename"].unique())

pivot = data.pivot(columns="firename", index="timestamp", values="hectares")
# pivot = round(pivot.pct_change()*100, 2)

for label, i in pivot.iteritems():
    if pivot[label].max() == pivot[label].min() or pivot[label].max() <= 100:
        pivot = pivot.drop(columns=label)

chart = datawrappergraphics.Chart("0XCbi").data(pivot).head(f"Wildfires in Canada since June 14").deck(f"There are currently <b>{out_of_control}</b> fires that are classified as <span style='background-color:#C42127; color:white;padding:1px 3px;border-radius:2px'>out of control</span>. Chart shows wildfires that have increased or decreased since June 14, and are currently larger than 100 hectares.")

meta_obj = {k: data.set_index("firename").at[k,"color"].max() for k in pivot.columns}

largest_fire = data.sort_values("hectares", ascending=False).reset_index().at[0,"firename"]

meta_obj[largest_fire] = "#E06618"

chart.metadata["metadata"]["visualize"]["custom-colors"] = meta_obj

chart.set_metadata().publish()