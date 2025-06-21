import os

FFMPEG_PATH = 'C:/ffmpeg/bin'
DEFAULT_DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Music")
SUPPORTED_FORMATS = {"mp3", "wav", "aac", "m4a", "flac", "opus", "vorbis"}
QUALITY_MAP = {
    "mp3":     ["64", "128", "192", "256", "320"],
    "m4a":     ["64", "128", "192", "256", "320"],
    "aac":     ["64", "128", "192"],
    "flac":    [],
    "wav":     [],
    "opus":    ["64", "128", "160", "192"],
    "vorbis":  ["64", "128", "192", "256"]
}
