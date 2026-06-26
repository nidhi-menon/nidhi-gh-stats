import os, json, datetime, urllib.request, urllib.error

TOKEN = os.environ["GH_TOKEN"]
USERNAME = os.environ["GH_USERNAME"]
TODAY = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

# Add repo short names here to exclude them from tracking, e.g. {"repo-name"}
EXCLUDE_REPOS = set()

def gh(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code in (403, 404):
            return None
        raise

try:
    with open("metrics-history.json") as f:
        history = json.load(f)
except FileNotFoundError:
    history = {"meta": {"username": USERNAME, "created": TODAY}, "snapshots": []}

repos = gh(f"/users/{USERNAME}/repos?per_page=100&type=public")
if not repos:
    print("Could not fetch repos — check token permissions")
    exit(1)

# Replace any existing snapshot for today rather than appending a duplicate
history["snapshots"] = [s for s in history["snapshots"] if s["date"] != TODAY]
snapshot = {"date": TODAY, "repos": {}}

for repo in repos:
    if repo["fork"] or repo["archived"] or repo["name"] in EXCLUDE_REPOS:
        continue

    name = repo["full_name"]
    short = repo["name"]

    entry = {
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "watchers": repo["watchers_count"],
        "open_issues": repo["open_issues_count"],
        "language": repo.get("language"),
        "description": repo.get("description", ""),
    }

    clones = gh(f"/repos/{name}/traffic/clones")
    if clones:
        entry["clones_14d"] = clones["count"]
        entry["unique_cloners_14d"] = clones["uniques"]
        entry["clones_daily"] = [
            {"date": c["timestamp"][:10], "count": c["count"], "uniques": c["uniques"]}
            for c in clones.get("clones", [])
        ]
    else:
        entry["clones_14d"] = None
        entry["unique_cloners_14d"] = None
        entry["clones_daily"] = []

    views = gh(f"/repos/{name}/traffic/views")
    if views:
        entry["views_14d"] = views["count"]
        entry["unique_visitors_14d"] = views["uniques"]
        entry["views_daily"] = [
            {"date": v["timestamp"][:10], "count": v["count"], "uniques": v["uniques"]}
            for v in views.get("views", [])
        ]
    else:
        entry["views_14d"] = None
        entry["unique_visitors_14d"] = None
        entry["views_daily"] = []

    referrers = gh(f"/repos/{name}/traffic/popular/referrers")
    if referrers:
        entry["top_referrers"] = [
            {"source": r["referrer"], "count": r["count"], "uniques": r["uniques"]}
            for r in referrers[:5]
        ]
    else:
        entry["top_referrers"] = []

    popular_paths = gh(f"/repos/{name}/traffic/popular/paths")
    if popular_paths:
        entry["popular_paths"] = [
            {"path": p["path"], "count": p["count"]}
            for p in popular_paths[:3]
        ]
    else:
        entry["popular_paths"] = []

    releases = gh(f"/repos/{name}/releases")
    if releases:
        entry["release_downloads"] = sum(
            asset["download_count"]
            for release in releases
            for asset in release.get("assets", [])
        )
        entry["release_count"] = len(releases)
    else:
        entry["release_downloads"] = 0
        entry["release_count"] = 0

    snapshot["repos"][name] = entry
    print(f"  {short}: {entry['stars']} stars, {entry['forks']} forks, "
          f"{entry.get('views_14d', 'N/A')} views (14d)")

history["snapshots"].append(snapshot)

with open("metrics-history.json", "w") as f:
    json.dump(history, f, indent=2)

total_stars = sum(s["stars"] for s in snapshot["repos"].values())
print(f"\nDone: {len(snapshot['repos'])} repos, {total_stars} total stars on {TODAY}")
