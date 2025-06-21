# i18n.py

LANGUAGES = {
    "it": {
        "title": "YouTube to Audio",
        "change_theme": "🌓 Cambia Tema",
        "video_url": "🎵 URL del video YouTube:",
        "audio_format": "🎧 Formato audio:",
        "no_download": "Nessun download in corso",
        "select_folder": "Scegli cartella di destinazione",
        "download_audio": "⬇️ Scarica Audio",
        "open_folder": "📂 Apri cartella",
        "folder_label": "📁 Cartella:",
        "clear_log": "🧹 Pulisci log",
        "downloading": "⏳ Scaricamento in corso...",
        "download_complete": "✅ Download completato",
        "start_download": "Inizio download...",
        "success": "✅ File scaricato correttamente in: {}",
        "error_url": "❌ URL non valido o supportato",
        "error_download": "❌ Errore durante il download. Verifica l'URL o la connessione.",
        "error_ffmpeg": "❌ FFMPEG non trovato. Controlla il percorso in config.py.",
        "error_unknown": "❌ Errore sconosciuto durante il download.",
        "status": "Stato",
        "url_placeholder": "Incolla qui il link del video...",
        "audio_quality": "Qualità audio (kbps):",
    },
    "en": {
        "title": "YouTube to Audio",
        "change_theme": "🌓 Change Theme",
        "video_url": "🎵 YouTube Video URL:",
        "audio_format": "🎧 Audio Format:",
        "no_download": "No download in progress",
        "select_folder": "Choose Download Folder",
        "download_audio": "⬇️ Download Audio",
        "open_folder": "📂 Open Folder",
        "folder_label": "📁 Folder:",
        "clear_log": "🧹 Clear logs",
        "downloading": "⏳ Downloading...",
        "download_complete": "✅ Download completed",
        "start_download": "Starting download...",
        "success": "✅ File successfully downloaded to: {}",
        "error_url": "❌ Invalid or unsupported URL",
        "error_download": "❌ Download error. Check the URL or internet connection.",
        "error_ffmpeg": "❌ FFMPEG not found. Check the path in config.py.",
        "error_unknown": "❌ Unknown error during download.",
        "status": "Status",
        "url_placeholder": "Paste the video link here...",
        "audio_quality": "Audio quality (kbps):",
    }
}

# Funzione per ottenere il testo nella lingua corrente
def t(key, lang="it"):
    return LANGUAGES.get(lang, LANGUAGES["it"]).get(key, key)
