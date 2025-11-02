import json, math, glob, os
import pandas as pd

# find file starting with GC
in_path = sorted(glob.glob("../data-raw/full/GC*.json"))[0]


base = os.path.basename(in_path)
station = "GC"


with open(in_path) as f:
    d = json.load(f)

def points(name):
    return d["observationalGraphs"][name]["dataConfig"]["series"]["groups"][0]["points"]

keys = [
    "wind", "pressure", "wind-gust", "rainfall", "temperature",
    "apparent-temperature", "cloud", "delta-t", "dew-point", "humidity"
]

series = {}
for k in keys:
    series[k] = points(k)
    # series = {k: points(k) for k in keys}

data_map = {}
for k, lst in series.items():
    for p in lst:
        t = p["x"]
        e = data_map.setdefault(t, {"timestamp": t})

        match k:
            case "wind":
                e[f"{station}_wind"] = p.get("y")
                e[f"{station}_wind_direction"] = p.get("direction")
            case "pressure":
                e[f"{station}_pressure"] = p.get("y")
            case "wind-gust":
                e[f"{station}_wind_gust"] = p.get("y")
            case "rainfall":
                e[f"{station}_rain"] = p.get("y")
            case "temperature":
                e[f"{station}_temp"] = p.get("y")
            case "apparent-temperature":
                e[f"{station}_apparent_temp"] = p.get("y")
            case "cloud":
                e[f"{station}_cloud_oktas"] = p.get("y")
            case "delta-t":
                e[f"{station}_delta_t"] = p.get("y")
            case "dew-point":
                e[f"{station}_dew_point"] = p.get("y")
            case "humidity":
                e[f"{station}_humidity"] = p.get("y")

# sin/cos for wind direction
for t, e in data_map.items():
    deg = e.get(f"{station}_wind_direction")
    if deg is not None:
        rad = deg * math.pi / 180.0
        e[f"{station}_wind_dir_cos"] = math.cos(rad)
        e[f"{station}_wind_dir_sin"] = math.sin(rad)

# flatten sorted
out = [data_map[t] for t in sorted(data_map.keys())]


out_path = "../data-processed/base/" + base.replace(".json", "_processed.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

# convert to dataframe
df = pd.DataFrame(out)

# save parquet file
parquet_path = "../data-processed/base/" + station + "_2025-11-01.parquet"
df.to_parquet(parquet_path, index=False)

print("saved:")
