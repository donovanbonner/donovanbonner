# profile asset generators

Hand-authored SVG banners for the profile README (monochrome terminal
aesthetic, dark/light via `prefers-color-scheme`). Everything under `assets/`
is generated — edit these scripts, not the SVGs.

## scripts

- **`gen_svgs.py`** — header, section labels, whoami, work (NeuroScan AI),
  the "building in stealth" teaser, and footer. Pure/static; no network.
- **`fetch_cal.py`** — pulls the contribution calendar from an anonymous public
  API (no token) into the JSON `gen_telemetry.py` expects. Works because
  "Include private contributions on my profile" is enabled, so the public data
  already counts private contributions.
- **`gen_telemetry.py`** — the contribution heatmap + headline stats
  (`assets/contribs.svg`). Reads the calendar JSON `fetch_cal.py` writes.

Light variants are authored with dark ink; dark variants are derived by a
color swap, so the two never drift.

## regenerate locally

```bash
python3 scripts/gen_svgs.py
python3 scripts/fetch_cal.py      # anonymous; writes /tmp/cal.json
python3 scripts/gen_telemetry.py  # draws assets/contribs.svg from it
```

## auto-refresh

`.github/workflows/refresh-telemetry.yml` runs daily, **no token or secret
required**. It fetches the public calendar via `fetch_cal.py` and **only commits
when the contribution total changes** — so the repo log doesn't gain a bot commit
every day the sliding 12-month window shifts. The total is stored as
an `<!-- total=N -->` marker in `contribs.svg` for the comparison. Commits are
authored by `github-actions[bot]`, so they never count toward the contribution
graph.
