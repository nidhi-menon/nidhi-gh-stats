# GitHub Stats Tracker

Nightly collection of stars, forks, views, clones, and referrer traffic across all public repos.

## Setup

1. Fork or clone this repo
2. In `.github/workflows/collect-stats.yml`, set `GH_USERNAME` to your GitHub username
3. In `portfolio-widget.html`, update `STATS_URL` to point at your raw `metrics-history.json`
4. Go to **Settings → Actions → General → Workflow permissions** → set to **Read and write**
5. Add a `STATS_TOKEN` secret (a personal access token with `repo` scope) — required for reading traffic data across all your repos
6. Run the workflow manually once from the Actions tab to generate the first snapshot

## What gets tracked

| Metric | Notes |
|---|---|
| Stars & forks | Cumulative totals |
| Views & clones (14d) | Rolling 14-day window, with daily breakdown |
| Top referrers | Up to 5 per repo, aggregated across repos in the widget |
| Release downloads | Cumulative, if releases exist |

> GitHub only retains traffic data for 14 days — start the nightly job early to build history.

## Behavior

- **Forks and archived repos are excluded** from collection
- **Each snapshot is dated yesterday** — the job runs at 2am PDT / 1am PST so the previous day is fully complete before collection
- **Duplicate dates are deduplicated** — re-running the workflow on the same day replaces rather than appends
- To exclude specific repos, add their short names to `EXCLUDE_REPOS` in `collect_stats.py`
- To fix the display order in the widget, edit `REPO_ORDER` in `portfolio-widget.html`

## Widget

Open `portfolio-widget.html` directly, embed it via `<iframe>`, or enable GitHub Pages on this repo.

The widget shows KPI cards, a trend chart (top 5 repos by selected metric, daily granularity for views/clones), a repo grid, and aggregated referrer traffic.
