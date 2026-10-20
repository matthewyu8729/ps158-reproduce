# U.S. attitudes toward AI, 2021–2026

## Figure

An Economist-inspired, three-panel line chart shows the percentages feeling **more concerned than excited**, **equally concerned and excited**, or **more excited than concerned** about increased AI use in daily life. Each panel compares Republicans (including leaners), Democrats (including leaners), and all U.S. adults. Labels show 2021 and 2026 values and the change in percentage points.

The figure is saved as `ai_sentiment_2021_2026.png`, `.svg`, and `.pdf`.

## Data

The data come from [Pew Research Center’s published chart table](https://www.pewresearch.org/chart/democrats-are-now-more-likely-than-republicans-to-express-concern-about-the-use-of-ai-in-daily-life/), published September 16, 2026. The latest survey was conducted June 22–28, 2026.

`get_data.py` downloads the source HTML and extracts 54 published percentages into `ai_sentiment.csv`. It also saves `pew_source.html` and provenance in `source.json`. Percentages are rounded; nonresponses are omitted without rescaling, so totals may not equal 100%.

## Rerun

Requires Python 3.9+ and `curl`. From this folder, run:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python get_data.py
python plot.py
```

To redraw using the included CSV, skip `python get_data.py`. Outputs are written beside the scripts. The downloader validates the 2021–2026 coverage; future source changes may require updating it.
