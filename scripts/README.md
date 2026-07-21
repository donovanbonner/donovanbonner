# profile asset generators

Hand-authored SVG banners for the profile README (monochrome terminal
aesthetic, dark/light via `prefers-color-scheme`). Everything under `assets/`
is generated — edit these scripts, not the SVGs.

## scripts

- **`gen_svgs.py`** — header, section labels, whoami, work (NeuroScan AI),
  the "building in stealth" teaser, and footer. Pure/static; no network.
- **`gen_telemetry.py`** — the contribution heatmap + headline stats
  (`assets/contribs.svg`). Reads a GitHub contribution-calendar JSON.

Light variants are authored with dark ink; dark variants are derived by a
color swap, so the two never drift.

## regenerate locally

```bash
python3 scripts/gen_svgs.py

# telemetry needs the contribution calendar (private contributions included
# require a token belonging to you, e.g. gh's):
gh api graphql -f query='query { user(login:"donovanbonner"){
  repositories(ownerAffiliations:OWNER,isFork:false){ totalCount }
  contributionsCollection{ contributionCalendar{ totalContributions
    weeks{ contributionDays{ contributionCount date weekday } } } } } }' > /tmp/cal.json
python3 scripts/gen_telemetry.py
```

## auto-refresh

`.github/workflows/refresh-telemetry.yml` runs weekly (Mondays). It fetches the
live calendar and **only commits when the contribution total changes** — so the
repo log doesn't gain a bot commit every time the sliding 12-month window shifts.
The total is stored as an `<!-- total=N -->` marker in `contribs.svg` for the
comparison. Commits are authored by `github-actions[bot]`, so they never count
toward the contribution graph.

Needs a repo secret **`PROFILE_TOKEN`** — a classic PAT with the `read:user`
scope — so private contributions are counted. Without the secret the job skips
cleanly.
