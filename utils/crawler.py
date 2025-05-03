import requests
from bs4 import BeautifulSoup

def crawl_xvideos(limit=300):
    url = "https://www.xvideos.com/?k=popular"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.select('div.thumb-inside')[:limit]
        results = []

        for card in cards:
            a = card.find_parent('a')
            if not a:
                continue

            href = a.get('href')
            img_tag = a.find('img')
            thumb = img_tag.get('data-src') if img_tag else ''
            title = a.get('title') or img_tag.get('alt', 'No Title') if img_tag else 'No Title'

            if href and thumb:
                results.append({
                    "video": f"https://www.xvideos.com{href}",
                    "thumb": thumb,
                    "title": title.strip()
                })

        return results

    except requests.RequestException as e:
        print(f"[Crawler] Request Error: {e}")
    except Exception as e:
        print(f"[Crawler] Parse Error: {e}")
    return []
