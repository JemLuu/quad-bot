---
name: update
description: Runs a training check-in — pulls recent activities from Strava (or asks the user to paste or log them), reads the calendar, compares planned vs actual, reports how on-track the runner is, and proposes specific plan adjustments the user can accept or reject one at a time. Use for a check-in, a progress review, to sync Strava, or to see whether training is on track. Requires quad-bot to be initialized.
allowed-tools: Read, Write, Edit
---

# update — check-in & reconcile

Syncs reality into the data folder, then proposes plan changes. Makes only small, user-approved edits to `plan.md` — its structure stays owned by `/training-plan`.

**Start:** run the initialization gate in `.claude/skills/_shared/data-conventions.md`. Then read `.claude/skills/_shared/schema.md`.

## Workflow

```
- [ ] 1. Read integrations + plan
- [ ] 2. Sync activities (Strava or manual)
- [ ] 3. Read the calendar
- [ ] 4. Reconcile planned vs actual
- [ ] 5. Propose changes (itemized)
- [ ] 6. Apply accepted changes
- [ ] 7. Record the check-in
```

### 1. Read integrations + plan
`integrations.md` (connection state, server/tool names, training calendar ID), `plan.md`, `profile.md`, `health-log.md`.

### 2. Sync activities
- **Strava connected:** fetch activities since `last_synced_activity_id` / `last_strava_sync`. **Dedupe before appending:** match each activity to an existing row by `strava_id`, or — for runs already logged manually (blank `strava_id`) — by `date + type + ~distance`, and update that row in place (attaching the `strava_id`) instead of adding a duplicate. Normalize to the athlete's units. Append genuinely new activities to activity-log.md's Recent activities, recompute Weekly totals, advance `last_synced_activity_id` + `last_strava_sync`, and compact old weeks per `data-conventions.md`.
- **Not connected:** ask the user to paste recent runs or run `/log-run`. Dedupe manual entries by `date + type + distance`.

### 3. Read the calendar
If connected, read events over the plan window (read-only) to see what was scheduled vs done. Skip cleanly if not connected.

### 4. Reconcile
Follow `${CLAUDE_SKILL_DIR}/reference/reconciliation.md`: compare planned vs actual volume and key sessions, assign an adherence verdict, spot patterns, and **cross-check `health-log.md`** — a week missed due to injury is different from skipping.

### 5. Propose changes (itemized)
Present a **numbered list** of specific, independent proposals, each with its reason — e.g. "1. Cut next week 10% (you missed two runs); 2. Move Thu workout to Fri (Thu was busy); 3. Push the long run a day (you were sick)." Don't change anything yet.

### 6. Apply accepted changes
- Ask the user to **accept all, reject all, or pick by number** (and allow edits to any proposal). Apply **only** accepted items.
- Edit `plan.md` in place and bump `plan_version`. For calendar-affecting items, follow `.claude/skills/_shared/calendar.md` (update/delete/create via stored event IDs, **training calendar only**, confirm before deletions).
- Roll up shoe mileage into `gear.md` from the newly synced activities.
- If the goal is no longer reachable on the current structure, **recommend running `/training-plan`** instead of rebuilding the plan here.

### 7. Record the check-in
Write to `check-ins.md`: the latest check-in in full (verdict + each proposal's accept/reject outcome), condense the previous one into history, `check_in_count` +1. Add a one-line pointer to plan.md's Change log and refresh integrations.md sync timestamps.
