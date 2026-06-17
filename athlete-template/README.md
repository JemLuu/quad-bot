# Your athlete data (template)

This folder is the **scaffold** for your personal quad-bot data. When you run `/init`, these files are copied into a sibling **`athlete/`** folder and filled in. From then on, the skills read and update the copies in `athlete/`.

> ⚠️ **`athlete/` is gitignored and must stay that way.** It holds your personal data. Never commit it. This `athlete-template/` folder is committed and must contain **no real personal data** — only structure and placeholders.

## The documents

| File | Holds | Owned by (authoritative writer) |
|---|---|---|
| `profile.md` | Who you are, your goals, constraints, paces, preferences | `/init` (paces refined by `/training-plan`) |
| `plan.md` | Your training plan + which workouts are on your calendar | `/training-plan` |
| `activity-log.md` | Runs/workouts you've done (from Strava or logged manually) | `/update` (and `/log-run` for manual entries) |
| `health-log.md` | Aches, injuries, PT consultations, and your prehab routine | `/physical-therapist` |
| `check-ins.md` | History of check-ins and the plan changes you accepted/rejected | `/update` |
| `gear.md` | Your shoes/equipment, their mileage, and retirement alerts | `/gear-tracker` |
| `integrations.md` | Whether Strava/Calendar are connected + the init flag | `/init` |
| `nutrition.md` | Your fueling profile and personal fueling playbook | `/dietician` |

"Owned by" means that skill is the authoritative writer; other skills read the file. The full machine-readable contract is in `.claude/skills/_shared/schema.md`.

## How the skills coordinate

- `/init` creates this folder and writes `initialized: true` to `integrations.md` last — that flag is what "unlocks" every other skill.
- `/training-plan` owns the *structure* of `plan.md`. `/update` and `/race-week` only make small, you-approved edits to it and log why in `check-ins.md`.
- `/update` syncs your activities and proposes adjustments; `/physical-therapist` records injuries that the planning skills then respect.
- Distances/paces use the unit (mi or km) you set in `profile.md`.

## Resetting

Re-running `/init` is safe: it repairs missing files and lets you revise goals/integrations without overwriting what you've already filled in. To start completely fresh, delete your `athlete/` folder and run `/init` again.
