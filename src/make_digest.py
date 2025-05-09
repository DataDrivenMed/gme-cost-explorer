import json, datetime as dt, pathlib

today = dt.date.today()
pathlib.Path("digests").mkdir(exist_ok=True)

rows = json.load(open("data/gme_clean_latest.json"))
rows = sorted(rows, key=lambda r: r.get("dgme_total",0), reverse=True)[:300]

lines = [f"# GME Cost‑Report Explorer – {today}", "",
         "| CCN | FY End | DGME $ | IME $ | FTE Cap | IME Weighted FTE |",
         "|-----|--------|-------|-------|---------|------------------|"]

for r in rows:
    lines.append(
        f"| {r['provider_number']} | {r['report_period_end']}"
        f" | ${r.get('dgme_total',0):,.0f}"
        f" | ${r.get('ime_total',0):,.0f}"
        f" | {r.get('dgme_fte_cap','')}"
        f" | {r.get('ime_weighted_fte','')} |"
    )

out = pathlib.Path(f"digests/gme_digest_{today}.md")
out.write_text("\n".join(lines))
print("Wrote", out)
