# quad-bot data schema (the contract)

The normative contract for the shared documents in `athlete/`. Every skill reads this before writing. Humans get the friendlier version in `athlete-template/README.md`.

## Contents
- Principles
- Ownership matrix
- Per-document specs
- Coordination rules

## Principles

- **One owner per document.** Only the owning skill writes a document's structure; every other skill reads it. (Two exceptions are spelled out below: `plan.md` and `activity-log.md`.)
- **Modify in place.** These are living documents — update the relevant section, never recreate the file or duplicate sections. See `data-conventions.md`.
- **Front-matter on every doc:** `last_updated` (YYYY-MM-DD), `owner_skill`, `schema_version`. Some docs add keys (below). Refresh `last_updated` on every write.

## Ownership matrix

`write` = authoritative writer. `read` = reads only.

| Document | init | training-plan | physical-therapist | update | log-run | gear-tracker | race-week | coach |
|---|---|---|---|---|---|---|---|---|
| `profile.md` | **write** | write (paces) | read | read | – | – | read | read |
| `plan.md` | scaffold | **write (structure)** | read | write (accepted edits) | – | – | write (taper/race) | read |
| `activity-log.md` | scaffold | read | read | **write (sync)** | write (manual) | read | read | read |
| `health-log.md` | scaffold | read | **write** | read | – | – | read | read |
| `check-ins.md` | scaffold | read | read | **write** | – | – | write (recap) | read |
| `gear.md` | scaffold | read | read | write (mileage) | tag shoe | **write (lifecycle)** | – | read |
| `integrations.md` | **write** | read | read | write (timestamps) | – | – | read | read |
| `nutrition.md` | scaffold | read | read | read | – | – | read (race fueling) | read |

`coach` is read-only across all documents. `data-analyst` is read-only on the core documents too — it only writes generated dashboards to `athlete/analysis/` (gitignored), and reads from the Strava MCP. `dietician` owns `nutrition.md` (the fueling profile + playbook) and reads profile/plan/activity/health; it writes no other document.

## Per-document specs

The exact section layout lives in each `athlete-template/<file>`. Key contracts:

- **profile.md** — `units: mi|km` in front-matter governs every distance/pace. Sections: Snapshot, Goals, Constraints, Fitness markers (training-plan may write computed paces), Preferences.
- **plan.md** — front-matter adds `plan_version`, `goal_ref`, `start_date`, `goal_date`, `current_phase`. Sections: Overview, Weekly template, **Week-by-week** (status: upcoming|current|done|modified), **Calendar sync state** (the `Date | Session | Event ID` table — the source of truth for which calendar events quad-bot created), Change log (one line per revision).
- **activity-log.md** — front-matter adds `source`, `last_strava_sync`, `last_synced_activity_id`. Sections: Recent activities (rolling ~8–12 wks), Weekly totals (derived), Archive summary.
- **health-log.md** — front-matter adds `active_issues_count`. Each active issue carries a **`Training impact`** line — this is what planning skills read to constrain load. Sections: Active issues, Consultation history, Prehab & strengthening routine, Resolved archive.
- **check-ins.md** — front-matter adds `check_in_count`. Sections: Latest check-in (full), Check-in history (one-liners).
- **gear.md** — Sections: Shoes (lifecycle table), Other gear. Mileage accumulates from tagged activities (maintained incrementally).
- **integrations.md** — front-matter `initialized: true|false` is the unlock flag. Records Strava/Calendar connection state, the **training calendar ID**, and detected MCP tool names.
- **nutrition.md** — front-matter `owner_skill: dietician`. Sections: Fueling profile (preferences, restrictions, optional weight), Gut-tested fuels, Daily framework, Fueling playbook (pre/during/post), Race fueling (read by `race-week`), Check-in notes. A captured profile + playbook, not a food log.

## Coordination rules

1. **`plan.md` has one structural owner: `training-plan`.** It creates and redesigns the plan (periodization, week shapes, mileage). `update` and `race-week` make only **incremental, user-approved** edits (shift/scale/drop sessions, taper tweaks), bump `plan_version`, and record the rationale in `check-ins.md`. If a structural overhaul is warranted (goal slipped badly, major injury), they **recommend running `/training-plan`** instead of rebuilding it themselves.
2. **`activity-log.md` is written by both `update` (Strava sync) and `log-run` (manual), under one shared dedupe rule:** before adding a run, find any existing row for the same session and update it in place rather than duplicating — match by `strava_id` when both have one, otherwise by `date + type + ~distance` (so a run logged manually and later synced from Strava is merged, not double-counted). `update` advances `last_synced_activity_id`.
3. **`gear.md` mileage accumulates incrementally** from activities tagged with a shoe (in `activity-log.md`): when runs are logged or synced, their distance is added to that shoe's current mileage. The shoe list/lifecycle is authoritative (owned by `gear-tracker`). Don't rely on recomputing from the log alone — old detailed rows get compacted away, so the maintained running total is the source of truth.
4. **The `Training impact` line in `health-log.md`** is binding on `training-plan` and `update`: respect active-issue limits when setting or adjusting load.
5. **All calendar event IDs live in `plan.md`'s Calendar sync state.** Never delete a calendar event that isn't listed there. See `calendar.md`.
