# GitHub Stats Tracker

Nightly collection of stars, forks, views, clones, and referrer traffic across all public repos.

## Setup

1. Fork or clone this repo
2. In `.github/workflows/collect-stats.yml`, set `GH_USERNAME` to your GitHub username
3. In `portfolio-widget.html`, update `STATS_URL` to point at your raw `metrics-history.json`
4. Go to **Settings → Actions → General → Workflow permissions** → set to **Read and write**
5. Run the workflow manually once from the Actions tab to generate the first snapshot

## What gets tracked

| Metric | Notes |
|---|---|
| Stars & forks | Cumulative totals |
| Views & clones (14d) | Rolling 14-day window |
| Top referrers | Up to 5 per repo |
| Release downloads | Cumulative, if releases exist |

> GitHub only retains traffic data for 14 days — start the nightly job early to build history.

## Widget

Open `portfolio-widget.html` directly, embed it via `<iframe>`, or enable GitHub Pages on this repo.
