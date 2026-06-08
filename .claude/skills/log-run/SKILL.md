---
name: log-run
description: Quickly logs a single run or workout into the athlete's activity log. This is the manual entry path, useful because the Strava connector is read-only and not every user connects it. Use when the user wants to record a run, log a workout, or add an activity by hand. Requires quad-bot to be initialized.
allowed-tools: Read, Write, Edit
---

# log-run — record one activity

Appends a single run/workout to `athlete/activity-log.md`. Keep it fast and low-friction.

**Start:** run the initialization gate in `.claude/skills/_shared/data-conventions.md`.

## Steps
1. Collect the details (ask only for what's missing; default the date to today):
   **date, type** (easy/long/tempo/intervals/recovery/cross/race), **distance, duration**, perceived **effort** (1–10), optional **shoe**, optional **notes**. Use the athlete's units from `profile.md`.
2. **Dedupe:** if an entry with the same `date + type + distance` already exists, update it instead of adding a duplicate.
3. Append the row to **Recent activities** with `source: manual` (leave `strava_id` blank). Recompute that week's **Weekly totals**. If the log has grown past the detailed window, compact old weeks per `data-conventions.md`.
4. If a shoe was tagged, add the distance to that shoe's mileage in `gear.md` (or note it for `/gear-tracker`).
5. Refresh `last_updated`, set `source` to `manual` or `mixed`, and confirm what you logged.
