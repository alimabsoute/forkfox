#!/usr/bin/env python3
"""ForkFox — B2B Restaurant Outreach Target List Builder (FOR-13)
Extracts restaurateurs from research-restaurateurs.md and writes
a ranked CSV ready for outreach execution.
"""

import re, csv, os

BASE = os.path.dirname(__file__)

PHILLY_PRIORITY = [
    "Marc Vetri", "Michael Solomonov", "Stephen Starr", "Jose Garces",
    "Michael Schulson", "Nicholas Elmi", "Kevin Sbraga", "Greg Vernick",
    "Erin O'Shea", "Ellen Yin", "Joe Cicala", "Valerie Safran",
]
BAY_AREA_PRIORITY = [
    "Stuart Brioza", "Nicole Krasinski", "Dominique Crenn", "Corey Lee",
    "David Kinch", "Mourad Lahlou", "Charles Phan", "Dennis Lee",
    "Daniel Patterson", "Chris Cosentino",
]


def tier(name, influence):
    name_upper = name.upper()
    if any(p.upper() in name_upper for p in PHILLY_PRIORITY[:6]):
        return "Tier 1 — Priority"
    if any(p.upper() in name_upper for p in PHILLY_PRIORITY[6:]):
        return "Tier 1 — Philly"
    if any(p.upper() in name_upper for p in BAY_AREA_PRIORITY[:5]):
        return "Tier 1 — Bay Area"
    if any(p.upper() in name_upper for p in BAY_AREA_PRIORITY[5:]):
        return "Tier 2 — Bay Area"
    if "HIGH" in influence:
        return "Tier 1 — Priority"
    if "MED" in influence.upper():
        return "Tier 2 — Outreach"
    return "Tier 3 — Long Game"


def extract_restaurateurs(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    contacts = []
    blocks = re.split(r"\n## \d+\.", content)

    for block in blocks[1:]:
        lines = block.strip().split("\n")
        name = lines[0].strip().lstrip("#").strip() if lines else ""

        restaurant = location = instagram = linkedin = influence = connection = ""

        for line in lines:
            l = line.strip()
            if l.startswith("- **Restaurant"):
                restaurant = re.sub(r"\*\*[^*]+\*\*:?\s*", "", l).strip("- ").strip()
            elif l.startswith("- **Location"):
                location = re.sub(r"\*\*[^*]+\*\*:?\s*", "", l).strip("- ").strip()
            elif l.startswith("- **Instagram"):
                instagram = re.sub(r"\*\*[^*]+\*\*:?\s*", "", l).strip("- ").strip()
            elif l.startswith("- **LinkedIn"):
                linkedin = re.sub(r"\*\*[^*]+\*\*:?\s*", "", l).strip("- ").strip()
            elif l.startswith("- **Community Influence"):
                influence = re.sub(r"\*\*[^*]+\*\*:?\s*", "", l).strip("- ").strip()
            elif l.startswith("- **Food/Tastyr Connection"):
                connection = re.sub(r"\*\*[^*]+\*\*:?\s*", "", l).strip("- ").strip()

        # Determine geography
        geo = "Philly" if "Philadelphia" in location or "PA" in location else \
              "Bay Area" if "San Francisco" in location or "CA" in location or "Oakland" in location else \
              "NJ/DE" if ("NJ" in location or "DE" in location or "New Jersey" in location) else \
              "Other"

        if name:
            t = tier(name, influence)
            contacts.append({
                "Name": name,
                "Restaurant / Group": restaurant[:80],
                "Geography": geo,
                "Outreach Tier": t,
                "Instagram": instagram[:40],
                "LinkedIn": linkedin[:80],
                "Influence": influence[:12],
                "ForkFox Connection": connection[:120],
                "Outreach Status": "Not Started",
                "Channel": "Email + LinkedIn",
                "Notes": "",
            })

    # Sort: Tier 1 first, then by geo (Philly, Bay Area, Other)
    geo_order = {"Philly": 0, "Bay Area": 1, "NJ/DE": 2, "Other": 3}
    tier_order = {"Tier 1 — Priority": 0, "Tier 1 — Philly": 1, "Tier 1 — Bay Area": 2,
                  "Tier 2 — Outreach": 3, "Tier 2 — Bay Area": 4, "Tier 3 — Long Game": 5}
    contacts.sort(key=lambda c: (tier_order.get(c["Outreach Tier"], 9), geo_order.get(c["Geography"], 9)))

    return contacts


def build():
    filepath = os.path.join(BASE, "docs", "research-restaurateurs.md")
    contacts = extract_restaurateurs(filepath)

    out_csv = os.path.join(BASE, "crm", "b2b-restaurant-outreach.csv")
    fieldnames = ["Name", "Restaurant / Group", "Geography", "Outreach Tier",
                  "Instagram", "LinkedIn", "Influence", "ForkFox Connection",
                  "Outreach Status", "Channel", "Notes"]

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)

    print(f"Built: {out_csv} ({len(contacts)} contacts)")

    # Print tier breakdown
    from collections import Counter
    tiers = Counter(c["Outreach Tier"] for c in contacts)
    for t, count in sorted(tiers.items()):
        print(f"  {t}: {count}")


if __name__ == "__main__":
    build()
