# Data conventions (shared by all skills)

How to read and edit the documents in `athlete/` safely. Skills reference this instead of repeating it.

## Initialization gate (run this first in every skill except `/init`)

1. Check whether `athlete/integrations.md` exists **and** its front-matter has `initialized: true`.
2. **If not** (folder/file missing, or flag false/absent): STOP. Tell the user:
   > "It looks like quad-bot isn't set up yet. Run `/init` first so I have your goals and data folder."
   Do nothing else.
3. **If yes:** read `.claude/skills/_shared/schema.md` to refresh the ownership contract, then proceed. Only write documents your skill owns.

## Editing: modify in place, don't recreate

These are living documents. For any change:

1. **Locate the owning section** (per `schema.md` / the template layout) and edit *that section in place*. Do not append a duplicate section, and never recreate the whole file.
2. **Refresh `last_updated`** in the front-matter to today's date (`YYYY-MM-DD`). Update any other relevant front-matter key (`plan_version`, `active_issues_count`, `check_in_count`, sync timestamps).
3. **Only logs are appended**, and only with dedupe:
   - `activity-log.md` recent activities — before adding a run, look for an existing row for the same session and update it in place instead of appending a duplicate. Match by `strava_id` when both rows have one; otherwise by `date + type + ~distance`. This catches a run that was logged manually (blank `strava_id`) and later synced from Strava — upgrade that row with the `strava_id` rather than adding a second copy.
   - `check-ins.md` history, `plan.md` change log, `integrations.md` sync log — one concise line per event.
4. **Preserve the user's words.** Don't silently rewrite content a user authored (goals, notes); add or update, and confirm before replacing.

## Keep documents from growing unbounded

- **activity-log.md:** keep a detailed rolling window (~8–12 weeks) in "Recent activities." When entries age out, collapse each old week into a single line under "Archive summary" (week + total distance/time), then remove its detailed rows.
- **check-ins.md:** keep the latest check-in in full; condense older ones to one line in "Check-in history."
- **health-log.md:** move resolved issues to "Resolved (archive)" as one-liners.
- **plan.md change log:** one line per revision; the detail lives in `check-ins.md`.

## Units

The athlete's unit (`mi` or `km`) is set in `profile.md` front-matter (`units:`). Normalize every distance and pace — including values pulled from Strava — to that unit before writing or displaying.

## Dates

Write dates as `YYYY-MM-DD`. Don't invent a date — use today's actual date when stamping `last_updated`.
