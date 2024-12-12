import tkinter as tk
from yt_dlp import YoutubeDL
import requests
from io import BytesIO
from PIL import Image, ImageTk

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
            title_label.config(text=f"Title: {title}")

            # fetch and display thumbnail
            response = requests.get(thumbnail_url)
            thumbnail_data = BytesIO(response.content)
            thumbnail_img = Image.open(thumbnail_data)
            thumbnail_img = thumbnail_img.resize((200,150), Image.Resampling.LANCZOS)
            thumbnail = ImageTk.PhotoImage(thumbnail_img)
            thumbnail_label.config(image=thumbnail)
            thumbnail_label.image = thumbnail
    except Exception as e:
        title_label.config(text="Error: Could not fetch video details")
        print(f"Error: {e}")

# Main window
root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("500x500") # window size

# Welcome labels
label = tk.Label(root, text="Welcome to Youtube Downloader!")
label.pack(pady=20)

# URL
url_label = tk.Label(root, text="Enter Youtube URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Fetch button
fetch_button = tk.Button(root, text="Fetch Details", command=fetch_video_details)
fetch_button.pack(pady=10)

# Title Label
title_label = tk.Label(root, text="Title: Not fetched yet")
title_label.pack(pady=10)

# Thumbnail Label
thumbnail_label = tk.Label(root)
thumbnail_label.pack(pady=10)

# Exit button
exit_button = tk.Button(root, text="Exit", command=on_exit)
exit_button.pack(pady=10)

# Run
root.mainloop()