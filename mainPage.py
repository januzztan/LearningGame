import tkinter as tk
from tkinter import PhotoImage
import pygame

# Initialize pygame mixer for music and sound effects
pygame.mixer.init()
pygame.mixer.music.set_volume(0.15)  # Music is played at 15%

# Load and play background music as soon as the program starts
pygame.mixer.music.load("Assets/BGM.mp3")  # Ensure the file path is correct
pygame.mixer.music.play(-1)  # Play music in a loop

# Load the mouse click sound
click_sound = pygame.mixer.Sound("Assets/mouse_click.mp3")

# Function to play or stop the music
music_playing = True
def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()
        music_toggle_button.config(image=volume_mute_image)
    else:
        pygame.mixer.music.unpause()
        music_toggle_button.config(image=volume_play_image)
    music_playing = not music_playing

# Function to play the click sound
def play_click_sound():
    click_sound.play()

# Functions to open different pages
def open_game_page():
    play_click_sound()  # Play click sound
    hide_main_page()
    game_page.pack(fill="both", expand=True)

def open_instruction_page():
    play_click_sound()  # Play click sound
    hide_main_page()
    instruction_page.pack(fill="both", expand=True)

def open_high_score_page():
    play_click_sound()  # Play click sound
    hide_main_page()
    high_score_page.pack(fill="both", expand=True)

def hide_main_page():
    button_frame.place_forget()  # Hide the button frame using place_forget
    music_toggle_button.place_forget()  # Hide the music button when navigating to another page
    title_image_label.pack_forget()  # Hide the title image when navigating to another page

def back_to_main_page():
    play_click_sound()  # Play click sound
    global music_playing
    
    # Hide all other pages
    game_page.pack_forget()
    instruction_page.pack_forget()
    high_score_page.pack_forget()
    
    # Repack the main button frame to show the buttons and music button
    title_image_label.pack(pady=100)  # Show the image when returning to the main page
    button_frame.place(relx=0.5, rely=1.0, anchor="s")  # Position at the bottom center
    music_toggle_button.place(relx=0.98, rely=0.02, anchor="ne")  # Position the mute button to the top-right corner
    
    # Ensure the music is playing and the button shows the correct state
    if not music_playing:
        pygame.mixer.music.unpause()
        music_toggle_button.config(image=volume_play_image)
    
    # Reset the music playing state to the same as when the game starts
    music_playing = True

# Main application window
root = tk.Tk()
root.title("Main Page")
root.geometry("1920x1080")
root.resizable(True, True)  # Allow resizing
root.configure(bg="black")  # Set background color to black

# Load the images for the buttons and title image
play_btn_image = PhotoImage(file="Assets/Start_btn.png")
instruction_btn_image = PhotoImage(file="Assets/Instruction_btn.png")  # Load instruction button image
high_score_btn_image = PhotoImage(file="Assets/HighScore_btn.png")     # Load high score button image
volume_play_image = PhotoImage(file="Assets/Volume_play.png")           # Image for volume play
volume_mute_image = PhotoImage(file="Assets/Volume_mute.png")           # Image for volume mute
title_image = PhotoImage(file="Assets/Title.png")                      # Load the title image

# Title image label (centered)
title_image_label = tk.Label(root, image=title_image, bg="black")
title_image_label.pack(pady=150)  # Add padding to position it in the middle

# Music toggle button on the top right corner with image
music_toggle_button = tk.Button(root, image=volume_play_image, command=lambda: [play_click_sound(), toggle_music()], borderwidth=0, bg="black")
music_toggle_button.place(relx=0.98, rely=0.02, anchor="ne")  # Position the button in the top-right corner

# Main frame to hold buttons
button_frame = tk.Frame(root, bg="black")  # Set background color to black
button_frame.place(relx=0.5, rely=1.0, anchor="s")  # Position the frame at the bottom center

# Buttons on the main page inside the frame
game_button = tk.Button(button_frame, image=play_btn_image, command=open_game_page, borderwidth=0, bg="black")
instruction_button = tk.Button(button_frame, image=instruction_btn_image, command=open_instruction_page, borderwidth=0, bg="black")
high_score_button = tk.Button(button_frame, image=high_score_btn_image, command=open_high_score_page, borderwidth=0, bg="black")

# Align the buttons in a row inside the frame
game_button.pack(side=tk.LEFT, padx=40, pady=140)
instruction_button.pack(side=tk.LEFT, padx=40, pady=140)
high_score_button.pack(side=tk.LEFT, padx=40, pady=140)

# Game Page
game_page = tk.Frame(root, bg="black")  # Set background color to black
tk.Label(game_page, text="Game Page", bg="black", fg="white").pack()  # Set label text color to white for visibility

# Back button for the game page
back_button_game = tk.Button(game_page, text="Back to Main", command=back_to_main_page, bg="black", fg="white")
back_button_game.pack()

# Instruction Page
instruction_page = tk.Frame(root, bg="black")  # Set background color to black
tk.Label(instruction_page, text="Instruction Page", bg="black", fg="white").pack()  # Set label text color to white for visibility
back_button_instruction = tk.Button(instruction_page, text="Back to Main", command=back_to_main_page, bg="black", fg="white")
back_button_instruction.pack()

# High Score Page
high_score_page = tk.Frame(root, bg="black")  # Set background color to black
tk.Label(high_score_page, text="High Score Page", bg="black", fg="white").pack()  # Set label text color to white for visibility
back_button_high_score = tk.Button(high_score_page, text="Back to Main", command=back_to_main_page, bg="black", fg="white")
back_button_high_score.pack()

# Start the main loop
root.mainloop()

# Quit pygame when closing the window
pygame.quit()
