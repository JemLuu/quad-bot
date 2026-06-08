---
last_updated: not-set
owner_skill: update
schema_version: 1
source: none                   # strava | manual | mixed | none
last_strava_sync: not-set      # YYYY-MM-DD of last successful Strava read
last_synced_activity_id: none  # highest Strava activity id already imported (for dedupe)
---

# Activity log

<!-- Owned by /update (Strava sync). /log-run appends manual entries. Before adding a run, dedupe:
     match an existing row by strava_id (if present) or by date+type+~distance, and update it in place
     instead of duplicating — so a run logged manually and later synced from Strava isn't counted twice. -->

## Recent activities

<!-- Rolling detailed window (~8–12 weeks). effort = perceived effort 1–10.
     source = strava | manual. Older entries get collapsed into "Archive summary" below. -->

| Date | Type | Distance | Duration | Avg pace | Effort | Shoe | Notes | source | strava_id |
|------|------|----------|----------|----------|--------|------|-------|--------|-----------|
|      |      |          |          |          |        |      |       |        |           |

## Weekly totals

<!-- Recomputed from the activities above. Used by /update to compare planned vs actual. -->

| Week (Mon–Sun) | Runs | Distance | Time |
|----------------|------|----------|------|
|                |      |          |      |

## Archive summary

<!-- Weeks older than the detailed window, collapsed to one line each (week + total distance/time). -->

-
