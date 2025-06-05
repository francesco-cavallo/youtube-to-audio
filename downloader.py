import os
import yt_dlp
from config import FFMPEG_PATH
from utils import validate_inputs

def download_audio(url, format_audio, output_folder, hook):
    error = validate_inputs(url, format_audio)
    if error:
        return error

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_audio,
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"✅ File scaricato correttamente in: {output_folder}"
    except Exception as e:
        return f"❌ Errore: {e}"
