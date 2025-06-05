from moviepy import AudioFileClip
import os
import yt_dlp
import threading

def threaded_download():
    threading.Thread(target=start_download).start()

supported_formats = {"mp3", "wav", "aac", "m4a", "flac", "opus", "vorbis"}

def is_valid_url(url):
    return url.startswith("https://www.youtube.com/") or url.startswith("https://youtu.be/")

### INTERFACCIA GRAFICA ###

def download_audio_from_ui(url, format_audio, output_folder):
    if not url or not is_valid_url(url):
        return "URL non valido o mancante."

    if not format_audio or format_audio not in supported_formats:
        return f"Formato non supportato. Formati disponibili: {', '.join(supported_formats)}"

    music_folder = os.path.join(os.path.expanduser("~"), "Music")

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': 'C:/ffmpeg/bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_audio,
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # ← QUI
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"✅ File scaricato correttamente in: {music_folder}"
    except Exception as e:
        log_message(f"Errore: {e}")
        return f"❌ Errore: {e}"

def set_buttons_state(state):
    if state == "disabled":
        choose_folder_button.config(state="disabled", bg="#5a5a5a", fg="#cccccc", activebackground="#5a5a5a")
        download_button.config(state="disabled", bg="#5a5a5a", fg="#cccccc", activebackground="#5a5a5a")
    else:
        choose_folder_button.config(state="normal", bg="#0078D7", fg="#ffffff", activebackground="#005999")
        download_button.config(state="normal", bg="#0078D7", fg="#ffffff", activebackground="#005999")

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# --- UI ---
root = tk.Tk()
root.title("YouTube to Audio")
root.configure(bg="#1e1e1e")  # Sfondo scuro
root.geometry("500x500")

label_style = {"bg": "#1e1e1e", "fg": "#ffffff", "font": ("Segoe UI", 10)}
entry_style = {"bg": "#2e2e2e", "fg": "#ffffff", "insertbackground": "#ffffff", "relief": tk.FLAT}
button_style = {"bg": "#0078D7", "fg": "#ffffff", "activebackground": "#005999"}
current_title = tk.StringVar(value="Nessun download in corso")

tk.Label(root, text="URL del video YouTube:", **label_style).pack(pady=5)
url_entry = tk.Entry(root, width=50, **entry_style)
url_entry.pack(pady=5)

tk.Label(root, text="Formato audio:", **label_style).pack(pady=5)
format_var = tk.StringVar()
format_dropdown = ttk.Combobox(root, textvariable=format_var, values=sorted(supported_formats))
format_dropdown.current(0)
format_dropdown.pack(pady=5)

tk.Label(root, textvariable=current_title, **label_style, wraplength=350, justify="center").pack(pady=5)

# Stile Combobox dark
style = ttk.Style()
style.theme_use('default')
style.configure("TCombobox", fieldbackground="#2e2e2e", background="#2e2e2e", foreground="#ffffff")

# Barra di progresso
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

log_area = tk.Text(root, height=10, width=100, bg="#1e1e1e", fg="#dcdcdc", insertbackground="#dcdcdc")
log_area.pack(pady=10)
log_area.config(state=tk.DISABLED)

music_folder = os.path.join(os.path.expanduser("~"), "Music")
selected_folder = tk.StringVar(value=music_folder)

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        selected_folder.set(folder_selected)
        folder_label.config(text=f"Cartella: {folder_selected}")

folder_label = tk.Label(root, text=f"Cartella: {selected_folder.get()}", **label_style)
folder_label.pack(pady=(0, 5))
choose_folder_button = tk.Button(root, text="Scegli cartella di destinazione", command=select_folder, **button_style)
choose_folder_button.pack()

download_button = tk.Button(root, text="Scarica Audio", command=threaded_download, **button_style)
download_button.pack(pady=10)

def update_progress(percent_str):
    try:
        percent_float = float(percent_str.strip('%'))
        progress["value"] = percent_float
        root.update_idletasks()
    except:
        pass

def progress_hook(d):
    def update_ui():
        if d['status'] == 'downloading':
            title = d.get('info_dict', {}).get('title', 'Scaricamento in corso...')
            current_title.set(title)

            percent = d.get('_percent_str', '').strip()
            downloaded = d.get('_downloaded_bytes_str', '')
            total = d.get('_total_bytes_str', d.get('_total_bytes_estimate_str', ''))
            speed = d.get('_speed_str', '')
            eta = d.get('_eta_str', '')
            update_progress(percent)

            log_message(f"{percent} ({downloaded} di {total}) - Velocità: {speed} - ETA: {eta}")

        elif d['status'] == 'finished':
            current_title.set("Estrazione audio in corso...")
            log_message("✅ Download completato. Estrazione audio in corso...")

    root.after(0, update_ui)

def start_download():
    set_buttons_state("disabled")  # Disabilita bottoni

    url = url_entry.get().strip()
    format_audio = format_var.get().strip().lower()

    # Reset
    progress["value"] = 0
    current_title.set("Inizio download...")
    root.update_idletasks()

    log_message(f"Inizio download: {url} in formato {format_audio}")

    status = download_audio_from_ui(url, format_audio, selected_folder.get())

    log_message(status)
    messagebox.showinfo("Stato", status)

    set_buttons_state("normal")  # Riabilita bottoni

def log_message(msg):
    log_area.config(state=tk.NORMAL)
    log_area.insert(tk.END, msg + '\n')
    log_area.see(tk.END)
    log_area.config(state=tk.DISABLED)

root.mainloop()

#https://www.youtube.com/watch?v=K4DyBUG242c&list=RDQMTgh66LaGkb4&start_radio=1