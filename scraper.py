import json
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (news-job-scraper learning project)"}


def scrape_news():
    """Top stories from Hacker News (static HTML, easy to scrape)."""
    res = requests.get("https://news.ycombinator.com/", headers=HEADERS, timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    items = []
    for row in soup.select("tr.athing"):
        link = row.select_one(".titleline > a")
        if not link:
            continue
        href = link["href"]
        if not href.startswith("http"):
            href = "https://news.ycombinator.com/" + href
        meta = row.find_next_sibling("tr")
        score = meta.select_one(".score") if meta else None
        site = row.select_one(".sitestr")
        items.append({
            "title": link.get_text(strip=True),
            "url": href,
            "site": site.get_text(strip=True) if site else "news.ycombinator.com",
            "points": int(score.get_text().split()[0]) if score else 0,
        })
    return items


def scrape_jobs():
    """Remote jobs from RemoteOK's public JSON feed."""
    res = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=15)
    res.raise_for_status()
    jobs = []
    for j in res.json()[1:]:  # first item is a legal notice
        if not j.get("position"):
            continue
        jobs.append({
            "title": j.get("position", ""),
            "company": j.get("company", ""),
            "location": j.get("location") or "Remote",
            "tags": (j.get("tags") or [])[:4],
            "url": j.get("url", ""),
            "date": (j.get("date") or "")[:10],
        })
    return jobs


def safe(fn):
    try:
        return fn()
    except Exception as e:
        print(f"{fn.__name__} failed: {e}")
        return []


if __name__ == "__main__":
    data = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "news": safe(scrape_news),
        "jobs": safe(scrape_jobs),
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data['news'])} news, {len(data['jobs'])} jobs")
