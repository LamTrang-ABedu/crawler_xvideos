import os
import requests
import json
import time
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Cấu hình Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'
DRIVE_FOLDER_ID = '1qYDmgDAv56HmRevKei1d8SexTmNujxYp'  # <-- Thay bằng ID thư mục Google Drive của bạn

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# Crawl Xvideos
def crawl_xvideos(limit=10):
    url = 'https://www.xvideos.com/?k=popular'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = []
    for card in soup.select('div.thumb-inside')[:limit]:
        a = card.find_parent('a')
        if not a or not a.find('img'):
            continue
        thumb_url = a.find('img')['data-src']
        title = a.get('title', 'No Title').strip()
        results.append({'title': title, 'thumb': thumb_url})
    return results

# Download ảnh/video về local
def download_media(url, filename):
    r = requests.get(url, stream=True, timeout=10)
    if r.ok:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

# Upload file lên Google Drive
def upload_to_drive(filepath, filename):
    file_metadata = {'name': filename, 'parents': [DRIVE_FOLDER_ID]}
    media = MediaFileUpload(filepath)
    file = drive_service.files().create(
        body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# Main crawler runner
def run_crawler():
    medias = crawl_xvideos(limit=10)
    for media in medias:
        filename = media['title'].replace('/', '_') + '.jpg'
        try:
            print(f"[Info] Downloading {media['thumb']}...")
            download_media(media['thumb'], filename)
            print(f"[Info] Uploading {filename} to Drive...")
            upload_to_drive(filename, filename)
            os.remove(filename)
            print(f"[Success] {filename} uploaded and deleted local file.")
            time.sleep(5)  # Thả nhẹ cho Drive không bị spam
        except Exception as e:
            print(f"[Error] {filename} failed: {e}")

if __name__ == "__main__":
    run_crawler()
