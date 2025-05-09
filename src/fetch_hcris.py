# src/fetch_hcris.py
import requests, pathlib, json, datetime as dt

DATA   = pathlib.Path("data"); DATA.mkdir(exist_ok=True)
today  = dt.date.today()
base   = "https://data.cms.gov/data-api/v1/dataset/ynj2-r877/data"

where  = "worksheet_code in ('E','E-1') and report_period_end >= '2022-01-01'"
limit  = 10000          # CMS max page size

rows   = []
offset = 0
while True:
    params = {"$limit": limit, "$offset": offset, "$where": where}
    r = requests.get(base, params=params, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"CMS API error {r.status_code}: {r.text[:200]}")
    page = r.json()
    if not page:
        break
    rows.extend(page)
    offset += limit
    print(f"Fetched {len(page):>5} rows  (total {len(rows)})")

out = DATA / f"hcris_raw_{today}.json"
out.write_text(json.dumps(rows, indent=2))
print("Saved", out, len(rows), "rows")
