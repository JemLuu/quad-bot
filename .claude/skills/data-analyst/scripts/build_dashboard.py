#!/usr/bin/env python3
"""Render a self-contained HTML dashboard from a JSON analysis payload.

Usage:
    python3 build_dashboard.py <input.json> [output.html]

Charts are passed straight through to Chart.js (loaded from a CDN at view
time), so the caller controls chart types and styling. Standard library only —
no third-party packages required.

Input JSON schema (only "title" is required):
{
  "title":     "Running analysis",                 # required
  "subtitle":  "Last 12 weeks · 42 runs",
  "footnote":  "Source: Strava",
  "kpis":   [ {"label": "Total distance",
               "value": "312 mi",
               "sub":   "+8% vs prior block"} ],
  "insights": [ "You run 82% easy — right in the 80/20 zone." ],
  "charts": [ {
      "id":          "weekly",            # unique id
      "type":        "bar",               # any Chart.js type
      "title":       "Weekly volume",
      "description": "Distance per week with a 4-week average",
      "span":        2,                   # 1 (default) or 2 grid columns
      "data":    { ...Chart.js data... }, # required
      "options": { ...Chart.js options... }
  } ]
}
"""
import html
import json
import sys
from pathlib import Path

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
  :root{--bg:#0f1419;--card:#1a222c;--ink:#e7edf3;--mut:#8aa0b2;--acc:#fc5200;--line:#27323e}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
  header{padding:32px 28px 4px;max-width:1200px;margin:0 auto}
  h1{margin:0;font-size:26px}
  .sub{color:var(--mut);margin-top:4px}
  .wrap{padding:8px 28px 48px;max-width:1200px;margin:0 auto}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin:18px 0 8px}
  .kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
  .kpi .l{color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.6px}
  .kpi .v{font-size:26px;font-weight:700;margin-top:6px}
  .kpi .s{color:var(--mut);font-size:12px;margin-top:4px}
  .insights{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:14px;padding:16px 20px;margin-top:18px}
  .insights h3{margin:0 0 10px;font-size:16px}
  .insights ul{margin:0;padding-left:18px}.insights li{margin:6px 0}
  .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:18px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
  .card.span2{grid-column:1 / -1}
  .card h3{margin:0 0 2px;font-size:16px}
  .card p.d{margin:0 0 12px;color:var(--mut);font-size:13px}
  .canvas-wrap{position:relative;height:300px}
  footer{color:var(--mut);font-size:12px;padding:24px 28px;text-align:center}
  @media(max-width:760px){.grid{grid-template-columns:1fr}.card.span2{grid-column:auto}}
</style>
</head>
<body>
<header><h1>__TITLE__</h1><div class="sub">__SUBTITLE__</div></header>
<div class="wrap">
  <div class="kpis" id="kpis"></div>
  <div class="insights" id="insightsBox" style="display:none"><h3>Highlights</h3><ul id="insights"></ul></div>
  <div class="grid" id="grid"></div>
</div>
<footer>__FOOTNOTE__</footer>
<script>
const PAYLOAD = __DATA__;
Chart.defaults.color = "#8aa0b2";
Chart.defaults.borderColor = "#27323e";
Chart.defaults.font.family = "-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif";

const kpiBox = document.getElementById("kpis");
(PAYLOAD.kpis || []).forEach(k => {
  const d = document.createElement("div"); d.className = "kpi";
  const l = document.createElement("div"); l.className = "l"; l.textContent = k.label || ""; d.appendChild(l);
  const v = document.createElement("div"); v.className = "v"; v.textContent = (k.value != null ? k.value : ""); d.appendChild(v);
  if (k.sub) { const s = document.createElement("div"); s.className = "s"; s.textContent = k.sub; d.appendChild(s); }
  kpiBox.appendChild(d);
});
if (!(PAYLOAD.kpis || []).length) kpiBox.remove();

const ins = PAYLOAD.insights || [];
if (ins.length) {
  document.getElementById("insightsBox").style.display = "";
  const ul = document.getElementById("insights");
  ins.forEach(t => { const li = document.createElement("li"); li.textContent = t; ul.appendChild(li); });
}

const grid = document.getElementById("grid");
(PAYLOAD.charts || []).forEach((c, i) => {
  try {
    const card = document.createElement("div");
    card.className = "card" + (c.span === 2 ? " span2" : "");
    const h = document.createElement("h3"); h.textContent = c.title || ("Chart " + (i + 1)); card.appendChild(h);
    if (c.description) { const p = document.createElement("p"); p.className = "d"; p.textContent = c.description; card.appendChild(p); }
    const cw = document.createElement("div"); cw.className = "canvas-wrap";
    const cv = document.createElement("canvas"); cv.id = c.id || ("chart" + i); cw.appendChild(cv); card.appendChild(cw);
    grid.appendChild(card);
    new Chart(cv.getContext("2d"), {
      type: c.type || "line",
      data: c.data || {},
      options: Object.assign({responsive: true, maintainAspectRatio: false, plugins: {legend: {labels: {boxWidth: 12}}}}, c.options || {})
    });
  } catch (e) { console.error("chart failed:", c && c.id, e); }
});
</script>
</body>
</html>
"""


def main(argv):
    if len(argv) < 2:
        sys.exit("usage: build_dashboard.py <input.json> [output.html]")
    src = Path(argv[1])
    out = Path(argv[2]) if len(argv) > 2 else src.with_suffix(".html")
    if not src.exists():
        sys.exit(f"input not found: {src}")
    try:
        payload = json.loads(src.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"invalid JSON in {src}: {e}")
    if not isinstance(payload, dict) or not payload.get("title"):
        sys.exit('payload must be a JSON object with at least a "title" field')

    # Escape text fields (they land in HTML), and guard the embedded JSON from
    # breaking out of the <script> tag.
    data_js = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    out_html = (
        TEMPLATE
        .replace("__TITLE__", html.escape(str(payload.get("title", "Running analysis"))))
        .replace("__SUBTITLE__", html.escape(str(payload.get("subtitle", "") or "")))
        .replace("__FOOTNOTE__", html.escape(str(payload.get("footnote", "") or "")))
        .replace("__DATA__", data_js)
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(out_html)
    n = len(payload.get("charts", []))
    print(f"wrote {out} ({n} chart{'s' if n != 1 else ''})")


if __name__ == "__main__":
    main(sys.argv)
