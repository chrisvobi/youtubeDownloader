import tkinter as tk
from yt_dlp import YoutubeDL
import requests
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import filedialog, ttk, messagebox

def on_exit():
    root.destroy()

def fetch_video_details():
    global playlist
    url = url_entry.get()
    reset_ui()
    url_entry.insert(0, url)
    try:
        ydl_opts = {'quiet': True, 'extract_flat': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info: # playlist
                video_titles = [entry['title'] for entry in info['entries']]
                global playlist_urls
                playlist_urls = [entry['url'] for entry in info['entries']]
                playlist = True
                title = info.get('title', 'Unknow Title')
                show_playlist_titles(video_titles)
            else: # single video
                title = info.get('title', 'Unknown Title')
                thumbnail_url = info.get('thumbnail', None)
                display_single_video(thumbnail_url)
                playlist = False
        
        save_button.config(state="normal")
        title_label.config(text=title)

    except Exception as e:
        title_label.config(text="Error: Could not fetch video details")
        print(f"Error: {e}")

def display_single_video(thumbnail_url):
    if thumbnail_url:
        response = requests.get(thumbnail_url, stream=True)
        thumbnail_data = BytesIO(response.content)
        thumbnail_img = Image.open(thumbnail_data)
        thumbnail_img = thumbnail_img.resize((200,150), Image.Resampling.LANCZOS)
        thumbnail = ImageTk.PhotoImage(thumbnail_img)
        thumbnail_label.config(image=thumbnail)
        thumbnail_label.image = thumbnail

def show_playlist_titles(video_titles):
    listbox_frame.pack(pady=5)
    playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    playlist_listbox.delete(0, tk.END)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    selection_frame.pack(pady=5)
    select_all_button.pack(side="left",padx=5)
    unselect_all_button.pack(side="left",padx=5)
    for title in video_titles:
        playlist_listbox.insert(tk.END, title)

def choose_save_location():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        save_location_label.config(text=f"Save location: {folder_selected}")
        download_button.config(state="normal")  # Enable download button after selecting the location

def update_progress(d):
    if d['status'] == 'downloading':
        if d.get('downloaded_bytes') and d.get('total_bytes'):
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            progress_var.set(percent)
            progress_label.config(text=f"Progress: {int(percent)}%")

def download_video(save_location):
    format_choice = format_choice_var.get()
    ydl_opts = {
        'outtmpl': f'{save_location}/%(title)s.%(ext)s',
        'progress_hooks': [update_progress],
    }
    if format_choice == 'Video':
        ydl_opts['format'] = 'best'
    else:
        ydl_opts['format'] = 'bestaudio'
    
    if playlist:
        selected_indices = playlist_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one video to download.")
            return
        selected_urls = [playlist_urls[i] for i in selected_indices]
    else:
        url = url_entry.get()
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            if playlist:
                ydl.download(selected_urls)
            else:
                ydl.download([url])
            messagebox.showinfo("Download Complete","The download has completed successfully.")
    except Exception as e:
        messagebox.showerror("Download Failed", f"An error occurred during the download: {e}")

def reset_ui():
    title_label.config(text="Not fetched yet")
    save_location_label.config(text="Save Location: Not selected yet")
    url_entry.delete(0, tk.END)
    progress_var.set(0)
    progress_label.config(text="Progress: 0%")
    thumbnail_label.config(image="")
    thumbnail_label.image = None
    download_button.config(state="disabled")
    save_button.config(state="disabled")
    playlist_listbox.delete(0, tk.END)
    playlist_listbox.pack_forget()
    select_all_button.pack_forget()
    unselect_all_button.pack_forget()
    selection_frame.pack_forget()
    listbox_frame.pack_forget()

def select_all_videos():
    playlist_listbox.select_set(0, tk.END)
    playlist_listbox.focus_set()
    playlist_listbox.activate(0)

def unselect_all_videos():
    playlist_listbox.select_clear(0, tk.END)
    playlist_listbox.selection_clear(0, tk.END)
    playlist_listbox.activate(-1)


# Main window
root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("750x850") # window size
root.resizable(False,False)
root.iconphoto(False, tk.PhotoImage(file="icon.png"))

# Header
header = tk.Label(root, text="Youtube Video Downloader", font=("Arial", 18, "bold"), fg="blue")
header.pack(pady=15)

# URL - Fetch
url_frame = tk.Frame(root)
url_frame.pack(pady=10)
tk.Label(url_frame, text="Enter Youtube URL:", font=("Arial", 12)).pack(side="left", padx=5)
url_entry = tk.Entry(url_frame, width=50, font=("Arial", 12))
url_entry.pack(side="left", padx=5)
tk.Button(url_frame, text="Fetch Details", command=fetch_video_details, font=("Arial", 12)).pack(side="left", padx=5)

## Video Details
details_frame = tk.Frame(root)
details_frame.pack(pady=10)
# Single Video
title_label = tk.Label(details_frame, text="Not fetched yet", font=("Arial", 12))
title_label.pack(pady=5)
thumbnail_label = tk.Label(details_frame)
thumbnail_label.pack(pady=5)
# Playlist
listbox_frame = tk.Frame(details_frame)
listbox_frame.pack_forget()
playlist_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, width=50, height=15)
playlist_listbox.pack_forget()
scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
scrollbar.pack_forget()
playlist_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=playlist_listbox.yview)
selection_frame = tk.Frame(details_frame)
selection_frame.pack_forget()
select_all_button = tk.Button(selection_frame, text="Select All", command=select_all_videos, font=("Arial", 12))
select_all_button.pack_forget()
unselect_all_button = tk.Button(selection_frame, text="Unselect All", command=unselect_all_videos, font=("Arial", 12))
unselect_all_button.pack_forget()

# Select Format
format_frame = tk.Frame(root)
format_frame.pack(pady=10)
tk.Label(format_frame, text="Choose format:", font=("Arial", 12)).pack(side="left",padx=5)
format_choice_var = tk.StringVar(value = "Video")
format_choice_menu = tk.OptionMenu(format_frame, format_choice_var, "Video", "Audio")
format_choice_menu.pack(side="left",padx=5)

# Save Section
save_button = tk.Button(root, text="Choose Save Location", state="disabled", command=choose_save_location, font=("Arial", 12))
save_button.pack(pady=10)
save_location_label = tk.Label(root, text = "Save Location: Not selected yet", font=("Arial", 12))
save_location_label.pack(pady=5)

# Download Button
download_button = tk.Button(root, text="Download", state="disabled", command=lambda: download_video(save_location_label.cget("text").split(": ")[-1]), font=("Arial", 12))
download_button.pack(pady=10)

# Progress Section
progress_label = tk.Label(root, text="Progress: 0%", font=("Arial", 12))
progress_label.pack(pady=5)
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=500)
progress_bar.pack(pady=5)

# Reset and Exit Button
action_frame = tk.Frame(root)
action_frame.pack(pady=20)
exit_button = tk.Button(root, text="Exit", command=on_exit, font=("Arial", 12))
exit_button.pack(side="left", padx=20)
reset_button = tk.Button(root, text="Reset", command=reset_ui, font=("Arial", 12))
reset_button.pack(side="left", padx=20)

# Run
root.mainloop()