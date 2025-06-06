import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import DEFAULT_DOWNLOAD_FOLDER, SUPPORTED_FORMATS
from downloader import download_audio
import threading
import os

class YouTubeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to Audio")
        self.root.geometry("600x560")
        self.root.configure(bg="#121212")

        self.selected_folder = DEFAULT_DOWNLOAD_FOLDER
        self.current_title = tk.StringVar(value="Nessun download in corso")
        self.status_message = tk.StringVar()

        self.build_ui()
        self.setup_styles()
        self.youtube_url_entry.focus()

    def build_ui(self):
        label_style = {"bg": "#121212", "fg": "#ffffff", "font": ("Segoe UI", 10)}
        entry_style = {"bg": "#1e1e1e", "fg": "#ffffff", "insertbackground": "#ffffff", "relief": tk.FLAT}
        button_style = {"bg": "#1f6feb", "fg": "#ffffff", "activebackground": "#1158c7", "relief": tk.FLAT, "bd": 0, "font": ("Segoe UI", 10, "bold")}

        container = tk.Frame(self.root, bg="#121212")
        container.pack(pady=15, padx=15, fill="both", expand=True)

        tk.Label(container, text="🎵 URL del video YouTube:", **label_style).grid(row=0, column=0, sticky="w")
        self.youtube_url_entry = tk.Entry(container, width=50, **entry_style)
        self.youtube_url_entry.grid(row=1, column=0, columnspan=2, pady=5, sticky="we")

        tk.Label(container, text="🎧 Formato audio:", **label_style).grid(row=2, column=0, sticky="w")
        self.format_var = tk.StringVar()
        self.format_dropdown = ttk.Combobox(container, textvariable=self.format_var, values=sorted(SUPPORTED_FORMATS))
        self.format_dropdown.current(0)
        self.format_dropdown.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")

        tk.Label(container, textvariable=self.current_title, **label_style, wraplength=450, justify="center", font=("Segoe UI", 10, "italic")).grid(row=4, column=0, columnspan=2, pady=5)

        self.progress = ttk.Progressbar(container, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=2, pady=10)

        self.log_area = tk.Text(container, height=8, width=65, bg="#1e1e1e", fg="#dcdcdc", insertbackground="#dcdcdc", font=("Consolas", 9))
        self.log_area.grid(row=6, column=0, columnspan=2, pady=10)
        self.log_area.config(state=tk.DISABLED)

        self.folder_label = tk.Label(container, text=f"📁 Cartella: {self.selected_folder}", **label_style)
        self.folder_label.grid(row=7, column=0, columnspan=2, sticky="w")

        self.choose_button = tk.Button(container, text="Scegli cartella di destinazione", command=self.select_folder, **button_style)
        self.choose_button.grid(row=8, column=0, columnspan=2, pady=(5, 5))

        self.download_button = tk.Button(container, text="⬇️ Scarica Audio", command=self.threaded_download, **button_style)
        self.download_button.grid(row=9, column=0, pady=10, sticky="e")

        self.open_folder_button = tk.Button(container, text="📂 Apri cartella", command=self.open_folder, **button_style)
        self.open_folder_button.grid(row=9, column=1, pady=10, sticky="w")

        self.status_label = tk.Label(container, textvariable=self.status_message, **label_style, font=("Segoe UI", 9, "italic"))
        self.status_label.grid(row=10, column=0, columnspan=2, pady=(5, 0))

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox", fieldbackground="#1e1e1e", background="#1e1e1e", foreground="#ffffff")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=f"📁 Cartella: {folder}")

    def open_folder(self):
        try:
            os.startfile(self.selected_folder)
        except Exception as e:
            self.log(f"❌ Impossibile aprire la cartella: {e}")

    def set_buttons(self, enabled):
        state = "normal" if enabled else "disabled"
        color = "#1f6feb" if enabled else "#5a5a5a"
        text_fg = "#ffffff" if enabled else "#cccccc"

        for widget in [self.choose_button, self.download_button, self.open_folder_button, self.format_dropdown, self.youtube_url_entry]:
            widget.config(state=state)
        self.choose_button.config(bg=color, fg=text_fg)
        self.download_button.config(bg=color, fg=text_fg)
        self.open_folder_button.config(bg=color, fg=text_fg)

    def log(self, msg):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, msg + '\n')
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def update_progress(self, percent_str):
        try:
            self.progress["value"] = float(percent_str.strip('%'))
            self.root.update_idletasks()
        except:
            pass

    def hook(self, d):
        def update():
            if d['status'] == 'downloading':
                title = d.get('info_dict', {}).get('title', 'Scaricamento in corso...')
                self.current_title.set(title)
                self.root.title(f"Scaricamento: {title[:50]}")
                self.update_progress(d.get('_percent_str', '0'))
                self.log(f"{d.get('_percent_str', '')} - {d.get('_downloaded_bytes_str', '')} / {d.get('_total_bytes_str', '')}")
            elif d['status'] == 'finished':
                self.current_title.set("Estrazione audio in corso...")
                self.log("✅ Download completato.")
        self.root.after(0, update)

    def threaded_download(self):
        threading.Thread(target=self.start_download).start()

    def start_download(self):
        self.set_buttons(False)
        self.progress["value"] = 0
        self.current_title.set("Inizio download...")
        self.status_message.set("")

        url = self.youtube_url_entry.get().strip()
        format_audio = self.format_var.get().strip().lower()
        self.log(f"Inizio download: {url} in formato {format_audio}")

        status = download_audio(url, format_audio, self.selected_folder, self.hook)
        self.log(status)
        self.status_message.set(status)
        messagebox.showinfo("Stato", status)

        self.set_buttons(True)
        self.root.title("YouTube to Audio")
