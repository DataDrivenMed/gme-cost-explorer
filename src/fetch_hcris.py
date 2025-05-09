# src/fetch_hcris.py  – CMS data‑api v1, dataset 44060663…
import os, requests, pathlib, json, datetime as dt

TOKEN  = os.getenv("CMS_APP_TOKEN")          # set via GitHub Secret
HEAD   = {"X-API-KEY": TOKEN} if TOKEN else {}

DATA   = pathlib.Path("data"); DATA.mkdir(exist_ok=True)
today  = dt.date.today()

DATASET_ID = "44060663-47d8-4ced-a115-b53b4c270acb"
BASE = f"https://data.cms.gov/data-api/v1/dataset/{DATASET_ID}/data"

LIMIT  = 50000
offset = 0
rows   = []

WHERE  = "worksheet_code in ('E','E-1') and report_period_end >= '2022-01-01'"

while True:
    params = {"limit": LIMIT, "offset": offset, "where": WHERE}
    r = requests.get(BASE, params=params, headers=HEAD, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"CMS API {r.status_code}: {r.text[:200]}")
    page = r.json()
    if not page:
        break
    rows.extend(page)
    offset += LIMIT
    print(f"Fetched {len(page):>5} rows  (total {len(rows)})")

out = DATA / f"hcris_raw_{today}.json"
out.write_text(json.dumps(rows, indent=2))
print("Saved", out, len(rows), "rows")
