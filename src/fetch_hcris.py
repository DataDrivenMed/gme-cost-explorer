# src/fetch_hcris.py  – Socrata resource endpoint version
import requests, pathlib, json, datetime as dt

DATA = pathlib.Path("data"); DATA.mkdir(exist_ok=True)
today = dt.date.today()

BASE = "https://data.cms.gov/resource/ynj2-r877.json"
WHERE = "worksheet_code in ('E','E-1') and report_period_end >= '2022-01-01'"
LIMIT = 50000    # Socrata max is 50k

rows  = []
offset = 0
while True:
    params = {"$limit": LIMIT, "$offset": offset, "$where": WHERE}
    r = requests.get(BASE, params=params, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"CMS API error {r.status_code}: {r.text[:200]}")
    page = r.json()
    if not page:
        break        # no more pages
    rows.extend(page)
    offset += LIMIT
    print(f"Fetched {len(page):>5} rows  (total {len(rows)})")

out = DATA / f"hcris_raw_{today}.json"
out.write_text(json.dumps(rows, indent=2))
print("Saved", out, len(rows), "rows")
