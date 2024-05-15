from pytube import YouTube
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import threading
import os, sys
from PIL import Image, ImageTk

# Methods
def download_video(url):
    try:
        yt = YouTube(url, on_progress_callback=on_progress, on_complete_callback=on_complete_video)
        video = yt.streams.get_highest_resolution()
        progress_frame.pack()
        link_input.configure(state="disabled")
        download_video_button.configure(state="disabled", fg_color="#242424")
        download_audio_button.configure(state="disabled", fg_color="#242424")
        download_thread = threading.Thread(target=lambda: video.download(download_path.get()))
        download_thread.start()
        link.set("")
    except:
        if(yt.age_restricted):
            messagebox.showerror("Age restriction", "The video has age restriction")
        else:
            messagebox.showerror("Invalid link", "Provide a valid YouTube video link")

def download_audio(url):
    try:
        yt = YouTube(url, on_progress_callback=on_progress, on_complete_callback=on_complete_audio)
        video = yt.streams.filter(only_audio=True).first()
        progress_frame.pack()
        link_input.configure(state="disabled")
        download_audio_button.configure(state="disabled", fg_color="#242424")
        download_video_button.configure(state="disabled", fg_color="#242424")
        
        # Download in mp3 format
        def download_in_thread():
            # Download in mp3 format
            out_file = video.download(download_path.get())
            base, ext = os.path.splitext(out_file) 
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

        # Start a new thread for downloading
        download_thread = threading.Thread(target=download_in_thread)
        download_thread.start()
        link.set("")
    except:
        if(yt.age_restricted):
            messagebox.showerror("Age restriction", "The video has age restriction")
        else:
            messagebox.showerror("Invalid link", "Provide a valid YouTube video link")

def getTitle(url):
    try:
        yt = YouTube(url)
        title.set(yt.title)
        download_video_button.configure(state="normal", fg_color="#FF0000")
        download_audio_button.configure(state="normal", fg_color="#FF0000")
    except:
        if(len(link_input.get()) != 0):
            title.set("Invalid link")
            download_video_button.configure(state="disabled", fg_color="#242424")
            download_audio_button.configure(state="disabled", fg_color="#242424")
            progress_frame.pack_forget()
        else: 
            title.set("")
            download_video_button.configure(state="disabled", fg_color="#242424")
            download_audio_button.configure(state="disabled", fg_color="#242424")
            progress_frame.pack_forget()

def update_title(event):
    getTitle(link_input.get())

def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size
    progress.set(round(pct_completed, 2))
    progress_perc.set(f"{round(pct_completed * 100, 2)}%")

def on_complete_video(p1, p2):
    link_input.configure(state="normal")
    download_video_button.configure(state="normal", fg_color="#FF0000")
    download_audio_button.configure(state="normal", fg_color="#FF0000")

def on_complete_audio(p1, p2):
    link_input.configure(state="normal")
    download_audio_button.configure(state="normal", fg_color="#FF0000")
    download_video_button.configure(state="normal", fg_color="#FF0000")

def CenterWindowToDisplay(Screen: ctk.CTk, width: int, height: int):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/1.5))
    return f"{width}x{height}+{x}+{y}"

def choose_directory():
    try:
        directory_path = filedialog.askdirectory(title="Select a path to save the downloaded content")
        if directory_path:
            download_path.set(directory_path+"/ytdownloads")
        else:
            download_path.set("")
    except:
        download_path.set("")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Window configs
window = tk.Tk()
window.title("Youtube Downloader")
window.geometry(CenterWindowToDisplay(window, 400, 250))
window.resizable(False, False)

# Import resources
logo_frame = ttk.Frame(window)
logo_title = ttk.Label(logo_frame, text="YouTube Downloader", font=("Helvetica", 25, "bold"))

try:
    img =  Image.open(resource_path("resources/ytdicon.png"))
    icon = ImageTk.PhotoImage(image=img)
    window.iconphoto(False, icon)

    img = img.resize((45, 45))
    tkimg = ImageTk.PhotoImage(image=img)
    logo = tk.Label(logo_frame, image=tkimg)
    logo.grid(row=0, column=0)
except Exception as e:
    print(e)

logo_title.grid(row=0, column=1)
logo_frame.pack(pady=(10, 5))

# Menubar
menubar = tk.Menu()
window.config(menu=menubar)
edit_menu = tk.Menu(menubar, tearoff=False)
about_menu = tk.Menu(menubar, tearoff=False)
edit_menu.add_command(
    label="Select download directory",
    command=choose_directory
)
about_menu.add_command(
    label="About YouTube Downloader",
    command=lambda: messagebox.showinfo(title="YouTube Downloader", message="YouTube Downloader\n\n2024 © Juan Orts\nhttps://github.com/juanorts\n\nPython 3.12.3")
)
menubar.add_cascade(menu=edit_menu, label="Edit")
menubar.add_cascade(menu=about_menu, label="About")

# Variable
link = tk.StringVar()
title = tk.StringVar()
progress = tk.DoubleVar()
progress_perc = tk.StringVar()
download_path = tk.StringVar()

# Widgets
link_input = ctk.CTkEntry(window, width=300, placeholder_text="Type in a YouTube video URL...")
link_input.pack(pady=(10,20))
link_input.bind("<KeyRelease>", update_title)
download_buttons_frame = ttk.Frame(window)
download_video_button = ctk.CTkButton(download_buttons_frame, text="Download video", command= lambda: download_video(link_input.get()), fg_color="#242424", hover_color="#242424", state="disabled")
download_video_button.grid(row=0, column=0, padx=8)
download_audio_button = ctk.CTkButton(download_buttons_frame, text="Download audio", command= lambda: download_audio(link_input.get()), fg_color="#242424", hover_color="#242424", state="disabled")
download_audio_button.grid(row=0, column=1, padx=8)
download_buttons_frame.pack()
title_label = ttk.Label(window, textvariable=title, font=("Arial", 16), wraplength=300)
title_label.pack(pady=10)
progress_frame = ttk.Frame(window)
progress_bar = ctk.CTkProgressBar(progress_frame, orientation="horizontal", progress_color="#FF0000", mode="determinate", width=250, variable=progress)
progress_label = ctk.CTkLabel(progress_frame, textvariable=progress_perc)
progress_bar.grid(row=0, column=0, padx=(10,0))
progress_label.grid(row=0, column=1, padx=10)


#  Main
choose_directory()
window.mainloop()