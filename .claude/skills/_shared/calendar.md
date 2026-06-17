# Calendar integration & safety (shared by /training-plan and /update)

How to put workouts on the user's calendar without ever touching their personal events. Read this before any calendar operation.

## Resolve the connection first

Read `athlete/integrations.md`:
- If Calendar **Connected** is not `yes`, **do not attempt calendar calls.** Degrade gracefully: present the schedule as text and tell the user they can connect a calendar via `SETUP.md`. This is never fatal.
- Use the recorded **Server name** (default `google-calendar`) and **Tool names** to build fully-qualified MCP tool calls, e.g. `google-calendar:create-event`. Resolve the exact tool names from `integrations.md` — don't hard-code them (different servers name tools differently, e.g. hyphens vs underscores).
- Read the **Training calendar ID** — the dedicated calendar all events go to. If it's `not-set`, ask the user to create/confirm it (see `SETUP.md`) and record it before writing anything.

## The safety rules (non-negotiable)

1. **Writes and deletes target ONLY the training calendar ID.** Never create, update, or delete events on the user's primary calendar or any other calendar. (The create/update tools take a calendar id — always pass the training calendar's.)
2. **Reads may span calendars** — to find free time, you may read the user's other calendars' busy blocks (`list-events` / `get-freebusy`). Reading is fine; writing is not.
3. **Delete only events quad-bot created.** The only deletable events are those listed in `plan.md`'s **Calendar sync state** table (by Event ID). Never bulk-delete or "clear the calendar."
4. **Confirm before any deletion or batch change.** Show the user exactly which events will be created/moved/removed and get a yes first.
5. **Persist every event ID.** After creating an event, write the returned event ID into `plan.md`'s Calendar sync state (Date | Session | Event ID). After deleting one, remove that row. This mapping is what makes updates idempotent and prevents duplicates.

## Typical flow (scheduling workouts)

1. Confirm the calendar is connected and the training calendar ID is set.
2. Read the relevant date range across the user's calendars to find open slots (respect the constraints in `profile.md`, and prefer the athlete's usual run days/times when the scheduling skill provides them).
3. **Propose** specific placements (session → date/time) and get explicit approval.
4. For each approved session: create the event **in the training calendar**; record the returned event ID in `plan.md`.
5. To change a session later: update the event (or delete + recreate) using the stored ID, then refresh the mapping.

## Notes

- Creating events requires a **write OAuth scope** (`calendar.events`). If writes fail with a permission error, tell the user to re-do the scope step in `SETUP.md`; fall back to printing the schedule.
- OAuth scopes are calendar-wide, so rule 1 is enforced by *always passing the training calendar ID* — be disciplined about it.
