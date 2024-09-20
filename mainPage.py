import tkinter as tk
from tkinter import PhotoImage
import pygame

# Initialize pygame mixer for music
pygame.mixer.init()
pygame.mixer.music.set_volume(0.8) #Music is played at 80%

# Load and play music as soon as the program starts
pygame.mixer.music.load("Assets/BGM.mp3")  # Ensure the file path is correct
pygame.mixer.music.play(-1)  # Play music in a loop

# Function to play or stop the music
music_playing = True
def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()
        music_toggle_button.config(text="Unmute")
    else:
        pygame.mixer.music.unpause()
        music_toggle_button.config(text="Mute")
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
    main_frame.pack_forget()

def back_to_main_page():
    game_page.pack_forget()
    instruction_page.pack_forget()
    high_score_page.pack_forget()
    main_frame.pack()
    pygame.mixer.music.stop()  # Stop music when returning to the main page

# Main application window
root = tk.Tk()
root.title("Main Page")
root.geometry("400x300")

# Load the image for the button
play_btn_image = PhotoImage(file="Assets/Play_btn.png")

# Main frame
main_frame = tk.Frame(root)
main_frame.pack()

# Buttons on the main page
game_button = tk.Button(main_frame, image=play_btn_image, command=open_game_page, borderwidth=0)
instruction_button = tk.Button(main_frame, text="Instructions", command=open_instruction_page, bg="purple", fg="white")
high_score_button = tk.Button(main_frame, text="High Scores", command=open_high_score_page, bg="blue", fg="white")

game_button.pack(pady=10)
instruction_button.pack(pady=10)
high_score_button.pack(pady=10)

# Game Page
game_page = tk.Frame(root)
tk.Label(game_page, text="Game Page").pack()

# Back button for the game page
back_button_game = tk.Button(game_page, text="Back to Main", command=back_to_main_page)
back_button_game.pack()

# Music toggle button on the top right corner
music_toggle_button = tk.Button(root, text="Mute", command=toggle_music)
music_toggle_button.place(x=350, y=10)  # Positioning it on the top right corner

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
