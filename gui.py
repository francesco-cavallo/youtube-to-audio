import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import DEFAULT_DOWNLOAD_FOLDER, SUPPORTED_FORMATS
from downloader import download_audio
import threading
import os
from i18n import t

FONT_REGULAR = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_ITALIC = ("Segoe UI", 10, "italic")


class YouTubeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to Audio")
        self.root.geometry("600x560")

        self.theme = "dark"
        self.lang = "it"
        self.selected_folder = DEFAULT_DOWNLOAD_FOLDER
        self.current_title = tk.StringVar(value="Nessun download in corso")
        self.status_message = tk.StringVar()

        self.styles = {}
        self._current_placeholder = None
        self.build_ui()
        self.setup_styles()
        self.set_url_placeholder()

    def build_ui(self):
        self.container = tk.Frame(self.root)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=2)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.pack(pady=15, padx=15, fill="both", expand=True)

        self.language_button = tk.Button(self.container, text="🌐 IT / EN", command=self.toggle_language)
        self.language_button.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.theme_button = tk.Button(self.container, command=self.toggle_theme)
        self.theme_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        self.url_label = tk.Label(self.container)
        self.url_label.grid(row=1, column=0, columnspan=3, sticky="n", pady=(10, 2))

        self.youtube_url_entry = tk.Entry(self.container, width=50)
        self.youtube_url_entry.grid(row=2, column=0, columnspan=3, sticky="we", padx=5, pady=5)
        self.youtube_url_entry.bind("<FocusIn>", self.clear_url_placeholder)
        self.youtube_url_entry.bind("<FocusOut>", self.restore_url_placeholder)

        self.format_label = tk.Label(self.container)
        self.format_label.grid(row=3, column=0, columnspan=3, sticky="n", pady=(10, 2))

        self.format_var = tk.StringVar()
        self.format_dropdown = ttk.Combobox(self.container, textvariable=self.format_var, values=sorted(SUPPORTED_FORMATS))
        self.format_dropdown.current(0)
        self.format_dropdown.grid(row=4, column=0, columnspan=3, sticky="we", padx=5, pady=5)

        self.title_label = tk.Label(self.container, textvariable=self.current_title, wraplength=450, justify="center", font=FONT_ITALIC)
        self.title_label.grid(row=5, column=0, columnspan=3, pady=5)

        self.progress = ttk.Progressbar(self.container, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

        self.log_area = tk.Text(self.container, height=8, width=65, font=("Consolas", 9))
        self.log_area.grid(row=7, column=0, columnspan=3, padx=5, pady=(5, 0))
        self.log_area.config(state=tk.DISABLED)

        self.clear_log_btn = tk.Button(self.container, command=self.clear_log)
        self.clear_log_btn.grid(row=8, column=0, columnspan=3, pady=(2, 5), sticky="n")

        self.folder_label = tk.Label(self.container)
        self.folder_label.grid(row=9, column=0, columnspan=3, sticky="w", padx=5, pady=(5, 0))

        self.choose_button = tk.Button(self.container, command=self.select_folder)
        self.choose_button.grid(row=10, column=0, padx=5, pady=(10, 5), sticky="we")

        self.download_button = tk.Button(self.container, command=self.threaded_download)
        self.download_button.grid(row=10, column=1, padx=5, pady=(10, 5), sticky="we")

        self.open_folder_button = tk.Button(self.container, command=self.open_folder)
        self.open_folder_button.grid(row=10, column=2, padx=5, pady=(10, 5), sticky="we")

        self.status_label = tk.Label(self.container, textvariable=self.status_message, font=FONT_ITALIC)
        self.status_label.grid(row=11, column=0, columnspan=3, pady=(5, 0))

        self.refresh_ui()
        self.set_url_placeholder()

    def setup_styles(self):
        self.styles = {
            "dark": {
                "bg": "#121212", "fg": "#ffffff", "entry_bg": "#1e1e1e", "btn_bg": "#1f6feb", "btn_fg": "#ffffff",
                "btn_active_bg": "#1158c7", "log_fg": "#dcdcdc", "disabled_fg": "#cccccc"
            },
            "light": {
                "bg": "#f0f0f0", "fg": "#000000", "entry_bg": "#ffffff", "btn_bg": "#1f6feb", "btn_fg": "#ffffff",
                "btn_active_bg": "#1158c7", "log_fg": "#333333", "disabled_fg": "#666666"
            }
        }

        style = ttk.Style()
        style.theme_use('default')
        self.apply_theme()

    def apply_theme(self):
        theme = self.styles[self.theme]
        self.root.configure(bg=theme["bg"])
        self.container.configure(bg=theme["bg"])

        for widget in self.container.winfo_children():
            try:
                if 'bg' in widget.keys() and 'fg' in widget.keys():
                    if isinstance(widget, tk.Label):
                        widget.configure(bg=theme["bg"], fg=theme["fg"])
                    elif isinstance(widget, tk.Button):
                        widget.configure(bg=theme["btn_bg"], fg=theme["btn_fg"],
                                         activebackground=theme["btn_active_bg"], relief=tk.FLAT, bd=0)
                    elif isinstance(widget, tk.Entry):
                        widget.configure(bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"], relief=tk.FLAT)
                    elif isinstance(widget, tk.Text):
                        widget.configure(bg=theme["entry_bg"], fg=theme["log_fg"], insertbackground=theme["log_fg"])
            except tk.TclError as e:
                print(f"Errore configurazione widget: {e}")

        style = ttk.Style()
        style.configure("Custom.TCombobox",
                        fieldbackground=theme["entry_bg"],
                        background=theme["entry_bg"],
                        foreground=theme["fg"])
        self.format_dropdown.configure(style="Custom.TCombobox")

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()

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

    def clear_log(self):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)

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
                self.animate_completion()
        self.root.after(0, update)

    def animate_completion(self):
        original_color = self.download_button.cget("bg")
        self.download_button.config(bg="#28a745")
        self.root.after(500, lambda: self.download_button.config(bg=original_color))

    def threaded_download(self):
        self.update_ui_for_download(starting=True)
        thread = threading.Thread(target=self.safe_download_audio)
        thread.start()

    def safe_download_audio(self):
        try:
            self.start_download()
        except Exception as e:
            self.log(f"❌ Errore inaspettato: {e}")
            self.set_status("Errore inaspettato durante il download.", success=False)
            self.set_buttons(True)

    def start_download(self):
        self.set_buttons(False)
        self.progress["value"] = 0
        self.current_title.set("Inizio download...")

        url = self.youtube_url_entry.get().strip()
        if url == t("url_placeholder", self.lang) or url == "":
            self.set_status("Inserisci un URL valido.", success=False)
            self.set_buttons(True)
            return

        format_audio = self.format_var.get().strip().lower()

        self.youtube_url_entry.config(highlightthickness=0)

        self.log(f"Inizio download: {url} in formato {format_audio}")
        success, message = download_audio(url, format_audio, self.selected_folder, self.hook)
        self.log(message)

        self.set_status(message, success=success)
        self.set_buttons(True)
        self.root.title("YouTube to Audio")

    def set_buttons(self, enabled):
        state = "normal" if enabled else "disabled"
        for widget in [self.choose_button, self.download_button, self.open_folder_button, self.youtube_url_entry]:
            widget.config(state=state)
        self.format_dropdown.config(state=state)

    def set_status(self, message, success=True):
        self.status_message.set(message)
        color = "#28a745" if success else "#e63946"
        self.status_label.config(fg=color)

    def update_ui_for_download(self, starting: bool):
        if starting:
            self.set_status("⏳ Scaricamento in corso...", success=True)
            self.set_buttons(False)
            self.theme_button.config(state=tk.DISABLED)
        else:
            self.set_status("✅ Download completato", success=True)
            self.set_buttons(True)
            self.theme_button.config(state=tk.NORMAL)

    def set_url_placeholder(self):
        placeholder = t("url_placeholder", self.lang)
        current_text = self.youtube_url_entry.get()
        if current_text == "" or current_text == self._current_placeholder:
            self.youtube_url_entry.delete(0, tk.END)
            self.youtube_url_entry.insert(0, placeholder)
            self.youtube_url_entry.config(fg="#888")
            self._current_placeholder = placeholder
        else:
            self._current_placeholder = None

    def clear_url_placeholder(self, event):
        placeholder = t("url_placeholder", self.lang)
        current_text = self.youtube_url_entry.get()
        if current_text == placeholder:
            self.youtube_url_entry.delete(0, tk.END)
            self.youtube_url_entry.config(fg=self.styles[self.theme]["fg"])
            self._current_placeholder = None

    def restore_url_placeholder(self, event):
        current_text = self.youtube_url_entry.get()
        if current_text == "":
            self.set_url_placeholder()


    def toggle_language(self):
        self.lang = "en" if self.lang == "it" else "it"
        self.refresh_ui()
        self.set_url_placeholder()
        self.root.focus()

    def refresh_ui(self):
        self.root.title(t("title", self.lang))
        self.theme_button.config(text=t("change_theme", self.lang))
        self.url_label.config(text=t("video_url", self.lang))
        self.format_label.config(text=t("audio_format", self.lang))
        self.choose_button.config(text=t("select_folder", self.lang))
        self.download_button.config(text=t("download_audio", self.lang))
        self.open_folder_button.config(text=t("open_folder", self.lang))
        self.folder_label.config(text=f"{t('folder_label', self.lang)} {self.selected_folder}")
        self.current_title.set(t("no_download", self.lang))
        self.clear_log_btn.config(text=t("clear_log", self.lang))