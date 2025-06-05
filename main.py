"""
YouTube to Audio Downloader GUI
Usa yt-dlp per scaricare l'audio da un video YouTube nel formato scelto.
"""

from gui import YouTubeConverterApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeConverterApp(root)
    root.mainloop()
