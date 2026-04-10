# ForkFox.ai — Visual Alignment + Analytics + Local-First pSEO + Social Automation

## Context

forkfox.ai is currently a vanilla static HTML site hosted on Vercel (repo: `C:\Users\alima\tastyr-iq\landing-pages\`). The site has **zero analytics**, **zero search-engine verification**, and **zero programmatic content** — all 7 live pages are handwritten HTML. Meanwhile the homepage already advertises "3,600+ dishes scored," and `/the-dish` is a human-edited blog index with ~9 curated articles.

**The project has evolved across this session.** The current plan reflects the final consolidated strategy:

1. **Ship analytics first, then everything else.** We are flying blind. Every day without GA4 + Vercel Analytics + Search Console is lost baseline data that cannot be recovered.
2. **The proprietary app dish dataset is OFF-LIMITS for marketing pages.** Ali confirmed the marketing site and the app backend database stay completely separate — and none of the app's dish scores, restaurant data, or user ratings can be reused for public SEO pages. This invalidates the original "dish/cuisine/restaurant from backend" schema idea.
3. **Strategy pivot: hyper-local + historical + multi-dimensional.** Since we can't use app data, the pSEO content will come from free public sources (OpenStreetMap, Wikipedia/Wikidata, Library of Congress, NYPL Menu Collection, Chronicling America newspaper archives, Reddit API) combined with Firecrawl for public blog/Reddit scraping. Content focuses HARD on Philly + Bay Area (where the founders live and where paying customers + fundraising will come from), across multiple dimensions: historical restaurants by decade, neighborhood food guides, longest-running spots, oldest bars, dish anatomy, cuisine migration stories, and more. ~80% local, ~20% non-local breaker content.
4. **Scale target: 25-75 new pages per day, ramping to 50K total over ~6 months.** Cost target: under $300-600 all-in (LLM writing via Claude Haiku 4.5 + Firecrawl + optional Flux image gen). Images: Library of Congress + Wikimedia CC0 + programmatic Excalidraw diagrams as the unique visual voice (zero image cost).
5. **Daily pages get auto-posted to 9 social platforms** via RSS feed + Postiz (open-source, self-hosted, ~$0-15/mo). LinkedIn, Facebook, Instagram feed, Threads, Bluesky, Mastodon, Pinterest all get full auto volume; X gets a curated 3-5/day subset due to free tier limits; Reddit stays manual. Instagram auto-posting works via Meta Graph API (Business account required, one-time setup).
6. **New sections to add to forkfox.ai**: `/atlas/` (the programmatic content section) and `/about/` (founder + mission page). `/the-dish` blog structure will be upgraded alongside. The existing cinematic homepage stays.

**Intended outcome of THIS plan update:** deliver a large Excalidraw canvas that visualizes the entire system — workflow, data schema, social channels, site map, current + new page UIs, 4 example Atlas pages, and how social posts will look across platforms — so Ali can approve the visual direction before any code is written.

**Explicitly narrower than the original brief:** no Next.js (static HTML + Python generator). Parts 2-3 of this plan below (the original app-data schema + generator design) are **STALE** and need rework to reflect the no-app-data + local-historical strategy — flagged for future update, not in scope for this session's execution.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Supabase (marketing-only project, separate from app)   │
│  cities · cuisines · restaurants · dishes               │
└──────────────────────────┬──────────────────────────────┘
                           │ supabase-py (anon key, read)
                           ▼
┌─────────────────────────────────────────────────────────┐
│  scripts/build_seo_pages.py   (Python + Jinja2)         │
│  • applies quality gate                                 │
│  • renders dish / cuisine-city / restaurant templates   │
│  • writes static HTML into landing-pages/               │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  landing-pages/                                         │
│  ├── fork-landing-cinematic.html      (homepage, hand)  │
│  ├── the-dish/                        (blog, hand)      │
│  ├── dish/<slug>.html                 (GENERATED)       │
│  ├── cuisine/<type>/<city>.html       (GENERATED)       │
│  ├── restaurant/<slug>.html           (GENERATED)       │
│  ├── sitemap.xml                      (GENERATED)       │
│  └── robots.txt                       (GENERATED)       │
└──────────────────────────┬──────────────────────────────┘
                           │ vercel --prod --yes
                           ▼
                     forkfox.ai
```

Zero runtime DB queries. Zero Next.js bundle. Rebuild = Python script + redeploy. Analytics snippets injected into the shared `_base.html.j2` template so every generated page gets GA4 automatically, and also hand-injected into the 7 existing handwritten pages.

---

# PART 0 — Excalidraw Visual Alignment (Execute THIS Session)

**This is the only part of the plan being executed in the current session.** Everything else (Parts 1-3 below) stays as-is for now. Ali asked for a medium-detail visual sketch of the entire system before any code is written so he can see what's being built and approve the direction.

## 0.1 — Deliverable

One large Excalidraw canvas (~6400 × 6000 px) divided into 11 clearly-labeled zones. Each zone is a self-contained diagram with its own header. Ali can pan/zoom around the canvas. Built via the `mcp__excalidraw__*` tools (create_element, update_element, group_elements, align_elements) which manipulate a single live Excalidraw scene.

**Visual conventions used throughout:**
- **ForkFox brand accents**: primary `#FA2A52`, accent `#F97316`, dark bg `#0a0a0a` on UI mockups to match the real site
- **System diagrams**: neutral grays + thin strokes for boxes, colored arrows for data flow
- **Page wireframes**: light background with dark text + colored accent blocks so structure is readable
- **Labels**: bold headers per zone, body text in Jinja-ish annotation
- **Roughness**: 1-2 (hand-drawn feel, matches Excalidraw voice we want to use on actual Atlas pages)

## 0.2 — Canvas Zone Layout

```
┌─────────────────────┬─────────────────────┬─────────────────────┐
│ Zone 1              │ Zone 2              │ Zone 3              │
│ End-to-End Pipeline │ Supabase Schema ERD │ Social Channel Matrix│
│ (data sources → DB  │ (tables + FK links) │ (9 platforms, volume│
│  → generator → HTML │                     │  content type, cost)│
│  → RSS → Postiz →   │                     │                     │
│  9 platforms)       │                     │                     │
├─────────────────────┼─────────────────────┼─────────────────────┤
│ Zone 4              │ Zone 5              │ Zone 6              │
│ Site Map Tree       │ Homepage Wireframe  │ /the-dish Blog      │
│ (current + new)     │ (current cinematic) │ (upgraded layout)   │
├─────────────────────┼─────────────────────┼─────────────────────┤
│ Zone 7              │ Zone 8              │ Zone 9              │
│ /about Page (NEW)   │ /atlas Landing (NEW)│ Postiz Dashboard    │
│                     │                     │ (calendar + queue)  │
├─────────────────────┴─────────────────────┴─────────────────────┤
│ Zone 10 — Four Atlas Example Pages (side by side)              │
│ A: Historical  │ B: Neighborhood │ C: Dish Anatomy │ D: Super. │
├──────────────────────────────────────────────────────────────────┤
│ Zone 11 — Social Post Mockups (one per page, different platform│
│ A→LinkedIn  │  B→Instagram  │  C→X  │  D→Threads  + universal  │
└──────────────────────────────────────────────────────────────────┘
```

## 0.3 — Zone Specifications

### Zone 1 — End-to-End Pipeline Flow (top-left, ~2000 × 1000)

A horizontal data-flow diagram showing the entire content-to-social pipeline.

**Elements:**
- **7 data source boxes** (left column, stacked): OpenStreetMap, Wikipedia/Wikidata, Library of Congress, NYPL Menu Collection, Chronicling America (newspapers 1700s-1963), Reddit JSON API, Firecrawl (public blogs)
- **All 7 sources → one arrow pointing right → "Supabase (marketing DB)" box**
- **Supabase box → "Python build script (scripts/build_seo_pages.py)" box** — annotated "25-75 pages/day, Jinja2 templates + Excalidraw diagram gen + Claude Haiku 4.5 writing"
- **Build script branches into 3 outputs**:
  - → "landing-pages/atlas/*.html" (static HTML files)
  - → "sitemap.xml" (auto-generated)
  - → "feed.xml" (RSS feed for social automation)
- **All HTML + sitemap → "Vercel" → "forkfox.ai"**
- **Separate: "Injection script (scripts/inject_analytics.py)" → annotated "runs before every deploy, tags all HTML with GA4 + GSC + Vercel Analytics snippets"**
- **RSS feed → "Postiz (self-hosted)" → fan-out to 9 platform icons**: X, LinkedIn, Facebook, Instagram, Threads, Bluesky, Mastodon, Pinterest, Google Business Profile
- **Reddit shown as separate gray box marked "MANUAL — anti-spam risk"**
- **Cost callouts**: annotate each stage with approximate cost ("$0", "~$0.003/page", etc.)

### Zone 2 — Supabase Data Schema ERD (top-center, ~1700 × 1000)

Entity-relationship diagram of the marketing Supabase tables (redesigned for local/historical content, NOT app data).

**Tables shown (with key fields):**
- **cities**: id, slug, name, state, region, founder_local_bool, is_priority, lat, lng
- **neighborhoods**: id, slug, name, city_id (FK), polygon_geojson, lat, lng, story_summary
- **places** (renamed from "restaurants" — covers restaurants/bars/cafes/markets/bakeries): id, slug, name, type, city_id (FK), neighborhood_id (FK), address, founded_year, closed_year (nullable), is_still_open, lat, lng, source_refs (jsonb)
- **content_sources**: id, source_type (osm/wiki/loc/nypl/reddit/firecrawl/chronicling), source_url, scraped_at, raw_content, normalized_data (jsonb), cost_cents
- **page_topics**: id, slug, type (historical/neighborhood/dish_anatomy/superlative/cuisine_city/comparison/etymology), scope_json, status (draft/queued/published/rejected), target_publish_date, priority
- **generated_pages**: id, topic_id (FK), url_path, title, meta_description, h1, body_html, hero_image_path, excalidraw_diagram_path, faq_jsonld, word_count, published_at, updated_at, gsc_impressions, gsc_clicks
- **social_posts**: id, generated_page_id (FK), platform, post_copy, image_url, scheduled_at, posted_at, post_url, engagement_json
- **page_queue**: id, topic_id (FK), status, generation_cost_usd, created_at

**Relationships drawn as arrows**: cities → neighborhoods (1:M), cities → places (1:M), neighborhoods → places (1:M), content_sources → page_topics (M:M via junction), page_topics → generated_pages (1:1), generated_pages → social_posts (1:M).

### Zone 3 — Social Channel Matrix (top-right, ~1700 × 1000)

A labeled table showing all 9 platforms with columns: Platform | Volume/Day | Post Type | Cost | Auto? | Status color dot.

Rows (all green-dot "full auto" unless noted):
- **LinkedIn** — 3-5/day — long-form commentary + link — $0 — ✅ full auto
- **Facebook** — 2-3/day — link card with excerpt — $0 — ✅ full auto
- **Instagram Feed** — 1-2/day — visual carousel — $0 — ✅ full auto (needs Business account)
- **Threads** — 5-10/day — conversational hook + link — $0 — ✅ full auto
- **Bluesky** — 5-10/day — punchy + link — $0 — ✅ full auto
- **Mastodon** — 5-10/day — casual + link — $0 — ✅ full auto
- **X / Twitter** — 3-5/day (curated) — 280-char hook — $0 (free tier 500/mo) — ⚠️ volume-limited
- **Pinterest** — 10-20/day — pin with image — $0 — ✅ full auto (great for food)
- **Google Business Profile** — 3-5/day — short blurb + image — $0 — ✅ full auto
- **Reddit** — 1-2/week — organic + relevant only — $0 — ❌ MANUAL (anti-spam)

**Right-side callout**: "Total auto volume/day: ~30-70 posts across 9 platforms. Monthly cost: ~$5-15 (Postiz VPS) + ~$11 LLM caption gen. All-in: ~$15-30/month."

### Zone 4 — Site Map Tree (middle-left, ~1500 × 1200)

A tree diagram showing the full planned site structure.

**Root**: `forkfox.ai`

**Existing branches** (current state, drawn in neutral gray):
- `/` (homepage, cinematic)
- `/the-dish/` (blog index — will be upgraded)
- `/privacy/`, `/support/`, `/socials/`, `/restaurants/`, `/gallery/`

**NEW branches** (drawn in ForkFox red to highlight):
- `/about/` — founder + mission page
- `/atlas/` — root of programmatic content
  - `/atlas/historical/<city>/<topic>` — e.g., `/atlas/historical/philadelphia/oldest-south-philly-italian-restaurants`
  - `/atlas/neighborhood/<city>/<neighborhood>` — e.g., `/atlas/neighborhood/philadelphia/fishtown`
  - `/atlas/dish/<slug>` — e.g., `/atlas/dish/cheesesteak`
  - `/atlas/superlative/<city>/<category>` — e.g., `/atlas/superlative/san-francisco/longest-running-seafood`
  - `/atlas/cuisine/<type>/<city>` — e.g., `/atlas/cuisine/thai/philadelphia`
  - `/atlas/comparison/<a>-vs-<b>` — e.g., `/atlas/comparison/pad-thai-vs-pad-see-ew`
  - `/atlas/term/<slug>` — e.g., `/atlas/term/gochujang`

**Annotations**: "~80% of Atlas pages = Philly + Bay Area local/historical. ~20% breaker content (general dish/cuisine/comparison)."

### Zone 5 — Current Homepage Wireframe (middle-center, ~1500 × 1200)

Wireframe of the existing `fork-landing-cinematic.html` homepage. Dark background block with white text to match real aesthetic.

**Sections stacked top-to-bottom:**
1. Top nav bar: ForkFox logo | `#discover` `#ai` `#cities` `/the-dish` | CTA button
2. Hero: "The world's first dish intelligence platform" + "AI scores every dish you eat — not the restaurant" + CTA + particle-ish background
3. Animated counter: "3,600+ dishes scored" (label: auto-counts up)
4. Cuisine scroll strip: 10 cuisine pills scrolling horizontally (Burmese, Chinese, Ethiopian, Indian, Japanese, Mexican, Pizza, Thai, Vietnamese + 1 more)
5. "AI Concierge powered by Claude" split section
6. "12 US Cities" map section
7. Signup/waitlist form
8. Footer: privacy / support / the-dish / socials / hello@forkfox.ai

**Label**: "Current state — keep as-is, add analytics + nav link to /atlas + /about in next phase."

### Zone 6 — Upgraded /the-dish Blog Wireframe (middle-right, ~1500 × 1200)

Proposed redesign of the blog index. Current state is a simple list of 9 articles; proposed state is a proper editorial hub.

**Sections:**
1. Top nav (same as homepage)
2. Blog header: "The Dish — ForkFox Intelligence Brief" + sub: "Hand-written deep dives on food, cities, and the algorithms that rank them"
3. Featured article: big full-width card with hero image, title, excerpt, byline, read time
4. Category filter chips: All | Dish Discovery | City Spotlights | The Algorithm | Score Reveals | Restaurant Intel | Historical
5. Grid of article cards (3-column desktop / 1-column mobile): each card = image + title + excerpt + date + category pill + read time
6. "Subscribe to The Dish" newsletter signup (captures email for future)
7. Cross-link block: "Explore the Atlas →" linking to `/atlas/`
8. Footer

**Annotation**: "Blog stays human-written. ~2-5 posts per week. Provides E-E-A-T authority signals that the Atlas inherits."

### Zone 7 — /about Page Wireframe (NEW) (second row left, ~1500 × 1100)

**Sections:**
1. Top nav
2. Hero: "We live where the food is. That's kind of the point." + subhead about being local founders
3. Founder split section:
   - LEFT: Ali Mabsoute (Philadelphia) — short bio, photo placeholder, "what I eat weekly in Philly" callout, LinkedIn link
   - RIGHT: Nik (Bay Area) — short bio, photo placeholder, "what I eat weekly in SF" callout, LinkedIn link
4. "Why ForkFox exists" — mission statement (the patent-pending algorithm origin story, why dish-level scoring matters, why apps that rate restaurants are broken)
5. "Where we are, where we're going" — map of current beta cities (Philly, SF) + planned expansion
6. "As seen in" / press bar — placeholder for future press mentions
7. Contact callout: `hello@forkfox.ai` + social links + "Want to pitch us a restaurant story? Email us."
8. Footer

**Annotation**: "Doubles as E-E-A-T signal for Google AND investor/fundraising landing page. Link heavily from /atlas and /the-dish."

### Zone 8 — /atlas Landing Page Wireframe (NEW) (second row center, ~1500 × 1100)

**Sections:**
1. Top nav
2. Hero: "The ForkFox Atlas" + sub: "A living encyclopedia of food in Philadelphia, the Bay Area, and beyond. Scored, mapped, and written by locals."
3. Stats row: "X pages · Y neighborhoods · Z cities · Updated daily"
4. Search bar: "Find a dish, neighborhood, restaurant, or era…"
5. "Browse by dimension" — 6 large tile cards:
   - 🗺 By Neighborhood
   - 🍜 By Dish
   - 🏛 By Era (historical)
   - 🏆 By Superlative (oldest, longest-running, etc.)
   - 🌏 By Cuisine
   - 🆚 Comparisons
6. "Latest added" — 6 recent atlas entries as small cards
7. Featured map section: interactive map of Philly + Bay Area with pin clusters (placeholder)
8. "Want to suggest an Atlas entry?" form → feeds page_queue table
9. Footer

**Annotation**: "This is the hub that links to every programmatic page. Critical for internal link graph and Google crawlability."

### Zone 9 — Postiz Dashboard Mockup (second row right, ~1800 × 1100)

A rough mockup of what the Postiz admin UI looks like (based on real Postiz screenshots I've seen — not pixel-perfect, but representative enough for Ali to understand what he'll be looking at).

**Sections:**
1. Top nav: `Dashboard` | `Posts` | `Calendar` | `Accounts` | `Settings`
2. Left sidebar: connected accounts list with status dots (X ✅, LinkedIn ✅, FB ✅, IG ✅, Threads ✅, Bluesky ✅, Pinterest ✅, GBP ✅)
3. Main area: **calendar week view** showing scheduled posts as colored blocks on each day, color = platform
4. Right sidebar: **queue list** showing next ~15 posts in order: `[Instagram] Mar 12 9:00am — "Fishtown coffee guide…"` etc.
5. Top action bar: `+ New Post` button, `Auto-import from RSS: forkfox.ai/feed.xml ✅`
6. Small analytics row at top: posts this week / engagement rate / upcoming scheduled

**Annotation**: "Postiz is self-hosted (Docker on a $5/mo VPS OR free Railway tier). Polls forkfox.ai/feed.xml every hour, auto-drafts posts, drip-feeds queue. ~15-30 min/week monitoring."

### Zone 10 — Four Atlas Example Page Wireframes (third row, 6400 × 1200)

Four page wireframes side by side, each ~1500 × 1100. Each represents a different Atlas content type so Ali can see the variety.

**Page A — Historical: "The 50 Oldest Restaurants in South Philadelphia, 1850–Present"**
- Breadcrumbs: Home › Atlas › Historical › Philadelphia › South Philly Restaurants
- Hero: **Excalidraw-generated timeline diagram** showing 50 restaurants as dots on a 1850-2025 horizontal axis, color-coded by still-open/closed, with a few labeled (City Tavern, Ralph's, Dante & Luigi's etc.)
- H1 + subhead + byline ("Written by Ali Mabsoute · Philadelphia, PA · Updated March 2026")
- Intro paragraph (~120 words)
- Data table: Restaurant | Founded | Neighborhood | Status | Notes | Source
- "The 10 oldest still open" callout section
- Map of locations (static Excalidraw-style)
- "How we verified this" methodology blurb (E-E-A-T gold)
- Related Atlas pages: "Oldest Italian spots in Philly" "Prohibition-era speakeasies"
- FAQ section (JSON-LD schema): "Which is the oldest continuously operating restaurant in Philly?" etc.
- CTA: "Get the ForkFox app"
- Footer

**Page B — Neighborhood: "Fishtown Food Guide: Every Spot Worth Knowing, Mapped"**
- Breadcrumbs: Home › Atlas › Neighborhoods › Philadelphia › Fishtown
- Hero: **Excalidraw-generated neighborhood map** showing Fishtown boundaries with dots for every restaurant/bar/cafe, labeled
- H1 + sub + byline
- "About Fishtown" — 100 word neighborhood intro (gentrification history, Frankford Ave food corridor)
- Categorized lists: Coffee (6) | Bars (11) | Dinner (18) | Breakfast (5) | Bakeries (3) | etc.
- "Where the locals actually go" — curated picks with short blurbs
- "3 walking routes" — suggested food tours
- Neighboring neighborhoods links
- FAQ schema
- CTA + footer

**Page C — Dish Anatomy: "Cheesesteak: Anatomy, Origin, Where to Eat One"**
- Breadcrumbs: Home › Atlas › Dishes › Cheesesteak
- Hero: **Excalidraw exploded-diagram** of a cheesesteak — bread, meat type, cheese choices, onions, other toppings, all labeled
- H1 + sub
- "Origin story" — Pat Olivieri 1930 hot dog stand, evolution
- "Anatomy" — component-by-component breakdown
- "The Great Debate" — Whiz vs Provolone vs American, "wit" vs "witout"
- "Where to eat one" — NOT scored (can't use app data), but historical/critical list: Pat's, Geno's, Jim's, John's, Dalessandro's, Ishkabibble's with founding dates from public sources
- "Common mistakes tourists make" — punchy section
- Related: hoagie, roast pork sandwich, Philly breakfast sandwich
- FAQ + CTA + footer

**Page D — Superlative: "12 Longest-Running Seafood Restaurants in San Francisco"**
- Breadcrumbs: Home › Atlas › Superlatives › San Francisco › Longest-Running Seafood
- Hero: **Excalidraw-generated bar chart** — 12 restaurants ranked by years in operation, color-coded by neighborhood
- H1 + sub + byline (Nik / Bay Area)
- Intro: "San Francisco has been a seafood town since 1849. Here are the 12 restaurants that have been serving fish longer than anyone else."
- Ranked list 1-12: each entry gets a mini-card with name, founding year, neighborhood, founder story, "what survived" section
- #1 Tadich Grill 1849 — big featured writeup
- "How many survived major events" — 1906 earthquake, Prohibition, dot-com bust, COVID
- Map of all 12
- Related: "Oldest continuously operating restaurants in SF" "Ferry Building history"
- FAQ + CTA + footer

### Zone 11 — Social Post Mockups (fourth row, 6400 × 1400)

Four social post mockups, each showing **actual copy** (not lorem ipsum) for one of the Atlas example pages above, rendered in the approximate visual style of the target platform (image size, text layout, platform chrome).

**Mockup 1 — Page A → LinkedIn post (square 1200×1200 image)**
- Image: Excalidraw timeline diagram (from Page A hero)
- Copy (~150 words):
  ```
  Before Geno's opened in 1966, before Pat's in 1930, before most of us
  were even born — there were restaurants in South Philly still serving
  tonight.

  I spent the weekend digging through Sanborn insurance maps, Chronicling
  America newspaper archives, and the NYPL historical menu collection to
  verify every claim.

  Ralph's on 9th Street has been open since 1900. Dante & Luigi's since
  1899. The oldest on the list opened before the Civil War.

  The full list, with founding dates, current status, and source links:
  → forkfox.ai/atlas/historical/philadelphia/oldest-south-philly-restaurants

  #Philadelphia #FoodHistory #SouthPhilly
  ```
- Mock LinkedIn chrome: profile circle, "ForkFox" name, "Food Intelligence · 2h" timestamp, engagement buttons

**Mockup 2 — Page B → Instagram feed post (square carousel 1080×1080)**
- Image: Excalidraw Fishtown map diagram + swipe indicator dots
- Caption (~200 words):
  ```
  FISHTOWN FOOD GUIDE ↓

  47 spots worth knowing, mapped by neighborhood corridors, categorized
  by what you're actually in the mood for.

  Coffee on Frankford Ave? We have 6 picks.
  Late-night bar food? 11 options.
  Sunday brunch that's not packed? We know 3.

  Swipe for:
  → The walk-only Frankford Ave strip
  → Where to actually get BYOB
  → What the locals REALLY order

  Made by someone who actually lives here. Not another listicle.

  Full guide + walking routes → link in bio

  #Fishtown #PhillyFood #PhiladelphiaEats
  ```
- Mock IG chrome: username, location tag, heart/comment/share/save icons

**Mockup 3 — Page C → X post (1200×675 landscape image)**
- Image: Excalidraw cheesesteak anatomy diagram
- Copy (280 chars):
  ```
  A cheesesteak has 4 components. The way you combine them is a class
  marker in Philadelphia.

  "Whiz wit" means something.
  "Provolone witout" means the opposite.

  We wrote the taxonomy.

  🔗 forkfox.ai/atlas/dish/cheesesteak
  ```
- Mock X chrome: profile, handle, timestamp, reply/retweet/like/bookmark counts

**Mockup 4 — Page D → Threads post (1080×1350 portrait image)**
- Image: Excalidraw bar chart of 12 longest-running SF seafood restaurants
- Copy (~300 chars):
  ```
  Tadich Grill has been serving fish in San Francisco since 1849.

  It survived: the 1906 earthquake. Prohibition. the Summer of Love.
  the dot-com bust. COVID. TikTok.

  We mapped every SF seafood restaurant older than 50 years.
  There are 12.

  forkfox.ai/atlas/superlative/san-francisco/longest-running-seafood
  ```
- Mock Threads chrome: profile circle, handle, timestamp, reply/repost/like/share

**Bottom strip of Zone 11** — a small "same page → 4 platforms" comparison showing how **Page A** gets transformed into 4 different post variants so Ali can see the platform-specific voice calibration (tiny thumbnails labeled X / LinkedIn / Instagram / Threads with one-line copy each).

## 0.4 — Tools Used

- `mcp__excalidraw__create_element` — rectangles, text, arrows, ellipses for every element
- `mcp__excalidraw__update_element` — fine-tuning position/color/text after initial placement
- `mcp__excalidraw__group_elements` — keeping related elements together per zone for easy later editing
- `mcp__excalidraw__align_elements` — cleaning up rows/columns within zones
- `mcp__excalidraw__query_elements` — introspection during build to track what's been placed

No Write tool needed — the Excalidraw MCP server holds the scene in memory and Ali can open it from the Excalidraw UI / export from the browser extension he has installed.

## 0.5 — Build Order (When Executing)

To avoid creating elements at wrong coordinates and having to reposition, build zones in this order:
1. Zone 1 (pipeline) — defines the canvas origin and visual voice
2. Zone 4 (sitemap) — small, defines left column baseline
3. Zone 2 (schema ERD) — heavy data, middle top
4. Zone 3 (social channel matrix) — right top
5. Zones 5, 6 (homepage + blog wireframes) — middle row
6. Zones 7, 8 (about + atlas landing) — middle-bottom row
7. Zone 9 (Postiz dashboard) — next to above
8. Zone 10 (4 Atlas example pages) — big horizontal strip
9. Zone 11 (social post mockups) — bottom strip
10. Final pass: labels, zone headers, connecting annotations

Estimated element count: ~400-600 elements total. Estimated build time: 30-60 minutes of tool calls.

## 0.6 — Verification (Part 0)

1. All 11 zones are visible and labeled on the canvas.
2. Each zone has a clear title/header element.
3. Zone 1's pipeline arrows flow left-to-right with no crossed lines.
4. Zone 2's ERD has visible FK relationships.
5. Zone 10's 4 example pages are distinguishable from each other by section headings.
6. Zone 11's social post mockups contain the actual copy strings as specified (not placeholder text).
7. Ali can open the canvas in Excalidraw and visually verify every zone renders.
8. No overlapping elements between adjacent zones.

## 0.7 — What Happens After Ali Reviews

- **If Ali approves the visual direction**: next session is full plan rewrite for Parts 1-3 to reflect the new local/historical strategy + social automation, then begin Phase 1 (analytics injection script + GA4 setup) once Ali provides the GA4 Measurement ID.
- **If Ali wants changes**: iterate on specific zones via `update_element` — cheap to change.
- **If Ali rejects the direction entirely**: tear down and rethink before writing any code.

---

> ⚠️ **STALE SECTIONS BELOW** — Parts 1-3 below reflect the OLD plan (app-data-based schema, generic dish/cuisine/restaurant routes). These sections are preserved for reference but need full rewrite in the next session to match the new local/historical strategy, no-app-data constraint, and social automation layer described in the Context section above. **Part 1 (Analytics) is still mostly valid** — just needs the injection script + RSS feed additions. **Parts 2-3 (schema + generator) need substantial rework.**

---

# PART 1 — Analytics Foundation (Execute First)

This is the only part of the plan with immediate file edits. It unblocks everything else.

## 1.1 — Google property creation (user steps, manual)

Claude cannot create the GA4 property or the GSC property for you — both require you to be logged into your Google account in a browser. Follow these exact steps, copy the IDs into a `.env` file, then I'll handle the injection.

### GA4 Property Creation

1. Go to **https://analytics.google.com** — sign in with the Google account you want to own the data.
2. Top-left gear icon (**Admin**) → under **Account**, click **Create** → **Account**.
   - Account name: `ForkFox`
   - Data sharing: leave defaults checked (unless you care, none are harmful).
3. Click **Next** → **Create property**.
   - Property name: `forkfox.ai`
   - Reporting time zone: `United States — Eastern Time` (Philly beta)
   - Currency: `US Dollar (USD)`
4. **Next** → Business details:
   - Industry: `Food & Drink`
   - Business size: `Small — 1 to 10 employees`
5. **Next** → Business objectives: check **Generate leads** and **Examine user behavior**.
6. **Create** → accept GA4 terms.
7. Data stream setup → **Web**:
   - Website URL: `https://forkfox.ai`
   - Stream name: `forkfox.ai — production`
   - Leave **Enhanced measurement** ON (captures scrolls, outbound clicks, video engagement, file downloads for free).
8. **Create stream**. Copy the **Measurement ID** shown at the top-right of the stream detail page — it looks like `G-XXXXXXXXXX` (10 alphanumeric chars after `G-`).
9. Paste it into `landing-pages/.env.local` as `GA4_MEASUREMENT_ID=G-XXXXXXXXXX` and share it with Claude, OR just paste it into the session — I will do the file injection.

### Google Search Console Verification

1. Go to **https://search.google.com/search-console** — same Google account.
2. Click **Add property** → choose **URL prefix** → enter `https://forkfox.ai` → **Continue**.
3. Verification methods will appear — choose **HTML tag**. GSC shows a meta tag like:
   ```
   <meta name="google-site-verification" content="AbC123_longstringhere" />
   ```
4. Copy **just the `content="..."` value** (the token, not the whole tag). Share it with Claude or paste it into `landing-pages/.env.local` as `GSC_VERIFICATION=AbC123_longstringhere`.
5. **Do NOT click "Verify" in the GSC UI yet** — the token must be live on forkfox.ai first, which happens after we inject + deploy.
6. After Claude injects and Ali deploys (`cd landing-pages && vercel --prod --yes`), return to GSC and click **Verify**.

### Vercel Analytics (no manual work required)

Vercel Analytics works by loading a single script from Vercel's edge. It's free on the Hobby plan. No property creation, no dashboard signup — Claude will inject the script tag and it starts showing data in the Vercel dashboard under the `landing-pages` (or `forkfox-ai`) project's **Analytics** tab.

### PostHog (deferred — not in this plan)

Original brief included PostHog. Deferring to a later session because:
- GA4 + Vercel Analytics cover 90% of what you need for a pre-launch beta site.
- PostHog is more valuable on the *app* (inside the mobile app funnel + backend), where session replay and funnels matter.
- Adding 4 separate scripts (GA4, Vercel, GSC, PostHog) at once inflates the `<head>` and makes debugging harder.

PostHog can be added in 15 minutes whenever you want. Not a blocker.

## 1.2 — Snippet to inject

This block gets inserted into all 7 live HTML files. The `{GA4_ID}` and `{GSC_TOKEN}` placeholders get filled in once Ali provides the values.

```html
<!-- Google Search Console verification -->
<meta name="google-site-verification" content="{GSC_TOKEN}">
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{GA4_ID}', { anonymize_ip: true });
</script>
<!-- Vercel Analytics -->
<script defer src="/_vercel/insights/script.js"></script>
```

**Design choices baked in:**
- `async` on gtag (doesn't block render).
- `anonymize_ip: true` (privacy-safe default, doesn't change what you see in the dashboard).
- Vercel Analytics uses the self-hosted `/_vercel/insights/script.js` path — it only works on Vercel deploys, which is exactly where forkfox.ai lives.
- **No consent banner.** Ali chose "Skip for now." This is defensible for a US-focused pre-launch beta. Revisit before EU expansion.

## 1.3 — Injection targets (exact line numbers)

Every live HTML file has a Google Fonts `<link>` line followed eventually by `</head>`. The snippet goes **immediately after the Google Fonts link, before the inline `<style>` block**. This ordering:
- Keeps external resource hints grouped together.
- Loads analytics before the ~1700-line inline CSS parses, so gtag can start recording early.
- Is consistent across all 7 files so future edits are trivial.

| # | File | Fonts `<link>` line | `</head>` line | Insert after line |
|---|---|---|---|---|
| 1 | `landing-pages/fork-landing-cinematic.html` | 14 | 162 | **14** |
| 2 | `landing-pages/privacy/index.html` | 9 | 82 | **9** |
| 3 | `landing-pages/support/index.html` | 9 | 88 | **9** |
| 4 | `landing-pages/the-dish/index.html` | 14 | 148 | **14** |
| 5 | `landing-pages/socials/index.html` | 13 | 78 | **13** |
| 6 | `landing-pages/restaurants/index.html` | 14 | 173 | **14** |
| 7 | `landing-pages/gallery/index.html` | 9 | 856 | **9** |

**Do NOT inject into:** `preview-redesign.html` (dev preview, not in `vercel.json` rewrites), `dishes/*.jpg` (image assets), `forkfox-logo.png`, or the generated `dish/*.html` files (they'll inherit the snippet via the Jinja2 base template — see Part 3).

## 1.4 — Verification (Part 1)

After injection + deploy:

1. **GSC verification**: go back to Search Console → click **Verify**. Should flip to green within ~30 seconds.
2. **GA4 realtime check**: open https://forkfox.ai in an incognito window. In GA4 go to **Reports → Realtime** — you should see 1 active user within 15 seconds.
3. **Snippet sanity check**: `curl -s https://forkfox.ai | grep -E "googletagmanager|google-site-verification|vercel/insights"` should return 3 matching lines.
4. **Repeat realtime test on 2 other pages**: visit `https://forkfox.ai/the-dish` and `https://forkfox.ai/privacy` in incognito. GA4 realtime should show both page_view events tagged with the correct `page_location`.
5. **PageSpeed sanity**: run https://pagespeed.web.dev/report?url=https://forkfox.ai — LCP should not regress more than ~100ms vs. pre-injection baseline (the gtag script is async + tiny).

---

# PART 2 — Supabase Database Design

## 2.1 — Supabase project setup (user steps, manual)

Same reason as GA4: Supabase project creation requires a browser login.

1. Go to **https://supabase.com** → sign in (GitHub or Google).
2. **New project**:
   - Organization: (use existing or create `ForkFox`)
   - Name: `forkfox-marketing`
   - Database password: generate and save to 1Password / password manager immediately
   - Region: `East US (North Virginia)` (closest to PA + lowest latency for the Vercel edge)
   - Plan: **Free** (500MB DB, 5GB bandwidth, sufficient for the entire lifetime of this site's marketing DB)
3. Wait ~2 minutes for provisioning.
4. From the project dashboard → **Project Settings → API** — copy:
   - **Project URL** → `SUPABASE_URL` in `.env.local`
   - **anon public key** → `SUPABASE_ANON_KEY` in `.env.local` (this is safe to commit to the frontend; the Python script will use it for read-only queries)
   - **service_role key** → keep ONLY in `.env.local` (never commit, never ship to frontend; the Python script uses it only for the initial seed/migrate)
5. Paste credentials into the session or `landing-pages/.env.local`.

## 2.2 — Schema (migration file: `supabase/migrations/0001_seo_schema.sql`)

Four tables. Lean on purpose. This schema was designed against the existing FastAPI `DishOut` / `DishScoreResponse` Pydantic models in `backend/app/models/schemas.py` so it mirrors the shape the backend already knows, but adds the fields pSEO needs (slugs, publish flag, city, neighborhood).

```sql
-- 0001_seo_schema.sql
-- marketing-only schema, separate from backend app DB

create extension if not exists "uuid-ossp";

-- ─────────────────────────────────────────────────────────
-- cities: one row per metro where the beta is live
-- ─────────────────────────────────────────────────────────
create table public.cities (
  id           uuid primary key default uuid_generate_v4(),
  slug         text not null unique,               -- 'philadelphia'
  name         text not null,                      -- 'Philadelphia'
  state        text not null,                      -- 'PA'
  region       text,                               -- 'philly-metro' | 'bay-area'
  is_live      boolean not null default false,     -- only pages for live cities get generated
  lat          numeric(9,6),
  lng          numeric(9,6),
  created_at   timestamptz not null default now()
);

-- ─────────────────────────────────────────────────────────
-- cuisines: controlled vocabulary
-- ─────────────────────────────────────────────────────────
create table public.cuisines (
  id           uuid primary key default uuid_generate_v4(),
  slug         text not null unique,               -- 'thai'
  name         text not null,                      -- 'Thai'
  description  text,                               -- 1-2 sentence blurb for hero
  created_at   timestamptz not null default now()
);

-- ─────────────────────────────────────────────────────────
-- restaurants: physical restaurants (beta scope)
-- ─────────────────────────────────────────────────────────
create table public.restaurants (
  id             uuid primary key default uuid_generate_v4(),
  slug           text not null unique,             -- 'pod-thai-fishtown-philadelphia'
  name           text not null,
  city_id        uuid not null references public.cities(id) on delete restrict,
  address        text,
  neighborhood   text,                             -- 'Fishtown'
  price_tier     smallint check (price_tier between 1 and 4),  -- $ to $$$$
  lat            numeric(9,6),
  lng            numeric(9,6),
  is_published   boolean not null default false,
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);
create index idx_restaurants_city on public.restaurants (city_id) where is_published;

-- ─────────────────────────────────────────────────────────
-- dishes: the core pSEO unit
-- ─────────────────────────────────────────────────────────
create table public.dishes (
  id               uuid primary key default uuid_generate_v4(),
  slug             text not null,                  -- 'pad-thai' (unique per restaurant, not global)
  name             text not null,                  -- 'Pad Thai'
  restaurant_id    uuid not null references public.restaurants(id) on delete cascade,
  cuisine_id       uuid not null references public.cuisines(id) on delete restrict,
  community_score  numeric(4,1) check (community_score between 0 and 100),
  rating_count     integer not null default 0,
  ai_summary       text,                           -- unique blurb per dish, 1-3 sentences
  image_url        text,
  is_published     boolean not null default false, -- quality-gate flag
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now(),
  unique (restaurant_id, slug)                     -- same dish name OK at different restaurants
);
create index idx_dishes_cuisine_score
  on public.dishes (cuisine_id, community_score desc)
  where is_published;
create index idx_dishes_restaurant
  on public.dishes (restaurant_id)
  where is_published;

-- ─────────────────────────────────────────────────────────
-- updated_at trigger (reusable)
-- ─────────────────────────────────────────────────────────
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin new.updated_at := now(); return new; end;
$$;
create trigger trg_restaurants_updated before update on public.restaurants
  for each row execute function public.touch_updated_at();
create trigger trg_dishes_updated before update on public.dishes
  for each row execute function public.touch_updated_at();
```

## 2.3 — Row Level Security (RLS)

Crucial: the Python generator uses the **anon key**, so RLS must be enabled and policies must grant read-only access to *published* rows only.

```sql
-- 0002_rls_policies.sql
alter table public.cities       enable row level security;
alter table public.cuisines     enable row level security;
alter table public.restaurants  enable row level security;
alter table public.dishes       enable row level security;

-- anon can SELECT live cities / all cuisines / published restaurants / published dishes
create policy anon_read_cities
  on public.cities for select to anon
  using (is_live = true);

create policy anon_read_cuisines
  on public.cuisines for select to anon
  using (true);

create policy anon_read_restaurants
  on public.restaurants for select to anon
  using (is_published = true);

create policy anon_read_dishes
  on public.dishes for select to anon
  using (is_published = true);

-- service_role bypasses RLS automatically — used only for seeds/migrations
```

## 2.4 — Quality-gate SQL views

These power the generator without duplicating logic in Python. Views inherit the RLS of their underlying tables.

```sql
-- 0003_seo_views.sql

-- top dishes per cuisine+city with at least 3 ratings
create or replace view public.v_dishes_full as
select
  d.id, d.slug, d.name, d.community_score, d.rating_count, d.ai_summary, d.image_url,
  r.id as restaurant_id, r.slug as restaurant_slug, r.name as restaurant_name,
  r.neighborhood, r.price_tier,
  c.id as city_id, c.slug as city_slug, c.name as city_name, c.state as city_state,
  cu.id as cuisine_id, cu.slug as cuisine_slug, cu.name as cuisine_name
from public.dishes d
join public.restaurants r  on r.id  = d.restaurant_id
join public.cities c       on c.id  = r.city_id
join public.cuisines cu    on cu.id = d.cuisine_id
where d.is_published = true
  and r.is_published = true
  and c.is_live      = true
  and d.rating_count >= 3;

-- cuisine+city candidates with enough dishes to justify a page (>= 5)
create or replace view public.v_cuisine_city_pages as
select cuisine_id, cuisine_slug, cuisine_name,
       city_id, city_slug, city_name, city_state,
       count(*) as dish_count,
       max(community_score) as top_score
from public.v_dishes_full
group by 1,2,3,4,5,6,7
having count(*) >= 5;

-- restaurant page candidates (>= 2 published dishes)
create or replace view public.v_restaurant_pages as
select restaurant_id, restaurant_slug, restaurant_name,
       city_slug, city_name, neighborhood,
       count(*) as dish_count,
       avg(community_score)::numeric(4,1) as avg_score
from public.v_dishes_full
group by 1,2,3,4,5,6
having count(*) >= 2;
```

## 2.5 — How to populate (options — pick one later)

Not part of this plan's execution — Ali will populate Supabase separately. Options, in order of effort:

1. **Manual SQL in Supabase SQL Editor** — fine for seeding the first 5-10 cities/cuisines/restaurants to test the generator end-to-end. Fastest path to validate the pipeline.
2. **CSV import via Supabase dashboard** — good for bulk-loading 200-500 dishes from a spreadsheet if Ali already has one.
3. **One-off Python script that reads from the FastAPI backend DB** — best if the backend already has clean scored data. Would live at `tastyr-iq/scripts/migrate_backend_to_marketing.py`, uses both DBs simultaneously, runs once, and is deleted afterwards. Deferred until Ali decides.

---

# PART 3 — Programmatic SEO Generator Pipeline

## 3.1 — Directory layout (to be created)

```
tastyr-iq/landing-pages/
├── .env.example                    # NEW (safe to commit)
├── .env.local                      # NEW (gitignored; real secrets)
├── .gitignore                      # MODIFIED (add .env.local)
├── supabase/
│   └── migrations/
│       ├── 0001_seo_schema.sql     # NEW
│       ├── 0002_rls_policies.sql   # NEW
│       └── 0003_seo_views.sql      # NEW
├── scripts/
│   ├── requirements.txt            # NEW
│   ├── build_seo_pages.py          # NEW — main generator
│   ├── build_sitemap.py            # NEW — walks generated HTML, emits sitemap.xml
│   ├── README.md                   # NEW — run instructions
│   └── templates/
│       ├── _base.html.j2           # NEW — shared head/nav/footer + analytics
│       ├── dish.html.j2            # NEW
│       ├── cuisine_city.html.j2    # NEW
│       └── restaurant.html.j2      # NEW
├── dish/                           # NEW (output dir, gitignored or committed per preference)
├── cuisine/                        # NEW
├── restaurant/                     # NEW
├── sitemap.xml                     # NEW (generated)
├── robots.txt                      # NEW (hand or generated)
└── vercel.json                     # MODIFIED (add /dish/*, /cuisine/*, /restaurant/* rewrites)
```

**Commit policy for generated output:** commit the generated HTML files to git. Reasons: (1) Vercel deploys from git, (2) it gives you a full diff when content changes, (3) it's text — storage is free, (4) rollback is `git revert`. The 500-file ceiling is trivial for git.

## 3.2 — Python dependencies (`scripts/requirements.txt`)

```
supabase>=2.0.0
jinja2>=3.1.0
python-slugify>=8.0.0
python-dotenv>=1.0.0
```

That's it. No numpy, no pandas, no requests. Keep it tight.

## 3.3 — `build_seo_pages.py` architecture

Single-file script, ~200 lines, structure:

```python
# Pseudocode shape — real script in a future session
def main():
    load_env()
    client = supabase.create_client(URL, ANON_KEY)
    env = jinja2.Environment(loader=FileSystemLoader("scripts/templates"))

    # 1. Fetch source data
    cuisine_city_rows = client.from_("v_cuisine_city_pages").select("*").execute()
    restaurant_rows   = client.from_("v_restaurant_pages").select("*").execute()
    dish_rows         = client.from_("v_dishes_full").select("*").execute()

    # 2. Render each route type
    render_cuisine_city_pages(env, cuisine_city_rows, dish_rows)
    render_restaurant_pages(env, restaurant_rows, dish_rows)
    render_dish_pages(env, dish_rows)

    # 3. Emit index of generated URLs for sitemap step
    write_generated_urls_index()

def render_dish_pages(env, dish_rows):
    tpl = env.get_template("dish.html.j2")
    for dish in dish_rows:
        related = related_dishes_for(dish, dish_rows)  # same cuisine+city, top 5
        html = tpl.render(
            dish=dish,
            related=related,
            seo_title=dish_title(dish),
            seo_description=dish_description(dish),
            analytics=load_analytics_config(),
        )
        path = f"dish/{dish['slug']}-{dish['restaurant_slug']}.html"
        write_file(path, html)
```

**Slug collision strategy for `/dish/*`:** combine dish slug + restaurant slug in the URL so `pad-thai-pod-thai-fishtown-philadelphia.html` is globally unique without needing a DB-level unique constraint on `dishes.slug`. Keeps DB flexible, URL unambiguous.

## 3.4 — SEO title / meta formulas

All titles stay under 60 chars, descriptions under 155 chars (Google truncation limits).

| Route | `<title>` formula | `<meta description>` formula |
|---|---|---|
| `/dish/<slug>-<restaurant>.html` | `{Dish Name} at {Restaurant} — ForkFox` | `{Dish Name} at {Restaurant} in {Neighborhood}, {City} scored {score}/100 by ForkFox AI across {rating_count} ratings. {ai_summary_first_sentence}` |
| `/cuisine/<type>/<city>.html` | `Best {Cuisine} in {City} — Scored by ForkFox` | `{dish_count} {Cuisine} dishes across {City} scored by ForkFox AI. Top pick: {top_dish} at {top_restaurant} ({top_score}/100).` |
| `/restaurant/<slug>.html` | `{Restaurant} in {City} — Best Dishes, Scored` | `{Restaurant} in {Neighborhood}, {City}. {dish_count} dishes scored by ForkFox AI. Highest-rated: {top_dish} ({top_score}/100).` |

## 3.5 — Page content blueprint per route

**Dish page (`dish.html.j2`)** — sections in order:
1. **Breadcrumbs:** `Home › {City} › {Cuisine} › {Dish Name}`
2. **Hero:** dish name, big score ring, restaurant name+neighborhood, price tier.
3. **AI summary:** the `ai_summary` field rendered as 2-3 paragraphs.
4. **Score context:** where this dish ranks among all {cuisine} dishes in {city}. One stat block.
5. **Restaurant card:** address, link to `/restaurant/<slug>`.
6. **Related dishes:** 5 other scored dishes in same (cuisine, city), linking to their dish pages.
7. **FAQ schema block (JSON-LD)**:
   - "How is {dish name} at {restaurant} scored?"
   - "How many ratings does this dish have?"
   - "What other {cuisine} dishes should I try in {city}?"
8. **CTA:** "Download ForkFox to rate this dish" → TestFlight link.
9. **Footer** (inherited from base).

**Cuisine+city page (`cuisine_city.html.j2`)**:
1. Breadcrumbs: `Home › {City} › {Cuisine}`
2. Hero: "Best {Cuisine} in {City}" + dish count + average score.
3. Ranked list (top 20): dish name, restaurant, neighborhood, score, CTA to dish page.
4. Neighborhood filter (client-side JS, optional — CSS-only `:target` selector works).
5. "Other cuisines in {City}" internal links block.
6. FAQ schema block:
   - "Where is the best {cuisine} in {city}?"
   - "How are these rankings calculated?"
   - "How many {cuisine} spots did ForkFox score in {city}?"
7. CTA + footer.

**Restaurant page (`restaurant.html.j2`)**:
1. Breadcrumbs: `Home › {City} › {Neighborhood} › {Restaurant}`
2. Hero: restaurant name, neighborhood, price tier, average dish score.
3. Full list of scored dishes, sorted by score descending.
4. Map embed placeholder (deferred — Google Maps iframe is free but requires API key).
5. "Other {top cuisine of this restaurant} in {city}" link to cuisine+city page.
6. FAQ schema block.
7. CTA + footer.

## 3.6 — `_base.html.j2` — shared design system

Extract from `fork-landing-cinematic.html` lines 15-18 (the inline CSS reset + color vars + font rules). Turn into a base template:

```jinja
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ seo_title }}</title>
<meta name="description" content="{{ seo_description }}">
<link rel="canonical" href="https://forkfox.ai{{ canonical_path }}">
<meta property="og:title" content="{{ seo_title }}">
<meta property="og:description" content="{{ seo_description }}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://forkfox.ai{{ canonical_path }}">
<meta property="og:image" content="{{ og_image or 'https://forkfox.ai/forkfox-logo.png' }}">
<link rel="icon" type="image/png" href="/forkfox-logo.png">
<link href="https://fonts.googleapis.com/css2?family=Geologica:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
{% include "_analytics.html.j2" %}
<style>{% include "_base.css" %}</style>
{% block extra_head %}{% endblock %}
</head>
<body>
  {% include "_nav.html.j2" %}
  {% block content %}{% endblock %}
  {% include "_footer.html.j2" %}
  {% if faq_schema %}<script type="application/ld+json">{{ faq_schema|tojson|safe }}</script>{% endif %}
  {% block breadcrumb_schema %}{% endblock %}
</body>
</html>
```

**Design tokens extracted from existing CSS:**
- `--bg: #0a0a0a;`
- `--primary: #FA2A52;`
- `--accent: #F97316;`
- Geologica (headings) + Inter (body) from Google Fonts

## 3.7 — `build_sitemap.py`

Walks every `.html` file under `landing-pages/` that's a live route (homepage + 6 hand pages + all generated pages), writes:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://forkfox.ai/</loc><priority>1.0</priority></url>
  <url><loc>https://forkfox.ai/the-dish</loc><priority>0.9</priority></url>
  <url><loc>https://forkfox.ai/cuisine/thai/philadelphia</loc><priority>0.8</priority></url>
  ...
</urlset>
```

Priority hierarchy: homepage 1.0 → top-level sections 0.9 → cuisine/city pages 0.8 → dish pages 0.7 → restaurant pages 0.6 → legal/support 0.3. `lastmod` pulled from `updated_at` on the source row.

Also emits `robots.txt`:
```
User-agent: *
Allow: /
Sitemap: https://forkfox.ai/sitemap.xml
```

## 3.8 — `vercel.json` updates

Append these rewrites (don't touch existing ones):

```json
{ "source": "/dish/:slug", "destination": "/dish/:slug.html" },
{ "source": "/cuisine/:cuisine/:city", "destination": "/cuisine/:cuisine/:city.html" },
{ "source": "/restaurant/:slug", "destination": "/restaurant/:slug.html" },
{ "source": "/sitemap.xml", "destination": "/sitemap.xml" },
{ "source": "/robots.txt", "destination": "/robots.txt" }
```

And a cache header for generated pages:
```json
{
  "source": "/(dish|cuisine|restaurant)/(.*)",
  "headers": [
    { "key": "Cache-Control", "value": "public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800" }
  ]
}
```

## 3.9 — Rollout strategy (phased)

| Phase | Scope | Goal |
|---|---|---|
| **0** | Part 1 only (analytics) | Start collecting baseline traffic data. No SEO work yet. |
| **1** | Seed Supabase with **5 cuisines × 2 cities = 10** cuisine-city pages + their dishes + restaurants. | Validate generator end-to-end. Deploy. Submit sitemap to GSC. |
| **2** | Expand to full Philly + Bay Area dataset. Target: 200-500 pages total past the quality gate. | Let Google index. Watch GA4 + GSC for 2-4 weeks. |
| **3** | Based on performance: add `/compare/<a>-vs-<b>`, expand to new cities, or iterate on thin-content pages. | Data-driven — don't scale blindly. |

Phase 0 is the only part this plan executes. Phases 1-3 are documentation for what comes next.

---

# Critical Files to Modify / Create

**Part 1 (this session's execution — 7 file edits):**
- `landing-pages/fork-landing-cinematic.html` (inject after line 14)
- `landing-pages/privacy/index.html` (inject after line 9)
- `landing-pages/support/index.html` (inject after line 9)
- `landing-pages/the-dish/index.html` (inject after line 14)
- `landing-pages/socials/index.html` (inject after line 13)
- `landing-pages/restaurants/index.html` (inject after line 14)
- `landing-pages/gallery/index.html` (inject after line 9)

**Part 1 (optional in-session — also pragmatic):**
- `landing-pages/.env.example` — document required env vars
- `landing-pages/.gitignore` — ensure `.env.local` is excluded
- `landing-pages/README.md` — short doc explaining analytics setup (create if absent)

**Part 2 + 3 (future session, after Ali populates Supabase):**
- Everything under `landing-pages/supabase/migrations/`
- Everything under `landing-pages/scripts/`
- `landing-pages/vercel.json` (add rewrites)
- Generated output under `landing-pages/dish/`, `cuisine/`, `restaurant/`

**Referenced existing patterns (for reuse, not modification):**
- Color tokens + font imports from `fork-landing-cinematic.html:15-18` → lift into `_base.html.j2`
- Nav + footer HTML from `fork-landing-cinematic.html` → lift into `_nav.html.j2` + `_footer.html.j2`
- OG tag structure from `fork-landing-cinematic.html:8-12` → pattern for `_base.html.j2`
- Existing `vercel.json` rewrite + cache-header syntax → pattern for new rules

---

# Verification (End-to-End)

**After Part 1 ships:**

1. `curl -s https://forkfox.ai | grep -c "googletagmanager"` → should return `1`.
2. `curl -s https://forkfox.ai/the-dish | grep -c "google-site-verification"` → should return `1`.
3. `curl -s https://forkfox.ai | grep -c "vercel/insights"` → should return `1`.
4. Open https://forkfox.ai in incognito, then GA4 **Reports → Realtime** → see 1 active user.
5. Click **Verify** in GSC → flips green within 30 seconds.
6. https://pagespeed.web.dev/report?url=https://forkfox.ai — verify LCP did not regress more than 100ms.
7. Repeat realtime test for /privacy, /support, /the-dish, /socials, /restaurants, /gallery — all 7 pages must fire `page_view` events.

**After Part 2 + 3 ship (future session):**

1. `python scripts/build_seo_pages.py` completes without errors, prints count of pages generated, and reports quality-gate rejections separately.
2. `python scripts/build_sitemap.py` emits `sitemap.xml` with at least N entries (where N ≥ phase target).
3. Spot-check 3 generated pages in a browser (dish page, cuisine+city page, restaurant page) — verify unique titles, meta descriptions, breadcrumbs, FAQ schema validates at https://validator.schema.org/.
4. `vercel --prod --yes` — verify deploy success.
5. Submit `https://forkfox.ai/sitemap.xml` to GSC → verify Google discovers ≥ 80% of URLs within 7 days.
6. Run https://pagespeed.web.dev on 2 random generated pages — both should score ≥ 90 on mobile.

---

# Out of Scope / Explicitly Deferred

- **PostHog** — will add later, more valuable on the app than the marketing site.
- **Consent Mode v2 / cookie banner** — Ali chose skip; revisit before EU expansion.
- **Next.js migration** — not happening; static HTML wins at this page count.
- **`/compare/<a>-vs-<b>` routes** — Phase 3, after core routes are indexed and earning traffic.
- **Google Maps embed on restaurant pages** — needs API key + billing setup, deferred.
- **Automated cron rebuild via GitHub Actions** — ship manual `vercel --prod` first, automate only once the pipeline has been trusted for 2+ weeks.
- **`/api/track` custom events endpoint** — GA4 + Vercel Analytics cover current needs; revisit if product-specific events become necessary.
- **Fixing missing OG tags on `/privacy` and `/support`** — noted but cosmetic; not in this plan.
- **Script-level migration from FastAPI backend DB to Supabase** — Ali will populate marketing Supabase manually or from CSV; sync script is a future decision.
- **PostHog, Segment, Amplitude, Mixpanel** — all deferred.
