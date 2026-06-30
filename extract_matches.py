"""
extract_matches.py
-------------------
Pulls 2026 FIFA World Cup fixture data from openfootball (free, no API key)
and exports a flat, analysis-ready CSV: data/raw/matches.csv
"""

import csv
import requests
from pathlib import Path

# ─────────────────────────────────────────────
# 1. CONFIGURATION
# ─────────────────────────────────────────────
URL = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
OUTPUT_PATH = Path("data/raw/matches.csv")

FIELDNAMES = [
    "fixture_id", "match_date", "round", "group_name",
    "status_short", "home_team", "away_team",
    "home_goals", "away_goals",
]


# ─────────────────────────────────────────────
# 2. FLATTEN ONE MATCH → ONE CSV ROW
# ─────────────────────────────────────────────
def flatten_match(match: dict, fixture_id: int) -> dict:
    score      = match.get("score", {})
    ft         = score.get("ft", [None, None])
    home_goals = ft[0] if ft and len(ft) > 0 else None
    away_goals = ft[1] if ft and len(ft) > 1 else None
    status     = "FT" if home_goals is not None else "NS"

    # group name comes from the round field e.g. "Group A"
    round_name = match.get("round", "")
    group_name = round_name if round_name.startswith("Group") else "Knockout"

    return {
        "fixture_id":   fixture_id,
        "match_date":   match.get("date"),
        "round":        round_name,
        "group_name":   group_name,
        "status_short": status,
        "home_team":    match.get("team1"),
        "away_team":    match.get("team2"),
        "home_goals":   home_goals,
        "away_goals":   away_goals,
    }


# ─────────────────────────────────────────────
# 3. FETCH & SAVE
# ─────────────────────────────────────────────
def main():
    print("Fetching World Cup 2026 data from openfootball...")
    response = requests.get(URL, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(f"Request failed [{response.status_code}]")

    data    = response.json()
    matches = data.get("matches", [])
    print(f"  → {len(matches)} matches found in JSON.")

    rows = []
    for i, match in enumerate(matches, start=1):
        rows.append(flatten_match(match, fixture_id=i))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    completed = sum(1 for r in rows if r["status_short"] == "FT")
    upcoming  = sum(1 for r in rows if r["status_short"] == "NS")

    print(f"  → {len(rows)} total fixtures saved to '{OUTPUT_PATH}'")
    print(f"  → {completed} completed, {upcoming} upcoming")
    print("Done.")


if __name__ == "__main__":
    main()