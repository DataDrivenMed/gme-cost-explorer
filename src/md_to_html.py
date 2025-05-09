import markdown, glob, datetime as dt, pathlib

md_path = sorted(glob.glob("digests/gme_digest_*.md"))[-1]
html_body = markdown.markdown(open(md_path).read(), extensions=["tables"])

html = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8">
<title>GME Cost‑Report Explorer</title>
<link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
</head><body>
<h1>GME Cost‑Report Explorer</h1>
<p><em>Last updated {dt.datetime.utcnow():%Y-%m-%d %H:%M UTC}</em></p>
{html_body}
</body></html>"""

out = pathlib.Path("docs/index.html")
out.parent.mkdir(exist_ok=True)
out.write_text(html)
print("Wrote", out)
