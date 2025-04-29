import requests
from bs4 import BeautifulSoup

def crawl_xvideos(limit=30):
    url = "https://www.xvideos.com/?k=popular"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        cards = soup.select('div.thumb-inside')[:limit]
        results = []
        for card in cards:
            a = card.find_parent('a')
            href = a['href']
            thumb = a.find('img')['data-src'] if a.find('img') else ''
            title = a.get('title', 'No Title')
            results.append({
                "video": f"https://www.xvideos.com{href}",
                "thumb": thumb,
                "title": title
            })
        return results
    except Exception as e:
        print(f"[Crawler] Error: {e}")
        return []
