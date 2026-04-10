# ForkFox Planning Docs

Session artifacts from the 2026-04-10 system design session with Claude.

## Files

- **`forkfox-system-sketch.excalidraw`** — 660-element visual sketch of the entire
  ForkFox.ai system: pipeline, data schema, social channels, site map, current/new
  page wireframes, 4 Atlas example pages, and social post mockups with actual copy.
  Open in Excalidraw to pan/zoom across all 11 zones.

- **`forkfox-system-plan.md`** — the detailed written plan that the sketch
  visualizes. Describes the architecture, analytics setup, local-first pSEO
  strategy, Supabase schema, Postiz-based social automation pipeline, cost
  projections (~$300-600 for 50K pages), and the 25-75/day ramp strategy.

## Scope of the plan

This is the consolidated output of a single session that evolved across multiple
constraints:

1. **No Next.js** — static HTML + Python generator + Jinja2 templates fits the
   existing `landing-pages/` repo shape and the 25-75 pages/day target volume.
2. **No app data** — the programmatic content uses only free public sources
   (OpenStreetMap, Wikipedia/Wikidata, Library of Congress, NYPL Menu Collection,
   Chronicling America, Reddit, Firecrawl). The marketing Supabase stays
   completely separate from the backend app DB.
3. **Hyper-local focus** — ~80% Philadelphia + Bay Area content (where the
   founders live, where paying customers and investors will come from). ~20%
   non-local breaker content for topical diversity.
4. **Multi-dimensional content** — historical, neighborhood, dish anatomy,
   superlative, cuisine×city, comparison, and term/glossary pages. Each page type
   slots into `/atlas/<type>/...`.
5. **9-platform auto-posting** via RSS feed → Postiz (self-hosted, ~$5-15/mo).
   LinkedIn, Facebook, Instagram feed, Threads, Bluesky, Mastodon, Pinterest, and
   Google Business Profile all get full auto volume. X gets curated 3-5/day due
   to free-tier limits. Reddit stays manual.

## Next step

Ship Phase 0 (analytics) first — waiting on GA4 Measurement ID from Ali before
the injection script can be built and the 7 existing HTML pages can be tagged.
