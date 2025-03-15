# main.py
import yt_dlp
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import json

VIDEO_URL = "https://youtube.com/shorts/Vfzn14BYkag"

# Load service account key from environment variable
key_info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_KEY'])
credentials = service_account.Credentials.from_service_account_info(
    key_info, scopes=['https://www.googleapis.com/auth/drive']
)
drive_service = build('drive', 'v3', credentials=credentials)

# Download video
ydl_opts = {
    'outtmpl': '/tmp/downloaded_video.%(ext)s',  # Use /tmp for GitHub Actions
    'format': 'best',
    'quiet': True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(VIDEO_URL, download=True)
    video_file = ydl.prepare_filename(info)

# Upload to Drive
file_metadata = {'name': os.path.basename(video_file)}
media = MediaFileUpload(video_file)
drive_service.files().create(body=file_metadata, media_body=media).execute()

os.remove(video_file)
print("Done!")
