# Connecting Strava & Google Calendar

quad-bot works fully offline. Connect these integrations only if you want automatic activity syncing (Strava) and calendar scheduling (Google Calendar). You can do this any time — then re-run `/init` (or `/update`) to record the connection.

You connect each one by adding it with a `claude mcp add` command and authenticating in your browser once. **Strava** is a hosted (remote) connector; **Google Calendar** runs as a small server on your own machine (Claude Code can't use Google's *hosted* calendar server — see the note in that section). Either way, the config and your credentials live in your local Claude setup, **not in this repo.**

> The Google Cloud console UI and MCP details change over time. If a step looks different, follow the official pages linked below and check status with `/mcp`.

---

## Strava (read-only activity data)

Requires an active Strava subscription. The connector is **read-only** — quad-bot can read your activities but never edit or upload them.

1. Open Strava's **[MCP Connector page](https://support.strava.com/hc/en-us/articles/46190267796237-Strava-MCP-Connector)** and copy the `claude mcp add` command they give you, then run it in a normal terminal. As of now that command is:
   ```bash
   claude mcp add --transport http strava-mcp https://mcp.strava.com/mcp
   ```
2. Start (or restart) Claude Code with `claude`, run `/mcp`, select **strava-mcp**, and log in to your Strava account in the browser when prompted.
3. Run `/init` (or `/update`) so quad-bot records that Strava is connected and learns its tool names.

> If **strava-mcp** doesn't show up in `/mcp`, run the `claude mcp add` command from inside the quad-bot folder (it's added for the current project by default), or append `--scope user` to make it available in every project.

---

## Google Calendar (scheduling workouts) — runs locally

**Why local:** Claude Code can't connect to Google's *hosted* Calendar MCP. That server needs a pre-registered OAuth client, but Claude Code's remote-MCP login only does *dynamic client registration*, so it fails with **"does not support dynamic client registration."** Instead we run a small, popular open-source server on your machine — [`@cocal/google-calendar-mcp`](https://github.com/nspady/google-calendar-mcp) — which does the Google sign-in itself and works with Claude Code. You still create a Google OAuth client once; the rest is two commands.

Do the parts in order: **A** (calendar) and **B** (Google Cloud) happen in your browser; **C** runs the local server in Claude Code.

### A. Create a dedicated calendar (important for safety)

quad-bot writes workouts to a **separate calendar** so it never touches your personal events and can never delete anything outside its own calendar.

1. In [Google Calendar](https://calendar.google.com), under **Other calendars** → **+** → **Create new calendar**.
2. Name it **`quad-bot Training`** and create it.
3. Open its **Settings**, scroll to **Integrate calendar**, and copy the **Calendar ID** (looks like `...@group.calendar.google.com`). You'll confirm this during `/init`.

### B. Create a Google OAuth client

1. Go to the [Google Cloud Console](https://console.cloud.google.com) and create (or select) a project (top bar → project dropdown → **New Project**).
2. **Enable the API:** APIs & Services → **Library** → enable **Google Calendar API**. (You do **not** need the "Google Calendar MCP API" — that's only for Google's hosted server, which we're not using.)
3. **Configure the OAuth consent screen** — Google now calls this the **Google Auth Platform** (the left menu: Overview · Branding · Audience · Clients · Data Access · …):
   - **First time in this project?** On **Overview**, click **Get started** and complete the short wizard — **App name** + your **support email** → **Audience: External** → your **contact email** → create. ("External" is the only option for a personal Gmail; it does **not** make your calendar public.)
   - **Audience** tab → confirm the audience is **External**, leave **Publishing status = Testing**, and under **Test users** click **Add users** and add **your own Google email**. *Required:* otherwise sign-in is blocked with "access blocked / app not verified". ⚠️ In Testing mode Google expires the login after **~7 days** — you just re-authenticate (step C) when that happens, or click **Publish app** to stop the expiry.
   - **Branding** tab → where the App name / support email / contact live if you need to edit them.
4. **Add the scopes:** open the **Data Access** tab → **Add or remove scopes** → under **"Manually add scopes"** add a **write** scope plus the read scopes, then click **Update**:
   - `https://www.googleapis.com/auth/calendar.events` ← **write** (create / update / delete events)
   - `https://www.googleapis.com/auth/calendar.events.readonly`
   - `https://www.googleapis.com/auth/calendar.events.freebusy`
   - `https://www.googleapis.com/auth/calendar.calendarlist.readonly`

   (If sign-in later complains about scopes, the server may request the broader `https://www.googleapis.com/auth/calendar` scope — add that one too.)
5. **Create the client:** open the **Clients** tab → **Create client** → **Application type: Desktop app** *(important — the local server requires a Desktop client)* → **Create**. A dialog then pops up with your client ID/secret and a **Download JSON** button — **download it right there and then.** That's the easiest moment to grab it; if you close the dialog without downloading, you can re-download anytime via the **⬇ icon** on the client's row in the Clients list. Move the file to a stable path outside the repo:
   ```bash
   mkdir -p ~/.config/quad-bot
   mv ~/Downloads/client_secret_*.json ~/.config/quad-bot/gcp-oauth.keys.json
   ```
   (A Desktop client's file starts with `{ "installed": … }`.)

### C. Run the local server in Claude Code

1. Add the server, pointing it at the JSON you downloaded (use the **absolute** path). Requires Node.js + `npx`:
   ```bash
   claude mcp add google-calendar \
     --env GOOGLE_OAUTH_CREDENTIALS=$HOME/.config/quad-bot/gcp-oauth.keys.json \
     -- npx -y @cocal/google-calendar-mcp
   ```
2. Start (or restart) Claude Code, run `/mcp`, and authenticate **google-calendar** — it opens a browser for Google sign-in/consent (you can also just ask Claude to "authenticate with Google Calendar"). Tokens are stored in `~/.config/google-calendar-mcp/tokens.json`, never in this repo.
3. Run `/init` (or `/update`). quad-bot lists your calendars, confirms the **`quad-bot Training`** calendar with you, and stores its Calendar ID in `athlete/integrations.md`. From then on, workout events go only to that calendar.

> Re-authenticate any time with `npx @cocal/google-calendar-mcp auth` — you'll need this roughly weekly while the consent screen stays in Testing mode.

---

## Troubleshooting

- **`claude mcp add` or `npx` not found:** run them in a terminal where the Claude Code CLI and Node.js are installed.
- **Server missing from `/mcp`:** `claude mcp add` defaults to the current project — run it from inside the quad-bot folder, or append `--scope user`. Then restart Claude Code.
- **Calendar sign-in blocked ("app not verified" / access denied):** add your Google account under **Audience → Test users** (step B3).
- **Calendar stops working after about a week:** Testing-mode tokens expire after ~7 days — re-run `npx @cocal/google-calendar-mcp auth`, or **Publish app** on the Audience tab.
- **Calendar events fail to create:** you probably granted only read scopes — redo step B4 with the `calendar.events` write scope, then re-authenticate.
- **Want a harder safety boundary than the dedicated calendar:** Google's `calendar.app.created` scope restricts an app to only the calendars it created. It's more involved to set up; the dedicated-calendar approach above is the recommended default.
