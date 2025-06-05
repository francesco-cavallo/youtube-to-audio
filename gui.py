import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import DEFAULT_DOWNLOAD_FOLDER, SUPPORTED_FORMATS
from downloader import download_audio
import threading

class YouTubeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to Audio")
        self.root.geometry("500x500")
        self.root.configure(bg="#1e1e1e")

        self.selected_folder = DEFAULT_DOWNLOAD_FOLDER
        self.current_title = tk.StringVar(value="Nessun download in corso")

        self.build_ui()
        self.setup_styles()

    def build_ui(self):
        label_style = {"bg": "#1e1e1e", "fg": "#ffffff", "font": ("Segoe UI", 10)}
        entry_style = {"bg": "#2e2e2e", "fg": "#ffffff", "insertbackground": "#ffffff", "relief": tk.FLAT}
        button_style = {"bg": "#0078D7", "fg": "#ffffff", "activebackground": "#005999"}

        tk.Label(self.root, text="URL del video YouTube:", **label_style).pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=50, **entry_style)
        self.url_entry.pack(pady=5)

        tk.Label(self.root, text="Formato audio:", **label_style).pack(pady=5)
        self.format_var = tk.StringVar()
        self.format_dropdown = ttk.Combobox(self.root, textvariable=self.format_var, values=sorted(SUPPORTED_FORMATS))
        self.format_dropdown.current(0)
        self.format_dropdown.pack(pady=5)

        tk.Label(self.root, textvariable=self.current_title, **label_style, wraplength=350, justify="center").pack(pady=5)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.log_area = tk.Text(self.root, height=10, width=100, bg="#1e1e1e", fg="#dcdcdc", insertbackground="#dcdcdc")
        self.log_area.pack(pady=10)
        self.log_area.config(state=tk.DISABLED)

        self.folder_label = tk.Label(self.root, text=f"Cartella: {self.selected_folder}", **label_style)
        self.folder_label.pack(pady=(0, 5))

        self.choose_button = tk.Button(self.root, text="Scegli cartella di destinazione", command=self.select_folder, **button_style)
        self.choose_button.pack()

        self.download_button = tk.Button(self.root, text="Scarica Audio", command=self.threaded_download, **button_style)
        self.download_button.pack(pady=10)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox", fieldbackground="#2e2e2e", background="#2e2e2e", foreground="#ffffff")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=f"Cartella: {folder}")

    def set_buttons(self, enabled):
        state = "normal" if enabled else "disabled"
        color = "#0078D7" if enabled else "#5a5a5a"
        text_fg = "#ffffff" if enabled else "#cccccc"
        self.choose_button.config(state=state, bg=color, fg=text_fg)
        self.download_button.config(state=state, bg=color, fg=text_fg)

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

        url = self.url_entry.get().strip()
        format_audio = self.format_var.get().strip().lower()
        self.log(f"Inizio download: {url} in formato {format_audio}")

        status = download_audio(url, format_audio, self.selected_folder, self.hook)
        self.log(status)
        messagebox.showinfo("Stato", status)

        self.set_buttons(True)
