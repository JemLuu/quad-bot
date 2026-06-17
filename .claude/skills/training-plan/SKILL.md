---
name: training-plan
description: Builds or revises a runner's training plan toward their goal, grounded in their profile, health log, and logged activity. Reads the Strava MCP (if connected) to learn the days and times they usually run and schedules around those habits. Can optionally read a connected Google Calendar to find free time (always confirming first) and create or update workout events in the dedicated "quad-bot Training" calendar. Use when the user wants a training plan, a new training block, to change their schedule, or to put workouts on their calendar. Requires quad-bot to be initialized.
allowed-tools: Read, Write, Edit
---

# training-plan — build & schedule the plan

Owns the structure of `athlete/plan.md`. (Other skills make only small, user-approved edits to it.)

**Start:** run the initialization gate in `.claude/skills/_shared/data-conventions.md`. Then read `.claude/skills/_shared/schema.md`.

## Workflow

```
- [ ] 1. Read the athlete's current state
- [ ] 2. Design (or revise) the plan
- [ ] 3. Confirm with the user
- [ ] 4. Write plan.md
- [ ] 5. Optional: schedule on the calendar
```

### 1. Read current state
- `profile.md` — goal, goal date, days/time available, paces, preferences, **units**.
- `health-log.md` — **Active issues → Training impact** (these limits are binding on load).
- `activity-log.md` — weekly totals / recent volume (the realistic starting point — don't plan from zero if they're already running, or from a high base if they're not).
- **Strava habits (if connected)** — pull recent activities (`strava-mcp:list_activities`; resolve exact names from `integrations.md`) and read their start times to learn the athlete's **usual run days and times of day** (e.g. weekday mornings, long run Saturday AM). No Strava? Infer the same from `activity-log.md` timestamps, or fall back to the availability stated in `profile.md`.
- `plan.md` — the existing plan, if any.

### 2. Design or revise
- Use the heuristics in `${CLAUDE_SKILL_DIR}/reference/plan-methodology.md`: choose the approach for the goal and timeline, set the weekly template, progress volume within safe caps, balance hard/easy, and scale the long run — all within the athlete's available days (leaning toward the days and times they already run) and any injury limits.
- New plan → build the full block to the goal date. Revision → change only what's needed; keep the rest intact.

### 3. Confirm
- Present the weekly template plus a week-by-week outline (next few weeks in detail, later weeks summarized). Get confirmation or adjustments **before** writing anything.

### 4. Write plan.md
- Update `plan.md` in place: Overview, Weekly template, Week-by-week table (set each week's status), and front-matter (`plan_version` +1, `goal_ref`, `start_date`, `goal_date`, `current_phase`, `last_updated`).
- If you computed training paces, write them back to `profile.md` → Fitness markers.
- Add a one-line entry to plan.md's Change log.

### 5. Optional: schedule on the calendar
- Only if the user wants it. Follow `.claude/skills/_shared/calendar.md` **exactly**: read free/busy across the user's calendars, propose specific placements — **defaulting each session to the athlete's usual time for that day** (from the habits read in step 1), shifting only to dodge conflicts — get approval, write events **only to the training calendar**, and record every returned event ID in plan.md's Calendar sync state.
- If no calendar is connected, present the schedule as text and point the user to `SETUP.md`. Never block on the calendar — it's additive.
