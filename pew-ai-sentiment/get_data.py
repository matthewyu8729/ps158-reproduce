"""Download Pew's published 2021–2026 AI sentiment table.
Requires: pip install beautifulsoup4
Run: python get_data.py
"""
from pathlib import Path
import subprocess
from datetime import datetime, timezone
import csv
import json
from bs4 import BeautifulSoup

URL = 'https://www.pewresearch.org/chart/democrats-are-now-more-likely-than-republicans-to-express-concern-about-the-use-of-ai-in-daily-life/'
OUT = Path(__file__).resolve().parent

def main():
    html = subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                           '--max-time', '60', URL], check=True, capture_output=True).stdout
    soup = BeautifulSoup(html, 'html.parser')
    tables = [t for t in soup.find_all('table') if 'Rep/Lean Rep' in t.get_text() and 'More concerned than excited' in t.get_text()]
    if len(tables) != 1:
        raise ValueError(f'Expected one sentiment table, found {len(tables)}')
    rows = []
    groups = ['U.S. adults', 'Rep/Lean Rep', 'Dem/Lean Dem']
    for tr in tables[0].select('tbody tr'):
        cells = [c.get_text(' ', strip=True) for c in tr.find_all('td')]
        if len(cells) != 5:
            raise ValueError(f'Unexpected row: {cells}')
        year, sentiment, *values = cells
        for group, value in zip(groups, values):
            rows.append(dict(year=int(year), group=group, sentiment=sentiment, percent=float(value)))
    assert len(rows) == 54, 'Source coverage changed: review before updating'
    assert {r['year'] for r in rows} == set(range(2021, 2027))
    assert all(0 <= r['percent'] <= 100 for r in rows)
    assert len({(r['year'], r['group'], r['sentiment']) for r in rows}) == len(rows)
    (OUT / 'pew_source.html').write_bytes(html)
    with (OUT / 'ai_sentiment.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['year', 'group', 'sentiment', 'percent'])
        writer.writeheader()
        writer.writerows(rows)
    (OUT / 'source.json').write_text(json.dumps({
        'url': URL, 'retrieved_utc': datetime.now(timezone.utc).isoformat(),
        'latest_fieldwork': 'June 22–28, 2026',
        'note': 'Published rounded percentages; party groups include leaners. Nonresponses not shown. No renormalization.'
    }, indent=2))
    print(f'Downloaded {len(rows)} observations to {OUT / "ai_sentiment.csv"}')

if __name__ == '__main__':
    main()
