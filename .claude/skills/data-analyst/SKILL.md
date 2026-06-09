---
name: data-analyst
description: Turns the runner's Strava data into an interactive visual dashboard and a sharp written analysis — pulls activities, streams, HR zones, and gear from the Strava MCP, computes training-load, pacing, intensity-distribution, consistency, and fitness-trend metrics, and renders a self-contained HTML chart dashboard. Use when the user wants to analyze their running, see charts/graphs/visualizations, explore trends, spot patterns, or get data-driven insights. Requires quad-bot to be initialized.
allowed-tools: Read, Write, Edit, Bash
---

# data-analyst — visualize & analyze your running

Pulls your Strava history and builds an interactive HTML dashboard plus a written read on what the data actually says. **Read-only on your quad-bot documents** — its only output is the dashboard under `athlete/analysis/` (gitignored). Strava is read-only too; never write activities.

**Start:** run the initialization gate in `.claude/skills/_shared/data-conventions.md`.

## Workflow

```
- [ ] 1. Scope the question
- [ ] 2. Pull Strava data
- [ ] 3. Compute the analyses
- [ ] 4. Build the dashboard
- [ ] 5. Open it + tell the story
```

### 1. Scope
Ask what they want analyzed, or default to **"last 12 weeks, all runs."** Read `profile.md` for **units**, goals, and paces so framing fits the athlete.

### 2. Pull Strava data
Confirm Strava is connected (resolve the server/tool names from `integrations.md`; default server `strava-mcp`). If it isn't, fall back to `activity-log.md` and say the analysis is limited. Useful tools:
- `strava-mcp:get_athlete_profile` — athlete + lifetime totals
- `strava-mcp:list_activities` — the activity feed (paginate to cover the window)
- `strava-mcp:get_athlete_zones` — HR/power zones
- `strava-mcp:get_gear` — shoes/bikes & mileage
- `strava-mcp:get_activity_streams` — per-activity time series (heartrate, velocity, altitude, cadence, latlng) for deep dives
- `strava-mcp:get_activity_performance` — per-activity performance metrics

**Be efficient:** use `list_activities` for the overview; only pull `get_activity_streams` for a handful of standout activities — never stream hundreds.

### 3. Compute the analyses
Pick a few that fit the question from `${CLAUDE_SKILL_DIR}/reference/analyses.md` (weekly load + ACWR, 80/20 easy–hard split, pace-vs-distance, HR-zone mix, aerobic decoupling / fitness trend, consistency, race predictions, shoe mileage, …). Normalize everything to the athlete's units.

### 4. Build the dashboard
Assemble a JSON payload (KPI cards, chart specs, insight callouts — schema is documented at the top of the script) and render it:
```bash
mkdir -p athlete/analysis
python3 ${CLAUDE_SKILL_DIR}/scripts/build_dashboard.py athlete/analysis/data.json athlete/analysis/dashboard.html
```
Each chart spec is passed **straight to Chart.js**, so you have full creative control over chart types (line / bar / scatter / doughnut / radar / …) while the script guarantees a clean, working render. **No Python packages required** (standard library only); Chart.js loads from a CDN at view time.

### 5. Open it + tell the story
Open the dashboard — `open athlete/analysis/dashboard.html` (macOS) — then give a concise written read: the 3–5 most interesting findings, what's improving or at risk, and one or two concrete next steps. For actions, point to the right skill (`/training-plan`, `/physical-therapist`, `/update`); don't edit those documents here.

## Notes
- Output lives in `athlete/analysis/` (gitignored — never commit it).
- This skill never modifies the core documents and never writes to Strava.
