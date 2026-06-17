# quad-bot — conventions for Claude

quad-bot is a running-coach toolkit built from Claude Code skills. Every skill reads and writes a shared set of **living documents** about one athlete. This file is the operating manual for any skill working in this repo.

## Where the data lives

- **`athlete/`** — the athlete's live data. **gitignored. NEVER commit it**, and never paste its contents into commit messages, PRs, issues, or any external service.
- **`athlete-template/`** — the committed scaffold. `/init` copies it into `athlete/`. Edit the template only to evolve the schema for *future* users; never put real personal data in it.

## The skills

`/init`, `/training-plan`, `/physical-therapist`, `/update`, `/log-run`, `/coach`, `/gear-tracker`, `/race-week`, `/data-analyst`, `/dietician`. Each lives in `.claude/skills/<name>/SKILL.md`. Shared knowledge is in `.claude/skills/_shared/`.

## Golden rules (every skill)

1. **Initialization gate.** Every skill *except* `/init` must first confirm `athlete/integrations.md` exists and its front-matter has `initialized: true`. If not, STOP and tell the user to run `/init`. The exact preamble is in `.claude/skills/_shared/data-conventions.md`.
2. **One source of truth.** Before editing any document, consult the ownership contract in `.claude/skills/_shared/schema.md`. Write only the documents your skill owns; read the rest.
3. **Modify in place — don't recreate.** These are living documents. Find the owning section, update it, and refresh `last_updated`. Only logs are *appended* (with dedupe). Never create duplicate files or sections. Details in `data-conventions.md`.
4. **Calendar safety.** All calendar **writes and deletes go ONLY to the dedicated "quad-bot Training" calendar** whose ID is in `integrations.md`. Never write to or delete from the user's other calendars. Only delete events quad-bot created (tracked in `plan.md`'s calendar sync state). Always confirm before any deletion or batch change. Details in `.claude/skills/_shared/calendar.md`.
5. **Strava is read-only.** Never attempt to create, edit, or delete Strava activities.
6. **PT is not medical advice.** `/physical-therapist` must lead with its disclaimer and never assert a definitive diagnosis — strong, hedged suggestions only. Details in its SKILL.md.
7. **Confirm before outward or hard-to-reverse actions** — calendar writes/deletes, and overwriting any document a user has already filled in.

## Conventions

- **Units** (mi/km) come from `athlete/profile.md`; normalize all distances/paces to the athlete's unit.
- **MCP tools:** reference by fully-qualified name, e.g. `google-calendar:create-event`, `strava-mcp:<tool>`. Resolve the exact server names and tool names from `athlete/integrations.md` (recorded at init). If an MCP isn't connected, degrade gracefully to manual mode — don't fail.
- **Keep `SKILL.md` files lean** (< 500 lines). Put detail in per-skill `reference/` files and the `_shared/` docs; reference them only when needed.
- **Dates:** write real dates as `YYYY-MM-DD`. Templates use placeholders, not real dates.
