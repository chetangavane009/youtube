from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import json
import time

VIDEO_URL = "https://youtube.com/shorts/Vfzn14BYkag"

# Set up headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

# Load service account key
key_info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_KEY'])
credentials = service_account.Credentials.from_service_account_info(
    key_info, scopes=['https://www.googleapis.com/auth/drive']
)
drive_service = build('drive', 'v3', credentials=credentials)

# Navigate to video and download (simplified; adjust based on Shorts behavior)
driver.get(VIDEO_URL)
time.sleep(5)  # Wait for page to load (adjust as needed)

# Note: Direct download via Selenium for Shorts is tricky; you may need a browser extension or manual click simulation
# For now, this is a placeholder. You’d need to extract the video URL or use a download helper.
print("Download logic needs implementation for Shorts; see notes below.")
video_file = "/tmp/downloaded_video.mp4"  # Placeholder path

# Upload to Drive (assuming download succeeds)
file_metadata = {'name': os.path.basename(video_file)}
media = MediaFileUpload(video_file)
drive_service.files().create(body=file_metadata, media_body=media).execute()

driver.quit()
os.remove(video_file)  # Clean up if file exists
print("Done!")
