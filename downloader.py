import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import time
import csv
import yt_dlp
import instaloader

def ensure_dirs():
    os.makedirs("downloads/youtube", exist_ok=True)
    os.makedirs("downloads/instagram", exist_ok=True)
    os.makedirs("downloads/audio", exist_ok=True)

def log_download(platform, url, path, status):
    with open("downloads_log.csv", "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([platform, url, time.strftime("%Y-%m-%d %H:%M:%S"), path, status])

def progress_hook(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes", 1)
        downloaded = d.get("downloaded_bytes", 0)
        percent = int(downloaded / total * 100)
        progress_bar["value"] = percent
        status_var.set(f"Downloading... {percent}%")
        root.update_idletasks()
    elif d["status"] == "finished":
        status_var.set("Processing...")


def download_youtube(url, audio_only=False):
    status_var.set("Starting download...")
    ensure_dirs()

    out_dir = "downloads/audio" if audio_only else "downloads/youtube"
    ydl_opts = {
        "outtmpl": os.path.join(out_dir, "%(title)s.%(ext)s"),
        "quiet": True,
        "progress_hooks": [progress_hook],
        "format": "bestaudio/best" if audio_only else "bestvideo+bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }] if audio_only else []
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_var.set("Download completed successfully!")
        log_download("YouTube", url, out_dir, "Success")
    except Exception as e:
        status_var.set(f"Error: {e}")
        log_download("YouTube", url, out_dir, f"Error: {e}")


def download_instagram(url):
    status_var.set("Starting Instagram download...")
    ensure_dirs()
    try:
        L = instaloader.Instaloader(dirname_pattern="downloads/instagram")
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target="downloads/instagram")
        status_var.set("✅ Instagram post downloaded successfully!")
        log_download("Instagram", url, "downloads/instagram", "Success")
    except Exception as e:
        status_var.set(f"Error: {e}")
        log_download("Instagram", url, "downloads/instagram", f"Error: {e}")


def threaded_download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Missing URL", "Please enter a valid URL.")
        return

    t = threading.Thread(target=run_download, args=(url,))
    t.start()


def run_download(url):
    platform = platform_var.get()
    audio_only = (platform == "YouTube (Audio)")
    progress_bar["value"] = 0
    status_var.set("Starting download...")

    if "instagram.com" in url:
        download_instagram(url)
    elif "youtube.com" in url or "youtu.be" in url:
        download_youtube(url, audio_only=audio_only)
    else:
        status_var.set("Unsupported platform URL detected!")


root = tk.Tk()
root.title("AI Social Media Downloader")
root.geometry("550x320")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TCombobox", font=("Segoe UI", 10))
style.configure("TProgressbar", thickness=20)

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(main_frame, text="Enter Video/Post URL:").grid(row=0, column=0, sticky="W")
url_entry = ttk.Entry(main_frame, width=60)
url_entry.grid(row=1, column=0, columnspan=2, pady=5)

ttk.Label(main_frame, text="Select Platform:").grid(row=2, column=0, sticky="W", pady=5)
platform_var = tk.StringVar(value="YouTube (Video)")
platform_box = ttk.Combobox(main_frame, textvariable=platform_var, width=30,
                            values=["YouTube (Video)", "YouTube (Audio)", "Instagram"])
platform_box.grid(row=2, column=1, sticky="EW")

download_button = ttk.Button(main_frame, text="Download", command=threaded_download)
download_button.grid(row=3, column=0, columnspan=2, pady=15)

ttk.Label(main_frame, text="Progress:").grid(row=4, column=0, sticky="W")
progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=5, column=0, columnspan=2, pady=5)

status_var = tk.StringVar(value="Ready")
status_label = ttk.Label(main_frame, textvariable=status_var, foreground="blue")
status_label.grid(row=6, column=0, columnspan=2, pady=10)

def browse_folder():
    folder = filedialog.askdirectory(title="Choose download folder")
    if folder:
        os.chdir(folder)
        status_var.set(f"Download directory changed to: {folder}")

ttk.Button(main_frame, text="Change Save Location", command=browse_folder).grid(row=7, column=0, columnspan=2, pady=5)

root.mainloop()
