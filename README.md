# quad-bot 🏃

Your running coach, built from [Claude Code](https://claude.com/claude-code) skills.

quad-bot is a suite of skills that work in tandem to coach your running. They share one set of **living documents** about you — your goals, plan, activities, injuries, and gear — so every skill's advice stays consistent and grounded in your real data. It can connect to **Strava** (to read your activities) and **Google Calendar** (to schedule your workouts), but works fully offline too.

## Quick start

1. **Clone this repo** and open it with Claude Code.
2. Run **`/init`** — it interviews you about your goals, sets up your private data folder, and guides you through connecting Strava and Google Calendar (optional).
3. Use the other skills as you train. Start with **`/training-plan`**.

> Integrations are optional. If you skip them, quad-bot runs in "manual mode" — you log runs with `/log-run` and it prints schedules instead of writing to your calendar. To connect Strava / Google Calendar later, see **[SETUP.md](SETUP.md)**.

## The skills

| Skill | What it does |
|---|---|
| `/init` | Onboards you (goals, constraints), creates your data folder, connects integrations. **Run this first.** |
| `/training-plan` | Builds or revises your training plan and (optionally) schedules workouts on your calendar. |
| `/physical-therapist` | Talks through aches and injuries like a PT — strong suggestions, never a diagnosis. *Not medical advice.* |
| `/update` | A check-in: syncs Strava, compares planned vs actual, and proposes plan tweaks you accept or reject. |
| `/log-run` | Quickly logs a single run/workout (handy when Strava isn't connected). |
| `/coach` | Answers running questions grounded in your own data. |
| `/gear-tracker` | Tracks shoe/equipment mileage and flags when gear is due for retirement. |
| `/race-week` | Taper guidance, race-day pacing, and a prep checklist before a goal race. |

Every skill except `/init` requires you to have run `/init` first.

## Your data & privacy

- Your real data lives in **`athlete/`**, which is **gitignored** — it never gets committed.
- **`athlete-template/`** is the committed scaffold `/init` copies from (like `.env.example`). It contains no personal data.
- Keep it that way: don't move personal data out of `athlete/`, and don't commit it.

## How it fits together

All skills read and write the same documents in `athlete/` (profile, plan, activity log, health log, check-ins, gear, integrations). Each document has a single owning skill that's authoritative for it; the others read it. The schema is documented in [`athlete-template/README.md`](athlete-template/README.md) (for humans) and `.claude/skills/_shared/schema.md` (for the skills).

## Disclaimer

quad-bot is not a coach, doctor, or physical therapist. The `/physical-therapist` skill provides educational information only and is not a substitute for a licensed professional. For pain that is severe, worsening, or accompanied by warning signs, see a medical professional.
