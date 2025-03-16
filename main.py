import yt_dlp
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

VIDEO_URL = "https://youtube.com/shorts/IfhmGncKxr8?si=TRluM1eO-477JuBL"  # Replace with your desired YouTube Short URL

# Download YouTube Short with yt_dlp
ydl_opts = {
    'outtmpl': 'video.%(ext)s',
    'format': 'best',
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([VIDEO_URL])
    info = ydl.extract_info(VIDEO_URL, download=False)
    video_file = f"video.{info['ext']}"

# Authenticate with Google Drive
key_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY"))
creds = service_account.Credentials.from_service_account_info(
    key_info,
    scopes=["https://www.googleapis.com/auth/drive"]
)
drive_service = build("drive", "v3", credentials=creds)

# Upload to Google Drive
file_metadata = {"name": video_file}
media = MediaFileUpload(video_file)
drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

# Clean up
os.remove(video_file)
