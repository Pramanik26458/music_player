import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from mutagen.mp3 import MP3
import pygame
import os
from PIL import Image, ImageTk 

pygame.mixer.init()

# Global variables
current_position = 0
paused = False
selected_folder_path = ""

def update_progress():
    global current_position
    if pygame.mixer.music.get_busy() and not paused:
        current_position = pygame.mixer.music.get_pos() / 1000
        slider.set(current_position)
      
    window.after(100, update_progress)

def select_music_folder():
    global selected_folder_path
    selected_folder_path = filedialog.askdirectory()
    if selected_folder_path:
        lbox.delete(0, tk.END)
        for filename in os.listdir(selected_folder_path):
            if filename.endswith(".mp3"):
                lbox.insert(tk.END, filename)

def play_selected_song():
    global current_position, paused
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        selected_song = lbox.get(current_index)
        full_path = os.path.join(selected_folder_path, selected_song)
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play()
        paused = False
        audio = MP3(full_path)
        song_duration = audio.info.length
        slider.config(to=song_duration)
        slider.set(current_position)  

def previous_song():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index > 0:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(current_index - 1)
            play_selected_song()

def next_song():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index < lbox.size() - 1:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(current_index + 1)
            play_selected_song()

def play_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        play_selected_song()

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def stop_music():
    global paused, current_position
    pygame.mixer.music.stop()
    paused = False
    current_position = 0
    slider.set(0)
    lbl_current_time.config(text="00:00")

def slide(val):
    global current_position
    current_position = float(val)
    pygame.mixer.music.play(start=current_position)

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

#  the main window
window = ctk.CTk()
window.title("Music Player App")
window.geometry("600x500")
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)

# images using Pillow for better format support
img_left = Image.open("music.png").resize((2000, 500))  # Adjust size as needed
photo_left = ImageTk.PhotoImage(img_left)
lab_left = tk.Label(window, image=photo_left)
lab_left.image = photo_left  # Keep a reference to prevent garbage collection
lab_left.place(x=10, y=8) 



#label for the music player title
l_music_player = ctk.CTkLabel(window, text="Music Player", font=("TkDefaultFont", 30, "bold"))
l_music_player.grid(row=0, column=0, pady=10)

# button to select the music folder
btn_select_folder = ctk.CTkButton(window, text="Select Music Folder",
                                  command=select_music_folder,
                                  font=("TkDefaultFont", 18))
btn_select_folder.grid(row=11, column=0, pady=10)

# listbox to display the available songs
lbox = tk.Listbox(window, width=20, font=("TkDefaultFont", 16))
lbox.grid(row=2, column=0, padx=0, pady=10, sticky="nsew")


# frame to hold the control buttons
btn_frame = ctk.CTkFrame(window)
btn_frame.grid(row=3, column=0, pady=20, sticky="ew")

# button icons
icon_previous = ImageTk.PhotoImage(Image.open("previous.png").resize((30, 30)))
icon_next = ImageTk.PhotoImage(Image.open("next.png").resize((30, 30)))
icon_play = ImageTk.PhotoImage(Image.open("play.png").resize((30, 30)))
icon_pause = ImageTk.PhotoImage(Image.open("pause.png").resize((30, 30)))

# buttons for previous, play, pause, and next
btn_previous = ctk.CTkButton(btn_frame, image=icon_previous, text=" Previous", command=previous_song,
                             width=20, font=("TkDefaultFont", 25), compound=tk.LEFT)
btn_previous.pack(side=tk.LEFT, padx=5)

btn_next = ctk.CTkButton(btn_frame, image=icon_next, text=" Next", command=next_song,
                         width=20, font=("TkDefaultFont", 25), compound=tk.LEFT)
btn_next.pack(side=tk.RIGHT,padx=5)

btn_play = ctk.CTkButton(btn_frame, image=icon_play, text=" Play", command=play_music,
                         width=20, font=("TkDefaultFont", 25), compound=tk.LEFT)
btn_play.pack( padx=5)

btn_pause = ctk.CTkButton(btn_frame, image=icon_pause, text=" Pause", command=pause_music,
                          width=20, font=("TkDefaultFont", 25), compound=tk.LEFT)
btn_pause.pack( padx=5)
 
#frame for time display and slider

time_frame = ctk.CTkFrame(window)
time_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

lbl_current_time = ctk.CTkLabel(time_frame, text="00:00", font=("TkDefaultFont", 12))
lbl_current_time.pack(side=tk.LEFT)

slider = ctk.CTkSlider(window, from_=0, to=100, command=slide)
slider.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

lbl_total_time = ctk.CTkLabel(time_frame, text="00:00", font=("TkDefaultFont", 12))
lbl_total_time.pack(side=tk.RIGHT)


# volume control slider
volume_slider = ctk.CTkSlider(window, from_=0, to=100, command=set_volume)
volume_slider.set(100)
volume_slider.grid(row=6, column=0, padx=20, pady=10, sticky="ew")


update_progress()
window.mainloop()
