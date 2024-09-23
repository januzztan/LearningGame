import tkinter as tk
from tkinter import PhotoImage
import pygame

# Initialize pygame mixer for music
pygame.mixer.init()
pygame.mixer.music.set_volume(0.7)  # Music is played at 70%

# Load and play music as soon as the program starts
pygame.mixer.music.load("Assets/BGM.mp3")  # Ensure the file path is correct
pygame.mixer.music.play(-1)  # Play music in a loop

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

# Functions to open different pages
def open_game_page():
    hide_main_page()
    game_page.pack()

def open_instruction_page():
    hide_main_page()
    instruction_page.pack()

def open_high_score_page():
    hide_main_page()
    high_score_page.pack()

def hide_main_page():
    button_frame.pack_forget()  # Use button_frame instead of main_frame

def back_to_main_page():
    global music_playing  # Declare global here at the start of the function
    
    # Hide all other pages
    game_page.pack_forget()
    instruction_page.pack_forget()
    high_score_page.pack_forget()
    
    # Repack the main button frame to show the buttons
    button_frame.pack()
    
    # Ensure the music is playing and the button shows the correct state
    if not music_playing:
        pygame.mixer.music.unpause()  # Restart music if it was paused
        music_toggle_button.config(image=volume_play_image)  # Set button to show volume play
    
    # Reset the music playing state to the same as when the game starts
    music_playing = True

# Main application window
root = tk.Tk()
root.title("Main Page")
root.geometry("1920x1080")

# Load the images for the buttons
play_btn_image = PhotoImage(file="Assets/Start_btn.png")
instruction_btn_image = PhotoImage(file="Assets/Instruction_btn.png")  # Load instruction button image
high_score_btn_image = PhotoImage(file="Assets/HighScore_btn.png")     # Load high score button image
volume_play_image = PhotoImage(file="Assets/Volume_play.png")           # Image for volume play
volume_mute_image = PhotoImage(file="Assets/Volume_mute.png")           # Image for volume mute

# Music toggle button on the top right corner with image
music_toggle_button = tk.Button(root, image=volume_play_image, command=toggle_music, borderwidth=0)
music_toggle_button.place(x=1180, y=10)  # Positioning it on the top right corner

# Main frame at the bottom to hold buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)  # Placing at the bottom of the window and stretching horizontally

# Buttons on the main page inside the frame
game_button = tk.Button(button_frame, image=play_btn_image, command=open_game_page, borderwidth=0)
instruction_button = tk.Button(button_frame, image=instruction_btn_image, command=open_instruction_page, borderwidth=0)
high_score_button = tk.Button(button_frame, image=high_score_btn_image, command=open_high_score_page, borderwidth=0)

# Align the buttons in a row inside the frame
game_button.pack(side=tk.LEFT, padx=40, pady=160)
instruction_button.pack(side=tk.LEFT, padx=40, pady=160)
high_score_button.pack(side=tk.LEFT, padx=40, pady=160)

# Game Page
game_page = tk.Frame(root)
tk.Label(game_page, text="Game Page").pack()

# Back button for the game page
back_button_game = tk.Button(game_page, text="Back to Main", command=back_to_main_page)
back_button_game.pack()

# Instruction Page
instruction_page = tk.Frame(root)
tk.Label(instruction_page, text="Instruction Page").pack()
back_button_instruction = tk.Button(instruction_page, text="Back to Main", command=back_to_main_page)
back_button_instruction.pack()

# High Score Page
high_score_page = tk.Frame(root)
tk.Label(high_score_page, text="High Score Page").pack()
back_button_high_score = tk.Button(high_score_page, text="Back to Main", command=back_to_main_page)
back_button_high_score.pack()

# Start the main loop
root.mainloop()

# Quit pygame when closing the window
pygame.quit()
