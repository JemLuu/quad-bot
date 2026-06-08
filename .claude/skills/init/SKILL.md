---
name: init
description: Sets up quad-bot for a runner — interviews them about their running goals and constraints, optionally connects the Strava and Google Calendar MCPs (including a dedicated training calendar), and creates the private athlete/ data folder from the committed template. Use on first run, when the user wants to get started with or set up quad-bot, or to revise their goals or integrations. Running it unlocks the other coaching skills.
allowed-tools: Read, Write, Edit, Bash
---

# init — set up quad-bot

Onboards the athlete and creates their data folder. This is the only skill that runs *before* initialization, so it does **not** use the init-check gate. Running it again later is safe — switch to repair/update mode (step 1).

First, read `.claude/skills/_shared/schema.md` (what you'll write) and skim `SETUP.md` (integration steps you'll walk the user through).

## Workflow

Copy this checklist and check items off as you go:

```
- [ ] 1. Detect existing setup
- [ ] 2. Create athlete/ from the template
- [ ] 3. Goal interview → profile.md
- [ ] 4. Connect integrations (Strava, Calendar) — optional
- [ ] 5. Mark initialized (do this LAST)
- [ ] 6. Hand off
```

### 1. Detect existing setup
- If `athlete/integrations.md` exists with `initialized: true`, you're in **repair/update mode**: tell the user quad-bot is already set up, and ask what they want — revise goals, (re)connect an integration, or repair missing template files. **Never overwrite a filled-in document without confirming.**
- Otherwise, continue with first-time setup.

### 2. Create athlete/ from the template
Copy any template files that are missing from `athlete/` (never overwrite existing ones):

```bash
mkdir -p athlete
for f in athlete-template/*; do
  name="$(basename "$f")"
  [ -e "athlete/$name" ] || cp "$f" "athlete/$name"
done
```

### 3. Goal interview → profile.md
- Work through the question groups in `${CLAUDE_SKILL_DIR}/reference/goal-interview.md`, **one group at a time** — don't dump every question at once, and adapt follow-ups to their answers.
- Write answers into the matching sections of `athlete/profile.md`. Set `units:` (mi or km) from their preference. Refresh `last_updated`.

### 4. Connect integrations (optional — confirm each)
Both are optional; quad-bot works in manual mode without them.

- Ask whether they want **Strava** (read-only activity sync) and/or **Google Calendar** (workout scheduling).
- For each they want, check whether the MCP is already connected — try a lightweight read (e.g. list calendars / fetch the athlete); if the tool is absent or errors, it's **not** connected.
  - **Connected:** record `Connected: yes`, the server name, and the tool names you actually see into `athlete/integrations.md`. For Calendar, list the user's calendars and confirm/record the dedicated **quad-bot Training** calendar ID (creation steps are in `SETUP.md`); note whether a write scope is present.
  - **Not connected:** point them to `SETUP.md`, set `Connected: no`, and continue in manual mode.
- If `gcloud` is installed and they're setting up Calendar, you may offer to run the API-enable commands from `SETUP.md`. **Never store secrets in the repo.**

### 5. Mark initialized (LAST)
As the final step, set `initialized: true` in `athlete/integrations.md` (both the front-matter key and the mirrored line in the Initialization section) and fill the init date. Doing this last means an interrupted setup correctly leaves quad-bot locked.

### 6. Hand off
Summarize what's configured and what's in manual mode, then suggest next steps — usually `/training-plan`. Remind them the other skills (`/physical-therapist`, `/update`, `/log-run`, `/coach`, `/gear-tracker`, `/race-week`) are now available.
