# Configura e avvia il download dell'audio con yt-dlp, salvando nella cartella scelta

import os
import yt_dlp
from config import FFMPEG_PATH
from utils import validate_inputs

def download_audio(url, format_audio, output_folder, hook, audio_quality=None):
    error = validate_inputs(url, format_audio)
    if error:
        return False, error

    postprocessor_opts = {
        'key': 'FFmpegExtractAudio',
        'preferredcodec': format_audio,
    }
    if audio_quality:
        postprocessor_opts['preferredquality'] = audio_quality

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [postprocessor_opts],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True, f"✅ File scaricato correttamente in: {output_folder}"
    except yt_dlp.utils.DownloadError:
        return False, "❌ Errore durante il download. Verifica l'URL o la connessione a internet."
    except FileNotFoundError:
        return False, "❌ FFMPEG non trovato. Controlla il percorso in config.py."
    except Exception as e:
        print("Errore tecnico:", e)
        return False, "❌ Errore sconosciuto durante il download."