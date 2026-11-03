# Daily Feed: News and Job Scraper

A Python scraper collects top tech news (Hacker News) and remote jobs (Remote OK),
saves them to `data.json`, and a responsive web page (`index.html`) shows them with tabs and search.
GitHub Actions refreshes the data every 6 hours and GitHub Pages hosts the page.

## Run locally
```bash
pip install -r requirements.txt
python scraper.py          # creates data.json
python -m http.server      # open http://localhost:8000
```

## Host on GitHub
1. Create a public repo and upload all files (including the `.github` folder).
2. Settings > Pages > Deploy from a branch > `main` / root.
3. Actions > "Update data" > Run workflow.
4. Open `https://<username>.github.io/<repo>/`.

## Files
- `scraper.py`: scraping logic
- `index.html`: user interface
- `.github/workflows/scrape.yml`: scheduled automation
- `requirements.txt`: Python libraries
