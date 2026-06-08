---
name: gear-tracker
description: Tracks the runner's shoe and equipment mileage and warns when gear is due for retirement. Use to add a new shoe, retire one, set a mileage threshold, log gear, or check how much life is left in the current rotation. Requires quad-bot to be initialized.
allowed-tools: Read, Write, Edit
---

# gear-tracker — shoes & equipment mileage

Owns the shoe/equipment lifecycle in `athlete/gear.md`. Mileage **accumulates** from activities tagged with a shoe.

**Start:** run the initialization gate in `.claude/skills/_shared/data-conventions.md`.

## Actions (do what the user asks)
- **Add a shoe:** name, date added, starting mileage (usually 0), and a retirement threshold (default ~300–500 mi / ~500–800 km — set per the shoe and the user's preference). Status `active`.
- **Retire a shoe:** set status `retired`; keep it for history.
- **Set / change a threshold.**
- **Check status:** show each active shoe's current mileage and how much is left before its threshold; **flag any shoe at or near retirement** (e.g. within ~10%).

## Mileage
- Maintain each shoe's **Current mileage** incrementally: when activities are logged (`/log-run`) or synced (`/update`) with that shoe tagged, add their distance. `Start mileage` is the baseline.
- You may reconcile/correct against the `Shoe` column in `activity-log.md`, but don't rely on recomputing from it alone — old detailed rows get compacted away, so the maintained running total is the source of truth.
- Use the athlete's units from `profile.md`. Update `last_updated` after changes.
