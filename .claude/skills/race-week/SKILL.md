---
name: race-week
description: Provides taper guidance, a race-day pacing strategy, and a preparation checklist for an upcoming goal race in the runner's plan. Use in the final weeks before a race, or when the user asks about tapering, race-day pacing, fueling, or race prep. Requires quad-bot to be initialized.
allowed-tools: Read, Write, Edit
---

# race-week — taper, pacing & prep

Gets the runner to the start line sharp and ready. Makes only small, user-approved edits to the plan (structure stays owned by `/training-plan`).

**Start:** run the initialization gate in `.claude/skills/_shared/data-conventions.md`.

## Workflow
1. **Read context:** `profile.md` (goal race, date, goal time, units), `plan.md` (current phase, recent weeks), `activity-log.md` (current fitness/freshness), `health-log.md` (any active issues). Confirm the race and how many days out it is.
2. **Taper:** propose how to reduce volume into race day while keeping a little intensity so the legs stay sharp (taper length scales with race distance — longer for marathon, shorter for 5K/10K). Present as itemized, user-approved tweaks; apply accepted ones to `plan.md` (bump `plan_version`) and log the reason in `check-ins.md`.
3. **Race-day pacing:** suggest a pacing strategy from their goal time and recent fitness (even effort or slight negative split for most distances; realistic target and a fallback). For fueling/hydration, read the **Race fueling** section of `nutrition.md` and summarize it, and point the user to `/dietician` to build or refine that plan.
4. **Prep checklist:** give a concise checklist — logistics (start time, travel, bib/kit), gear (shoes, weather layers, nothing new on race day), nutrition the day before and morning of, sleep, warm-up.
5. **Write it down:** add a "Race Week & Day" section to `plan.md` with the taper, pacing target, and checklist. Optionally schedule the taper sessions on the calendar via `.claude/skills/_shared/calendar.md` (training calendar only). After the race, you may add a short recap to `check-ins.md`.
