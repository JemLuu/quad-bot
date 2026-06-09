# Analysis ideas (a creative palette)

Pick a handful that fit the user's question — don't cram everything in. Each chart is a Chart.js spec (`{type, data, options}`) handed to the dashboard script, so you have full freedom on chart type and styling. Normalize to the athlete's units. Strava sources noted per item.

## Volume & training load
- **Weekly volume** — bar of distance/week + a line for the 4-week rolling average. (`list_activities`)
- **Cumulative distance** — line of YTD cumulative distance, optionally vs the same point last year. (`list_activities`)
- **Acute:Chronic Workload Ratio (ACWR)** — line of (7-day load ÷ 28-day load); shade the ~0.8–1.3 "sweet spot" and flag spikes >1.5 as injury risk. Load = distance, moving time, or TRIMP. (`list_activities`, HR for TRIMP)
- **Monotony & strain (Foster)** — monotony = mean daily load ÷ its SD across a week; strain = weekly load × monotony. High monotony flags grind/overtraining risk. (`list_activities`)

## Intensity distribution
- **80/20 easy–hard** — doughnut of time easy vs moderate vs hard (by HR zone or pace). Are they actually polarized? (`get_athlete_zones`, `get_activity_streams`)
- **HR-zone time** — stacked bar of minutes per zone per week. (`get_athlete_zones`, streams)
- **Pace histogram** — distribution of average paces; reveals the "comfort rut." (`list_activities`)

## Pacing & fitness
- **Pace vs distance** — scatter (x = distance, y = avg pace): the shape of their pacing. (`list_activities`)
- **Aerobic decoupling** — within long runs, pace:HR drift in the 2nd half vs the 1st; rising = aerobic fatigue, falling over weeks = fitness gains. (`get_activity_streams`)
- **Efficiency trend** — average pace at a fixed easy-HR band over time (faster at the same HR = fitter). (`list_activities` + streams)
- **Race predictions** — from recent bests, project 5K/10K/half/marathon via Riegel: `t2 = t1 · (d2/d1)^1.06`. Show as a small bar/table. (`list_activities`, `get_activity_performance`)

## Consistency & behavior
- **Day-of-week pattern** — bar of runs (or distance) by weekday. (`list_activities`)
- **Runs per week over time** + current / longest-streak KPI. (`list_activities`)
- **Time-of-day** — when they tend to run. (`list_activities` start times)

## Terrain & gear
- **Elevation trend** — climbing per week. (`list_activities`)
- **Shoe mileage** — bar per shoe with a retirement line (~300–500 mi / 500–800 km). (`get_gear`)

## Presentation tips
- Lead with 3–5 **KPI cards** (total distance, total runs, avg weekly, biggest week, a fitness signal).
- Add 1–2 sentence **insight callouts** in plain language — the "so what."
- Use `span: 2` for the hero chart (usually weekly volume).
- Strava's brand orange `#fc5200` makes a nice accent for the primary dataset.
