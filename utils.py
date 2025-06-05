from config import SUPPORTED_FORMATS

def is_valid_url(url):
    return url.startswith("https://www.youtube.com/") or url.startswith("https://youtu.be/")

def validate_inputs(url, format_audio):
    if not url or not is_valid_url(url):
        return "URL non valido o mancante."
    if format_audio not in SUPPORTED_FORMATS:
        return f"Formato non supportato. Formati disponibili: {', '.join(SUPPORTED_FORMATS)}"
    return None
