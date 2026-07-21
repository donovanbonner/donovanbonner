#!/usr/bin/env python3
"""Fetch donovanbonner's contribution calendar from an ANONYMOUS public API and
write it in the shape gen_telemetry.py expects. No token required.

This works because "Include private contributions on my profile" is enabled, so
the public contribution graph (and anything that scrapes it) already counts the
private contributions. `SRC` may point at a local jogruber-format JSON for
offline testing.
"""
import json, os, urllib.request
from datetime import date, timedelta

USER = os.environ.get("GH_USER", "donovanbonner")
OUT = os.environ.get("CAL_JSON", "/tmp/cal.json")
SRC = os.environ.get("SRC")  # optional local jogruber-format file for testing


def load():
    if SRC:
        return json.load(open(SRC))
    url = f"https://github-contributions-api.jogruber.de/v4/{USER}?y=all"
    req = urllib.request.Request(url, headers={"User-Agent": "profile-telemetry"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


counts = {c["date"]: c["count"] for c in load().get("contributions", [])}

today = date.today()
# grid ends on the Saturday of the current week and spans 53 weeks (like GitHub)
end_sat = today + timedelta(days=(6 - today.isoweekday() % 7))
start_sun = end_sat - timedelta(days=53 * 7 - 1)

weeks, d = [], start_sun
while d <= end_sat:
    days = []
    for _ in range(7):
        iso = d.isoformat()
        cnt = counts.get(iso, 0) if d <= today else 0
        days.append({"contributionCount": cnt, "date": iso, "weekday": d.isoweekday() % 7})
        d += timedelta(days=1)
    weeks.append({"contributionDays": days})

# headline number = GitHub-style rolling last 365 days (exclude future padding)
total = sum(counts.get((today - timedelta(days=n)).isoformat(), 0) for n in range(365))

out = {"data": {"user": {
    "contributionsCollection": {"contributionCalendar": {
        "totalContributions": total, "weeks": weeks}}}}}
open(OUT, "w").write(json.dumps(out))
print(f"wrote {OUT}: rolling-365 total={total}, weeks={len(weeks)}")
