# ryanlamug-visualz

Personal portfolio website

## Scraper Utility

This repository includes a simple Python script `scraper.py` for scraping a webpage.
It collects the anchor text and URL for each link on the page and attempts to find
images and videos on the linked pages.

### Usage

```bash
python scraper.py <url>
```

The script prints the text of each link, the link URL, and any images or videos
found on the linked page.
