import pandas as pd, json, glob, pathlib, datetime as dt

raw_path = sorted(glob.glob("data/hcris_raw_*.json"))[-1]
df = pd.read_json(raw_path)

MAP = {("E-1","31","1"): "dgme_total",
       ("E-1","31","3"): "dgme_fte_cap",
       ("E",  "4", "1"): "ime_total",
       ("E",  "3", "1"): "ime_weighted_fte"}

df = df[df.apply(lambda r: (r.worksheet_code, r.line, r.column) in MAP, axis=1)]
df["metric"] = df.apply(lambda r: MAP[(r.worksheet_code, r.line, r.column)], axis=1)

pivot = df.pivot_table(index=["provider_number","report_period_end"],
                       columns="metric", values="value", aggfunc="first").reset_index()
pivot["report_period_end"] = pd.to_datetime(pivot["report_period_end"]).dt.date
pivot.columns.name = None

out = pathlib.Path("data/gme_clean_latest.json")
pivot.to_json(out, orient="records", indent=2)
print("Wrote", out, len(pivot), "records")
