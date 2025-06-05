# 🎵 YouTube to Audio Converter (GUI)

Un'applicazione Python con interfaccia grafica per convertire facilmente i video YouTube in file audio (mp3, wav, aac, flac, ecc.).

## 🚀 Funzionalità

- Interfaccia moderna con `tkinter`
- Supporto a più formati audio: mp3, wav, aac, m4a, flac, opus, vorbis
- Selezione personalizzata della cartella di destinazione
- Barra di avanzamento e log in tempo reale
- Estrazione audio con `yt-dlp` e `ffmpeg`

## 🧰 Struttura del progetto

youtubeconverter/
├── config.py # Configurazioni base (formati supportati, path ffmpeg)
├── downloader.py # Logica per il download ed estrazione audio
├── gui.py # Interfaccia grafica e interazioni utente
├── main.py # Punto di ingresso dell'applicazione
├── utils.py # Validazioni URL e formati
└── README.md # Questo file

## 🛠 Requisiti

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html) installato e disponibile nel percorso indicato in `config.py`
- Librerie Python:
  - `yt-dlp`
  - `tkinter` (incluso in Python)

### 📦 Installazione dipendenze

```bash
pip install yt-dlp
