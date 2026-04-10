# ForkFox — Onboarding Flow Spec (v1)

## Goal
First-time users pick their cuisine preferences in under 30 seconds so the home feed is personalized from the first tap.

## Screens

### Screen 0 — Splash / Welcome (1.5s auto-advance)
- ForkFox logo + tagline: "Outsmart any menu."
- Dark background, FA2A52 accent
- Auto-advances; no user input needed

---

### Screen 1 — Value Prop Carousel (swipeable, 3 cards)

**Card 1**
- Headline: "Rate the dish. Not the restaurant."
- Sub: "A 4-star restaurant can hide 2-star food."
- Illustration: Split rating graphic (restaurant ★★★★ vs dish 38/100)

**Card 2**
- Headline: "2,500+ dishes. AI-scored."
- Sub: "We aggregate critic ratings, social signals, and diner feedback into one Dish Score."
- Illustration: Score card UI mockup

**Card 3**
- Headline: "Know before you order."
- Sub: "Browse, filter, and save the dishes worth ordering."
- Illustration: Browse feed with filters open

CTA: "Get Started" button (skip option top-right)

---

### Screen 2 — Cuisine Preference (multi-select)

**Header**: "What are you craving?"
**Sub**: "Pick your favorites. We'll prioritize those dishes."

**Options (grid 3x4):**
| Icon | Label |
|------|-------|
| 🍕 | Pizza |
| 🍜 | Japanese |
| 🌮 | Mexican |
| 🍛 | Indian |
| 🥡 | Chinese |
| 🍝 | Italian |
| 🫙 | Thai |
| 🥩 | Ethiopian |
| 🍲 | Burmese |
| 🥘 | Vietnamese |

**Behavior**: Tap to toggle (highlight selected). Minimum 1 required. "All" shortcut selects all.

**CTA**: "Show My Dishes →"

---

### Screen 3 — Location Permission (optional)

**Header**: "Find dishes near you?"
**Sub**: "We'll prioritize dishes from restaurants in your city. No location data is stored."

Buttons:
- "Allow Location" (primary, #FA2A52)
- "Not now" (text link, skips)

---

### Screen 4 — Notifications Permission (optional)

**Header**: "Get dish drops?"
**Sub**: "We'll notify you when a new top-rated dish hits your favorite cuisine."

Buttons:
- "Turn on Notifications" (primary)
- "Maybe later" (text link, skips)

---

### Screen 5 — Home Feed (onboarding complete)

Drop user into personalized home feed filtered to their selected cuisines.

**First-launch toast**: "Your top dishes are ready. Tap any dish to see its full score." (auto-dismiss 3s)

---

## Analytics Events

| Event | Trigger | Properties |
|-------|---------|------------|
| `onboarding_started` | Screen 0 shown | `source: fresh_install` |
| `onboarding_carousel_completed` | All 3 cards swiped | `swipe_count: int` |
| `onboarding_cuisines_selected` | Screen 2 CTA tapped | `cuisines: [array]`, `count: int` |
| `onboarding_location_granted` | Location allowed | — |
| `onboarding_location_skipped` | "Not now" tapped | — |
| `onboarding_notifications_granted` | Notifications allowed | — |
| `onboarding_notifications_skipped` | "Maybe later" tapped | — |
| `onboarding_completed` | Home feed shown | `duration_sec: float` |

---

## Acceptance Criteria

- [ ] Onboarding shown only on first launch (persisted via UserDefaults / AsyncStorage)
- [ ] Minimum 1 cuisine required before advancing past Screen 2
- [ ] Location and notification prompts are skippable — never required
- [ ] Completing onboarding sets `onboardingComplete = true` in local storage
- [ ] Feed on Screen 5 is pre-filtered to selected cuisines, not empty
- [ ] All 7 analytics events fire correctly and appear in PostHog

---

*Spec created: 2026-04-10 — FOR-3 Track 2*
