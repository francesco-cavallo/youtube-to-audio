import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import DEFAULT_DOWNLOAD_FOLDER, SUPPORTED_FORMATS
from downloader import download_audio
import threading
import os

FONT_REGULAR = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_ITALIC = ("Segoe UI", 10, "italic")

class YouTubeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to Audio")
        self.root.geometry("600x560")

        self.theme = "dark"
        self.selected_folder = DEFAULT_DOWNLOAD_FOLDER
        self.current_title = tk.StringVar(value="Nessun download in corso")
        self.status_message = tk.StringVar()

        self.styles = {}
        self.build_ui()
        self.setup_styles()
        self.youtube_url_entry.focus()

    def build_ui(self):
        self.container = tk.Frame(self.root)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=2)
        self.container.grid_columnconfigure(2, weight=1)
        self.container.pack(pady=15, padx=15, fill="both", expand=True)

        self.theme_button = tk.Button(self.container, text="🌓 Cambia Tema", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        self.url_label = tk.Label(self.container, text="🎵 URL del video YouTube:")
        self.url_label.grid(row=1, column=0, columnspan=3, sticky="n", pady=(10, 2))

        self.youtube_url_entry = tk.Entry(self.container, width=50)
        self.youtube_url_entry.grid(row=2, column=0, columnspan=3, sticky="we", padx=5, pady=5)

        self.format_label = tk.Label(self.container, text="🎧 Formato audio:")
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
        self.log_area.grid(row=7, column=0, columnspan=3, padx=5, pady=10)
        self.log_area.config(state=tk.DISABLED)

        self.folder_label = tk.Label(self.container, text=f"📁 Cartella: {self.selected_folder}")
        self.folder_label.grid(row=8, column=0, columnspan=3, sticky="w", padx=5, pady=(5, 0))

        self.choose_button = tk.Button(self.container, text="Scegli cartella di destinazione", command=self.select_folder)
        self.choose_button.grid(row=9, column=0, padx=5, pady=(10, 5), sticky="we")

        self.download_button = tk.Button(self.container, text="⬇️ Scarica Audio", command=self.threaded_download)
        self.download_button.grid(row=9, column=1, padx=5, pady=(10, 5), sticky="we")

        self.open_folder_button = tk.Button(self.container, text="📂 Apri cartella", command=self.open_folder)
        self.open_folder_button.grid(row=9, column=2, padx=5, pady=(10, 5), sticky="we")

        self.status_label = tk.Label(self.container, textvariable=self.status_message, font=FONT_ITALIC)
        self.status_label.grid(row=10, column=0, columnspan=3, pady=(5, 0))

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
        theme = self.styles[self.theme]

        # Applica tema alle combobox
        style.configure("TCombobox",
            fieldbackground=theme["entry_bg"],
            background=theme["entry_bg"],
            foreground=theme["fg"]
        )

        self.apply_theme()

    def apply_theme(self):
        theme = self.styles[self.theme]
        self.root.configure(bg=theme["bg"])
        self.container.configure(bg=theme["bg"])

        for widget in self.container.winfo_children():
            # Per sicurezza controlla se il widget supporta la configurazione di bg e fg
            try:
                # Se il widget supporta 'bg' e 'fg', applica
                if 'bg' in widget.keys() and 'fg' in widget.keys():
                    if isinstance(widget, tk.Label):
                        widget.configure(bg=theme["bg"], fg=theme["fg"])
                    elif isinstance(widget, tk.Button):
                        widget.configure(bg=theme["btn_bg"], fg=theme["btn_fg"],
                                        activebackground=theme["btn_active_bg"], relief=tk.FLAT, bd=0)
                    elif isinstance(widget, tk.Entry):
                        widget.configure(bg=theme["entry_bg"], fg=theme["fg"],
                                        insertbackground=theme["fg"], relief=tk.FLAT)
                    elif isinstance(widget, tk.Text):
                        widget.configure(bg=theme["entry_bg"], fg=theme["log_fg"],
                                        insertbackground=theme["log_fg"])
                    else:
                        # Se widget ha bg e fg ma non è uno dei tipi sopra, prova a settarli
                        widget.configure(bg=theme["bg"], fg=theme["fg"])
                else:
                    # Non ha bg/fg, probabilmente ttk o altro, skip
                    pass
            except tk.TclError as e:
                print(f"Errore di configurazione widget {widget} tipo {type(widget)}: {e}")
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.TCombobox",
            fieldbackground=theme["entry_bg"],
            background=theme["entry_bg"],
            foreground=theme["fg"]
        )
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

    def set_buttons(self, enabled):
        state = "normal" if enabled else "disabled"
        color = self.styles[self.theme]["btn_bg"] if enabled else "#5a5a5a"
        text_fg = self.styles[self.theme]["btn_fg"] if enabled else self.styles[self.theme]["disabled_fg"]

        # Per la Combobox usa .config(state=state) solo, non bg e fg (perché è ttk)
        for widget in [self.choose_button, self.download_button, self.open_folder_button, self.youtube_url_entry]:
            widget.config(state=state)
        self.format_dropdown.config(state=state)

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
                self.animate_completion()
        self.root.after(0, update)

    def animate_completion(self):
        original_color = self.download_button.cget("bg")
        self.download_button.config(bg="#28a745")  # verde
        self.root.after(500, lambda: self.download_button.config(bg=original_color))

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
