# Connecting Strava & Google Calendar

quad-bot works fully offline. Connect these integrations only if you want automatic activity syncing (Strava) and calendar scheduling (Google Calendar). You can do this any time — then re-run `/init` (or `/update`) to record the connection.

Both are **remote MCP servers**. You connect each one by (1) adding it with a single `claude mcp add` command in your terminal, then (2) authenticating once in your browser with Claude Code's `/mcp` command. The servers go into your *local* Claude config, so **nothing sensitive is stored in this repo.**

> The Google Cloud console UI and exact MCP details change over time. If a step looks different, follow the official pages linked below and check status with `/mcp`.

---

## Strava (read-only activity data)

Requires an active Strava subscription. The connector is **read-only** — quad-bot can read your activities but never edit or upload them. Details: **[Strava MCP Connector](https://support.strava.com/hc/en-us/articles/46190267796237-Strava-MCP-Connector)**.

1. In your terminal, add the server:
   ```bash
   claude mcp add --transport http strava-mcp https://mcp.strava.com/mcp
   ```
2. In Claude Code, run `/mcp`, select **strava-mcp**, and complete the Strava login in your browser.
3. Run `/init` (or `/update`) so quad-bot records that Strava is connected and learns its tool names.

---

## Google Calendar (scheduling workouts)

This uses Google's official Calendar MCP server. Setup is the most involved part of quad-bot because Google makes you create your own OAuth client — but you only do it once, and the same is required for *any* Google Calendar access. Official guide: **[Configure the Calendar MCP server](https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server)**.

Do the parts in order: **A** (calendar) and **B** (Google Cloud) happen in your browser; **C** connects it to Claude Code.

### A. Create a dedicated calendar (important for safety)

quad-bot writes workouts to a **separate calendar** so it never touches your personal events and can never delete anything outside its own calendar.

1. In [Google Calendar](https://calendar.google.com), under **Other calendars** → **+** → **Create new calendar**.
2. Name it **`quad-bot Training`** and create it.
3. Open its **Settings**, scroll to **Integrate calendar**, and copy the **Calendar ID** (looks like `...@group.calendar.google.com`). You'll confirm this during `/init`.

### B. Set up Google Cloud OAuth

1. Go to the [Google Cloud Console](https://console.cloud.google.com) and create (or select) a project (top bar → project dropdown → **New Project**).
2. **Enable the APIs:** APIs & Services → **Library** → search for and enable **Google Calendar API** and **Google Calendar MCP API**.
3. **Set up the OAuth consent screen.** This is the permission screen Google shows when an app asks to use your calendar; you must define it before you can create credentials. Go to **APIs & Services → OAuth consent screen** and fill it in:
   - **User type → choose "External", then Create.** "Internal" only exists for Google Workspace organizations, so for a personal Gmail account "External" is the only choice. It does **not** make your calendar public — it just means the app isn't restricted to a single organization.
   - **App information:** set an **App name** (e.g. `quad-bot`), choose your own email for **User support email**, and enter your email again under **Developer contact information**. Logo and links can stay blank. Save and continue.
   - **Test users → add your own Google email address.** This is required: while the app stays in **"Testing"** mode (which is fine for personal use — you never need to publish it), only the emails listed here are allowed to sign in. If you skip this, you'll hit an **"access blocked / app not verified"** error when you try to authenticate in step C.
4. **Add the scopes** (permissions). Include a **write** scope so quad-bot can create events, plus the read scopes the guide lists:
   - `https://www.googleapis.com/auth/calendar.events` ← **write** (create / update / delete events)
   - `https://www.googleapis.com/auth/calendar.events.readonly`
   - `https://www.googleapis.com/auth/calendar.events.freebusy`
   - `https://www.googleapis.com/auth/calendar.calendarlist.readonly`

   Without the `calendar.events` write scope, quad-bot can only *read* your calendar.
5. **Create the OAuth client:** APIs & Services → **Credentials** → **Create credentials** → **OAuth client ID**. Follow the linked Google guide for the client type and any redirect URI it specifies for MCP clients, and keep the **client ID / secret** it shows you.

> Tip: if you have the `gcloud` CLI installed and authenticated, `/init` can run the API-enable step for you (`gcloud services enable ...`). The consent screen and OAuth client still need the clicks above.

### C. Connect it to Claude Code

1. In your terminal, add the server:
   ```bash
   claude mcp add --transport http google-calendar https://calendarmcp.googleapis.com/mcp/v1
   ```
2. In Claude Code, run `/mcp`, select **google-calendar**, and complete the browser sign-in. If it asks for the OAuth client ID / secret from step B5, provide them.
3. Run `/init` (or `/update`). quad-bot lists your calendars, confirms the **`quad-bot Training`** calendar with you, and stores its Calendar ID in `athlete/integrations.md`. From then on, all workout events go only to that calendar.

---

## Troubleshooting

- **`claude mcp add` says command not found:** run it in a terminal where the Claude Code CLI is installed.
- **"Tool not found" / server not connected:** run `/mcp` to check status and re-authenticate.
- **Calendar events fail to create:** you probably granted only read scopes — redo step B4 with the `calendar.events` write scope, then re-authenticate via `/mcp`.
- **Connecting fails on transport:** remove it (`claude mcp remove <name>`) and re-add with `--transport sse` instead of `--transport http`.
- **Want a harder safety boundary than the dedicated calendar:** Google's `calendar.app.created` scope restricts an app to only the calendars it created. It's more involved to set up; the dedicated-calendar approach above is the recommended default.
