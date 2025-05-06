from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from .r2_manager import load_existing_media
import time

def setup_driver():
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def crawl_xvideos(limit=112):
    existing = load_existing_media(source='xvideos')
    existing_urls = set(item["video"] for item in existing)
    results = existing.copy()

    driver = setup_driver()

    for page in range(1, limit + 1):
        url = f"https://www.xvideos.com/best/2025-04/{page}"
        print(f"[Crawl] Page {page}: {url}")
        try:
            driver.get(url)
            time.sleep(2)  # chờ page load xong
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            cards = soup.select('div.thumb-inside')
            cards = soup.select('div.thumb-inside')
            for card in cards:
                a = card.find("a")
                if not a:
                    print("[Crawl] No <a> tag found inside card.")
                    continue

                href = a.get('href')
                print(f"[Crawl] Found href: {href}")
                full_url = f"https://www.xvideos.com{href.strip()}" if href else None

                img_tag = a.find('img')
                thumb = img_tag.get('src') if img_tag else ''
                print(f"[Crawl] Found thumb: {thumb}")
                
                # Tìm .thumb-under là sibling kế tiếp
                sibling = card.find_next_sibling('div', class_='thumb-under')
                if not sibling:
                    print("[Crawl] Không tìm thấy sibling .thumb-under")
                    continue
                link_tag = sibling.select_one('p.title a')
                title = (link_tag.get('title') or link_tag.text).strip()
                print(f"[Crawl] Found title: {title}")

                if full_url and thumb:
                    # print(f"[Crawl] Found: {full_url} - {title.strip()}")
                    results.append({
                        "video": full_url,
                        "thumb": thumb,
                        "title": title.strip()
                    })

                    existing_urls.add(full_url)

        except Exception as e:
            print(f"[Crawler] Error: {e}")

    driver.quit()
    return results
