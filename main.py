import tkinter as tk
from yt_dlp import YoutubeDL
import requests
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import filedialog

def on_exit():
    root.destroy()

def fetch_video_details():
    url = url_entry.get()
    try:
        with YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown Title')
            thumbnail_url = info.get('thumbnail')

            # update title
            title_label.config(text=f"{title}")

            # fetch and display thumbnail
            response = requests.get(thumbnail_url)
            thumbnail_data = BytesIO(response.content)
            thumbnail_img = Image.open(thumbnail_data)
            thumbnail_img = thumbnail_img.resize((200,150), Image.Resampling.LANCZOS)
            thumbnail = ImageTk.PhotoImage(thumbnail_img)
            thumbnail_label.config(image=thumbnail)
            thumbnail_label.image = thumbnail

            # enable save location button
            save_button.config(state="normal")

    except Exception as e:
        title_label.config(text="Error: Could not fetch video details")
        print(f"Error: {e}")

def choose_save_location():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        save_location_label.config(text=f"Save location: {folder_selected}")
        download_button.config(state="normal")  # Enable download button after selecting the location

def download_video(save_location):
    url = url_entry.get()
    format_choice = format_choice_var.get()

    ydl_opts = {
        'outtmpl': f'{save_location}/%(title)s.%(ext)s',
    }

    if format_choice == 'Video':
        ydl_opts['format'] = 'best'
    else:
        ydl_opts['format'] = 'bestaudio'

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        title_label.config(text="Download Complete!")

# Main window
root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("500x650") # window size

# Welcome labels
label = tk.Label(root, text="YoutubeDownloader by chrisvobi")
label.pack(pady=20)

# URL
url_label = tk.Label(root, text="Enter Youtube URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Fetch button
tk.Button(root, text="Fetch Details", command=fetch_video_details).pack(pady=10)

# Title Label
title_label = tk.Label(root, text="Not fetched yet")
title_label.pack(pady=10)

# Thumbnail Label
thumbnail_label = tk.Label(root)
thumbnail_label.pack(pady=10)

# Select Format
tk.Label(root, text="Choose format:").pack(pady=5)
format_choice_var = tk.StringVar(value = "Video")
format_choice_menu = tk.OptionMenu(root, format_choice_var, "Video", "Audio")
format_choice_menu.pack(pady=5)

# Save Button
save_button = tk.Button(root, text="Choose Save Location", state="disabled", command=choose_save_location)
save_button.pack(pady=10)

# Save Label
save_location_label = tk.Label(root, text = "Save Location: Not selected yet")
save_location_label.pack(pady=10)

# Download Button
download_button = tk.Button(root, text="Download", state="disabled", command=lambda: download_video(save_location_label.cget("text").split(": ")[-1]))
download_button.pack(pady=10)

# Exit button
tk.Button(root, text="Exit", command=on_exit).pack(pady=10)

# Run
root.mainloop()