# ForkFox v1 Launch Metrics Plan

## Primary Success Metric
**100 organic installs within 7 days of launch.**

## Tracking Stack (assumed/to confirm)
- **App Store Connect**: Install counts, product page views, conversion rate
- **PostHog** (or Mixpanel): In-app events, funnels, retention
- **Crashlytics**: Crash-free rate, crash reports

---

## Day-of-Launch Dashboard

### App Store Connect (check every 4h post-launch)
| Metric | Target | Threshold |
|--------|--------|-----------|
| Installs (cumulative) | 100 by Day 7 | <10 by Day 1 = flag |
| Product page views | — | Monitor for conversion rate |
| Conversion rate | >20% | <10% = optimize listing |
| Crash-free rate | >99.5% | <98% = emergency patch |
| Avg rating | ≥4.2 | <4.0 = review strategy |

### In-App Funnel (PostHog)
```
install
  → app_opened
    → onboarding_started
      → onboarding_completed        (target: >70%)
        → first_dish_viewed
          → first_dish_score_seen   (target: >60% of completions)
            → dish_saved            (engagement signal)
```

### Retention
| Day | D1 | D3 | D7 |
|-----|----|----|-----|
| Target | 30% | 20% | 15% |

---

## Event Schema

```json
// Core dish events
{ "event": "dish_viewed", "properties": { "dish_id": str, "cuisine": str, "score": int, "source": "feed|search|share" } }
{ "event": "dish_scored_seen", "properties": { "dish_id": str, "time_on_screen_sec": float } }
{ "event": "dish_saved", "properties": { "dish_id": str, "cuisine": str } }

// Search/filter events
{ "event": "search_query", "properties": { "query": str, "results_count": int } }
{ "event": "filter_applied", "properties": { "filter_type": "cuisine|value|spice|quality", "value": str } }

// Session
{ "event": "session_start", "properties": { "source": "direct|notification|share_link" } }
```

---

## Post-Launch Response Playbook

### If installs stall (<10 by Day 2)
1. Amplify on Twitter/Instagram with demo video
2. Push to ForkFox CRM contact list (outreach/)
3. Pitch to food bloggers (docs/research-food-bloggers.md)
4. ASO: A/B test first screenshot caption

### If crash rate >1%
1. Pull Crashlytics report immediately
2. Assess if crash is in onboarding (critical path) or secondary flow
3. If onboarding: expedite patch, submit for expedited review
4. If secondary: note in What's New, patch in v1.0.1

### If rating drops below 4.0
1. Review recent 1-3 star reviews for patterns
2. Respond to reviews with fix ETA if bug-related
3. Trigger in-app rating prompt only after `dish_saved` (positive signal gate)

---

*Created: 2026-04-10 — FOR-3 Track 3*
