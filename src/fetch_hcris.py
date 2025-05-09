import requests, pathlib, json, datetime as dt, itertools

DATA = pathlib.Path("data"); DATA.mkdir(exist_ok=True)
today = dt.date.today()

def fetch_chunk(offset=0, limit=50000):
    base = "https://data.cms.gov/data-api/v1/dataset/ynj2-r877/data"
    query = (
        f"?$limit={limit}&$offset={offset}"
        "&worksheet_code=E&worksheet_code=E-1"
        "&report_period_end>=2022-01-01"
    )
    return requests.get(base + query, timeout=60).json()

rows = list(itertools.chain.from_iterable(
    fetch_chunk(o) for o in range(0, 200000, 50000)
))
out = DATA / f"hcris_raw_{today}.json"
out.write_text(json.dumps(rows, indent=2))
print("Saved", out, len(rows), "rows")
