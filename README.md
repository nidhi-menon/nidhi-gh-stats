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

- **Forks and archived repos are excluded** from collection automatically
- **Each snapshot is dated yesterday** — the job runs at 9am UTC (~1–2am Pacific) so the previous day is fully complete before collection
- **Duplicate dates are deduplicated** — re-running the workflow on the same day replaces rather than appends
- To exclude specific repos from collection, add their short names to `EXCLUDE_REPOS` in `collect_stats.py`
- To hide repos from the widget without removing them from collection, add their short names to `WIDGET_EXCLUDE` in `portfolio-widget.html`
- To fix the display order of repo cards, edit `REPO_ORDER` in `portfolio-widget.html`

## Widget

Open `portfolio-widget.html` directly, embed it via `<iframe>`, or enable GitHub Pages on this repo.

The widget includes:
- **KPI cards** — total stars, forks, views, and clones across all repos
- **Trend chart** — top 5 repos by selected metric; click legend items to show/hide series
- **Repo cards** — stars, forks, views, and clones per repo; names link to GitHub
- **All repos table** — expandable ranked list sorted by selected metric
- **Top traffic sources** — referrers aggregated across all repos
