# Connecting Strava & Google Calendar

quad-bot works fully offline. Connect these integrations only if you want automatic activity syncing (Strava) and calendar scheduling (Google Calendar). You can do this any time — then re-run `/init` (or `/update`) to record the connection.

Both integrations are **remote MCP servers** already declared in [`.mcp.json`](.mcp.json). Connecting them means (1) providing a couple of values and (2) authenticating once in your browser via Claude Code's `/mcp` command. **No secrets are stored in this repo.**

> Some specifics below (OAuth client type, transport, exact tool names) can change. When in doubt, follow the official pages linked in each section and verify with `/mcp`.

---

## Strava (read-only activity data)

Requires an active Strava subscription. The connector is **read-only** — quad-bot can read your activities but never edit or upload them.

1. Get your Strava MCP connector URL from Strava: **[Strava MCP Connector](https://support.strava.com/hc/en-us/articles/46190267796237-Strava-MCP-Connector)**.
2. Make that URL available to `.mcp.json` as the `STRAVA_MCP_URL` environment variable — export it in your shell profile so it never touches a tracked file:
   ```bash
   export STRAVA_MCP_URL="https://...paste-the-strava-url..."
   ```
   The committed `.mcp.json` only references `${STRAVA_MCP_URL}`, so your personal URL stays out of git. Don't paste the URL directly into `.mcp.json` — it's tracked and could be committed by accident. If you'd rather configure it outside the repo, add Strava at local scope with `claude mcp add` instead.
3. In Claude Code, run `/mcp`, select **Strava**, and complete the OAuth login in your browser. Approve the project MCP server if prompted.
4. Run `/init` (or `/update`) so quad-bot records that Strava is connected and learns its tool names.

---

## Google Calendar (scheduling workouts)

This uses Google's official Calendar MCP server (`https://calendarmcp.googleapis.com/mcp/v1`). Setup is the most involved part of quad-bot because Google requires your own OAuth client. The same setup is required for *any* Google Calendar access, so it's unavoidable — but you only do it once. Official guide: **[Configure the Calendar MCP server](https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server)**.

### A. Create a dedicated calendar (important for safety)

quad-bot writes workouts to a **separate calendar** so it never touches your personal events, and so it can never delete anything outside its own calendar.

1. In [Google Calendar](https://calendar.google.com), under **Other calendars** → **+** → **Create new calendar**.
2. Name it **`quad-bot Training`** and create it.
3. Open its **Settings**, scroll to **Integrate calendar**, and copy the **Calendar ID** (looks like `...@group.calendar.google.com`). You'll confirm this during `/init`.

### B. Set up Google Cloud OAuth

1. Go to the [Google Cloud Console](https://console.cloud.google.com) and create (or select) a project.
2. **Enable APIs** (APIs & Services → Library): enable **Google Calendar API** and **Google Calendar MCP API**.
3. **OAuth consent screen**: configure it (User type *External* is fine for personal use), and add yourself as a **Test user**.
4. **Scopes**: add a **write** scope so quad-bot can create events — `https://www.googleapis.com/auth/calendar.events` — alongside the read scopes (`calendar.calendarlist.readonly`, `calendar.events.freebusy`, `calendar.events.readonly`). Without a write scope, quad-bot can only *read* your calendar.
5. **Create credentials** → **OAuth client ID**. Follow the linked Google guide for the client type and redirect URI it specifies for MCP clients.
6. If your setup requires the client ID/secret to be passed to the MCP server, add them to `.mcp.json` under the `google-calendar` server as `headers` using environment-variable placeholders (e.g. `"${GOOGLE_OAUTH_CLIENT_ID}"`) and export those vars — **never hard-code secrets into the committed file.**

> Tip: if you have the `gcloud` CLI installed and authenticated, `/init` can run the API-enable steps for you (`gcloud services enable ...`). The consent screen and OAuth client still need a few clicks in the console.

### C. Authenticate & record

1. In Claude Code, run `/mcp`, select **google-calendar**, and complete the browser OAuth. Approve the project MCP server if prompted.
2. Run `/init` (or `/update`). quad-bot will list your calendars, confirm the **`quad-bot Training`** calendar with you, and store its Calendar ID in `athlete/integrations.md`. From then on, all workout events go only to that calendar.

---

## Troubleshooting

- **"Tool not found" / server not connected:** run `/mcp` to check status and re-authenticate. Make sure project MCP servers are approved.
- **Calendar events fail to create:** you likely granted only read scopes — redo step B4 with the `calendar.events` write scope and re-authenticate.
- **Changed the connector URL or transport:** if a server uses SSE instead of streamable HTTP, change its `"type"` in `.mcp.json` from `"http"` to `"sse"`.
- **Want a harder safety boundary than the dedicated calendar:** the Google `calendar.app.created` scope restricts an app to only the calendars it created. It's more involved to set up; the dedicated-calendar approach above is the recommended default.
