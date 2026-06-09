---
last_updated: not-set
owner_skill: init
schema_version: 1
initialized: false      # /init sets this to true LAST — it is the "setup complete" flag every other skill checks
---

# Integrations & setup state

<!-- Owned by /init. /update may touch the sync timestamps below. -->

## Initialization

- **initialized:** false      <!-- mirrors the front-matter flag above -->
- **init date:**

## Strava (read-only)

- **Connected:** unknown          <!-- yes | no | unknown -->
- **Server name:** strava-mcp     <!-- MCP server name as it appears in /mcp -->
- **Tool names:** not-detected    <!-- e.g. strava-mcp:list_activities, strava-mcp:get_activity_streams — fill in what /mcp shows -->
- **Read-only:** yes (the connector cannot write activities)
- **Last successful read:**

## Calendar

- **Connected:** unknown          <!-- yes | no | unknown -->
- **Server name:** google-calendar    <!-- local server: @cocal/google-calendar-mcp -->
- **Training calendar name:** quad-bot Training
- **Training calendar ID:** not-set   <!-- the dedicated calendar; ALL workout events go only here -->
- **Write scope confirmed:** unknown  <!-- yes | no — needed to create events -->
- **Tool names:** create-event, update-event, delete-event, list-events, list-calendars, get-event, get-freebusy, search-events  <!-- confirm against /mcp -->
- **Last successful sync:**

## Sync log

<!-- Terse dated lines of the last Strava/calendar operations. -->

-
