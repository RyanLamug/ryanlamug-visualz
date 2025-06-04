import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys


def fetch_page(url):
    """Fetch the content of a webpage."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_links(html, base_url):
    """Return a list of (anchor_text, absolute_url) tuples for each link."""
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        if text:
            abs_url = urljoin(base_url, a['href'])
            links.append((text, abs_url))
    return links


def extract_media(html, base_url):
    """Return a dictionary with lists of image and video URLs."""
    soup = BeautifulSoup(html, 'html.parser')
    images = [urljoin(base_url, img['src']) for img in soup.find_all('img', src=True)]
    videos = []
    for video in soup.find_all('video'):
        if video.get('src'):
            videos.append(urljoin(base_url, video['src']))
        for source in video.find_all('source', src=True):
            videos.append(urljoin(base_url, source['src']))
    return {'images': images, 'videos': videos}


def scrape(url):
    """Scrape links from the initial page and find media in each linked page."""
    page_html = fetch_page(url)
    links = parse_links(page_html, url)
    results = []
    for text, link_url in links:
        try:
            linked_html = fetch_page(link_url)
            media = extract_media(linked_html, link_url)
        except Exception as e:
            media = {'images': [], 'videos': []}
        results.append({'text': text, 'url': link_url, 'media': media})
    return results


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <url>")
        sys.exit(1)
    url = sys.argv[1]
    results = scrape(url)
    for entry in results:
        print(f"Text: {entry['text']}")
        print(f" Link: {entry['url']}")
        if entry['media']['images']:
            print(" Images:")
            for img in entry['media']['images']:
                print(f"  - {img}")
        if entry['media']['videos']:
            print(" Videos:")
            for vid in entry['media']['videos']:
                print(f"  - {vid}")
        print()


if __name__ == '__main__':
    main()
