import tkinter as tk
from tkinter import PhotoImage, messagebox
import pygame
import random

#Main Page

# Initialize pygame mixer for music and sound effects
pygame.mixer.init()
pygame.mixer.music.set_volume(0.15)  # Music is played at 15%

# Load and play background music as soon as the program starts
pygame.mixer.music.load("Assets/BGM.mp3")  # Ensure the file path is correct
pygame.mixer.music.play(-1)  # Play music in a loop

# Load the mouse click sound
click_sound = pygame.mixer.Sound("Assets/mouse_click.mp3")

# Function to play the click sound
def play_click_sound():
    click_sound.play()

# Functions to open different pages
def open_game_page():
    play_click_sound()  # Play click sound
    main_menu_frame.pack_forget()  # Hide the main menu frame
    game_page.pack(fill="both", expand=True)  # Show the game page
    app.start_game()  # Call start_game from the LearningGame instance

def open_instruction_page():
    play_click_sound()  # Play click sound
    main_menu_frame.pack_forget()  # Hide the main menu frame
    instruction_page.pack(fill="both", expand=True)  # Show the instruction page

def open_high_score_page():
    play_click_sound()  # Play click sound
    main_menu_frame.pack_forget()  # Hide the main menu frame
    high_score_page.pack(fill="both", expand=True)  # Show the high score page

def back_to_main_page():
    play_click_sound()  # Play click sound
    app.reset_game_state()  # Reset the game state including the pause and overlay
    game_page.pack_forget()  # Hide the game page
    instruction_page.pack_forget()  # Hide the instruction page
    high_score_page.pack_forget()  # Hide the high score page
    main_menu_frame.pack(fill="both", expand=True)  # Show the main menu frame

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

# Main application window setup
root = tk.Tk()
root.title("Main Page")
root.attributes('-fullscreen', True)  # Set the window to full screen
root.bind("<Escape>", lambda e: exit_fullscreen())  # Bind Escape key to exit full screen
root.configure(bg="lightgray")  # Set background color to light gray

def exit_fullscreen():
    root.attributes('-fullscreen', False)  # Exit full screen
    root.state('zoomed')


# Load images for the main menu buttons and title
play_btn_image = PhotoImage(file="Assets/Start_btn.png")
instruction_btn_image = PhotoImage(file="Assets/Instruction_btn.png")
high_score_btn_image = PhotoImage(file="Assets/HighScore_btn.png")
volume_play_image = PhotoImage(file="Assets/Volume_play.png")
volume_mute_image = PhotoImage(file="Assets/Volume_mute.png")
title_image = PhotoImage(file="Assets/Title.png")

# Create main menu frame and buttons
main_menu_frame = tk.Frame(root, bg="black")
main_menu_frame.pack(fill="both", expand=True)

# Title image
title_image_label = tk.Label(main_menu_frame, image=title_image, bg="black")
title_image_label.pack(pady=150)

# Music toggle button
music_toggle_button = tk.Button(main_menu_frame, image=volume_play_image, command=lambda: [play_click_sound(), toggle_music()], borderwidth=0, bg="black")
music_toggle_button.place(relx=0.98, rely=0.02, anchor="ne")

# Button frame to hold the buttons
button_frame = tk.Frame(main_menu_frame, bg="black")
button_frame.place(relx=0.5, rely=1.0, anchor="s")

# Create the buttons and pack them into the frame
play_button = tk.Button(button_frame, image=play_btn_image, command=open_game_page, borderwidth=0, bg="lightgray")
instruction_button = tk.Button(button_frame, image=instruction_btn_image, command=open_instruction_page, borderwidth=0, bg="lightgray")
high_score_button = tk.Button(button_frame, image=high_score_btn_image, command=open_high_score_page, borderwidth=0, bg="lightgray")

play_button.pack(side=tk.LEFT, padx=40, pady=40)
instruction_button.pack(side=tk.LEFT, padx=40, pady=40)
high_score_button.pack(side=tk.LEFT, padx=40, pady=40)

# Create other pages
game_page = tk.Frame(root, bg="lightgray")
instruction_page = tk.Frame(root, bg="lightgray")
high_score_page = tk.Frame(root, bg="lightgray")

# Create a frame for the high score list
high_score_frame = tk.Frame(high_score_page, bg="lightgray")
high_score_frame.pack(pady=20)  # Add some padding at the top



#Game

# Function to load words from a file for the game
def load_words():
    word_list = []
    try:
        with open("Assets/dictionary/words.txt", "r") as f:
            word_list = f.read().splitlines()
    except FileNotFoundError:
        word_list = ['apple', 'banana', 'cat', 'dog', 'elephant']
    return word_list

# Main Game Class
class LearningGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Learning Game for Kids")
        self.root.geometry("1920x1080")
        self.root.state('zoomed')
        
        self.points = 0
        self.question_type = None
        self.correct_answer = None
        self.game_paused = False
        self.overlay_displayed = False
        
        self.word_list = load_words()

        # GUI components for the game
        self.label = tk.Label(game_page, text="Press Start to begin!", font=("Helvetica", 40), bg="lightgray")
        self.label.pack(pady=(80,40))
        
        self.entry = tk.Entry(game_page, font=("Helvetica", 30), width=20)
        self.entry.pack(pady=20)
        
        self.submit_button = tk.Button(game_page, text="Submit", command=self.check_answer, font=("Helvetica", 24))
        self.submit_button.pack(pady=20)
        
        self.points_label = tk.Label(game_page, text=f"Points: {self.points}", font=("Helvetica", 30), bg="lightgray")
        self.points_label.pack(pady=20)

        self.feedback_frame = tk.Frame(game_page, bg="lightgray")
        self.feedback_frame.pack(pady=20)

        self.cross_label = tk.Label(self.feedback_frame, text="", font=("Helvetica", 200), fg="red", bg="lightgray")
        self.cross_label.grid(row=0, column=0)

        self.tick_label = tk.Label(self.feedback_frame, text="", font=("Helvetica", 200), fg="green", bg="lightgray")
        self.tick_label.grid(row=0, column=0)

        # Add Pause/Unpause button
        self.pause_button = tk.Button(game_page, text="Pause", command=self.toggle_pause, font=("Helvetica", 24))
        self.pause_button.place(relx=0.98, rely=0.02, anchor="ne")  # Top-right corner


        self.root.bind('<Return>', lambda event: self.check_answer())

    def start_game(self):
        # Reset the game state before starting a new game
        self.reset_game_state()
        self.points = 0
        self.points_label.config(text=f"Points: {self.points}")
        self.ask_question()

    def reset_game_state(self):
        # Reset the paused state
        self.game_paused = False
        self.overlay_displayed = False
        self.pause_button.config(text="Pause")

        # Remove the overlay if it's displayed
        if hasattr(self, 'overlay_frame'):
            self.overlay_frame.destroy()

        # Reset points and other game variables
        self.points = 0
        self.points_label.config(text=f"Points: {self.points}")



    def ask_question(self):
        if not self.game_paused:
            self.entry.delete(0, tk.END)
            self.cross_label.config(text="")
            self.tick_label.config(text="")
            question_type = random.choice(['math', 'word'])
            self.question_type = question_type

            if question_type == 'math':
                self.generate_random_math_problem()
            else:
                self.generate_random_word_problem()

    def generate_random_math_problem(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-'])
        if op == '+':
            self.correct_answer = a + b
        else:
            self.correct_answer = a - b
        self.label.config(text=f"What is {a} {op} {b}?")

    def generate_random_word_problem(self):
        word = random.choice(self.word_list)
        self.correct_answer = word
        self.label.config(text=f"Type the word: {word}")

    def check_answer(self):
        if not self.game_paused:
            user_input = self.entry.get()
            if self.question_type == 'math':
                try:
                    if int(user_input) == self.correct_answer:
                        self.correct_response()
                    else:
                        self.incorrect_response()
                except ValueError:
                    self.incorrect_response()
            else:
                if user_input.lower() == self.correct_answer.lower():
                    self.correct_response()
                else:
                    self.incorrect_response()

    def correct_response(self):
        self.play_sound('correct')
        self.points += 10
        self.points_label.config(text=f"Points: {self.points}")
        self.flash_green_tick()
        self.root.after(1000, self.ask_question)

    def incorrect_response(self):
        self.play_sound('incorrect')
        self.flash_red_cross()
        self.root.after(1000, self.go_to_main_menu)

    def flash_red_cross(self):
        self.cross_label.config(text="X")
        self.tick_label.config(text="")
        self.root.after(1000, lambda: self.cross_label.config(text=""))

    def flash_green_tick(self):
        self.tick_label.config(text="✓")
        self.cross_label.config(text="")
        self.root.after(1000, lambda: self.tick_label.config(text=""))

    def play_sound(self, result):
        if result == 'correct':
            pygame.mixer.Sound("Assets/correct.mp3").play()
        elif result == 'incorrect':
            pygame.mixer.Sound('Assets/incorrect.mp3').play()
        
    def go_to_main_menu(self):
        back_to_main_page()

#OverLay

    # Define colors in hex
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    BLUE = "#0000FF"
    GRAY = "#646464"
    GREEN = "#00FF00"
    RED = "#FF0000"
    YELLOW = "#FFFF00"

    # Pause and Overlay management functions
    def toggle_pause(self):
        if self.game_paused:
            self.game_paused = False
            self.pause_button.config(text="Pause")
            self.remove_overlay()  # Hide pause overlay when resuming the game
            self.remove_instructions_overlay()  # Hide instructions overlay if it is displayed
        else:
            self.game_paused = True
            self.pause_button.config(text="Resume")
            self.show_overlay()  # Show pause overlay

    def remove_instructions_overlay(self):
        if hasattr(self, 'instructions_overlay_frame'):
            self.instructions_overlay_frame.destroy()  # Destroy the instructions overlay if it exists


    def toggle_overlay(self):
        if self.overlay_displayed:
            self.remove_overlay()
        else:
            self.show_overlay()

        # Function to show the overlay
    def show_overlay(self):
        self.overlay_frame = tk.Frame(game_page, bg="GRAY")
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Cover the whole game page
        self.overlay_frame.tkraise()  # Ensure the overlay is on top of everything

        # Create overlay text
        overlay_label = tk.Label(self.overlay_frame, text="Game Paused", font=("Helvetica", 48), fg="YELLOW", bg="GRAY")
        overlay_label.pack(pady=30)  # Add some top padding

        # Centralize buttons by creating a frame and using the pack manager
        button_frame = tk.Frame(self.overlay_frame, bg="GRAY")
        button_frame.pack(pady=50)  # Add padding to position the buttons centrally

        # Button to resume the game
        resume_button = tk.Button(button_frame, text="Resume Game", command=self.toggle_pause, font=("Helvetica", 24), bg="GREEN", fg="WHITE")
        resume_button.pack(padx=20, pady=20, fill=tk.X)  # Expand to fit horizontally

        # Button to show instructions overlay
        instruction_button = tk.Button(button_frame, text="Show Instructions", command=self.show_instructions_overlay, font=("Helvetica", 24), bg="BLUE", fg="WHITE")
        instruction_button.pack(padx=20, pady=20, fill=tk.X)

        # Button to go back to the main page
        main_menu_button = tk.Button(button_frame, text="Main Menu", command=self.go_to_main_menu, font=("Helvetica", 24), bg="RED", fg="WHITE")
        main_menu_button.pack(padx=20, pady=20, fill=tk.X)

        self.overlay_displayed = True  # Set flag to indicate overlay is displayed


    def show_instructions_overlay(self):
        self.instructions_overlay_frame = tk.Frame(game_page, bg="gray")
        self.instructions_overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Cover the whole game page
        self.instructions_overlay_frame.tkraise()  # Ensure the overlay is on top of everything

        # Instruction Title
        overlay_label = tk.Label(self.instructions_overlay_frame, text="How to play:", font=("Helvetica", 48), fg="yellow", bg="gray")
        overlay_label.pack(pady=30)  # Top padding for the title

        # Padding and font settings
        x_offset = 50  # Padding from the left side
        small_font = ("Helvetica", 28)  # Smaller font size for instructions
        y_offset = 50  # Initial vertical offset

        # Instruction 1 (simple, on one line)
        instruction1_label = tk.Label(self.instructions_overlay_frame, text="1. You start with 3 lives and 0 points.", font=small_font, fg="white", bg="gray")
        instruction1_label.pack(anchor="w", padx=x_offset)  # Left aligned with padding

        # Instruction 2
        part1_label = tk.Label(self.instructions_overlay_frame, text="2. If you see: ", font=small_font, fg="white", bg="gray")
        part1_label.pack(anchor="w", padx=x_offset)

        # Instruction 2 (RED and words in the same line)
        instruction2_frame = tk.Frame(self.instructions_overlay_frame, bg="gray")
        instruction2_frame.pack(anchor="w", padx=x_offset+30, pady=10)  # Left aligned, same line

        red_label = tk.Label(instruction2_frame, text="RED", font=small_font, fg="red", bg="gray")
        red_label.pack(side=tk.LEFT)

        part2_label = tk.Label(instruction2_frame, text=" words, type them exactly.", font=small_font, fg="white", bg="gray")
        part2_label.pack(side=tk.LEFT)

        # Instruction 3 (BLUE and words in the same line)
        instruction3_frame = tk.Frame(self.instructions_overlay_frame, bg="gray")
        instruction3_frame.pack(anchor="w", padx=x_offset+30, pady=10)  # Left aligned, same line

        part3_label = tk.Label(instruction3_frame, text="BLUE", font=small_font, fg="blue", bg="gray")
        part3_label.pack(side=tk.LEFT)

        part4_label = tk.Label(instruction3_frame, text=" words, solve the math.", font=small_font, fg="white", bg="gray")
        part4_label.pack(side=tk.LEFT)

        # Instruction 4
        instruction4_label = tk.Label(self.instructions_overlay_frame, text="3. Get it right:", font=small_font, fg="white", bg="gray")
        instruction4_label.pack(anchor="w", padx=x_offset, pady=10)  # Left aligned with padding

        instruction4_label1 = tk.Label(self.instructions_overlay_frame, text="You get 10 points!", font=small_font, fg="green", bg="gray")
        instruction4_label1.pack(anchor="w", padx=x_offset+30, pady=10)  # Left aligned with padding

        # Instruction 5
        instruction5_frame = tk.Frame(self.instructions_overlay_frame, bg="gray")
        instruction5_frame.pack(anchor="w", padx=x_offset, pady=10)

        instruction5_part1_label = tk.Label(instruction5_frame, text="4. Get it wrong or take too long: ", font=small_font, fg="white", bg="gray")
        instruction5_part1_label.pack(side=tk.LEFT)

        instruction5_part2_label = tk.Label(self.instructions_overlay_frame, text="You lose 1 life.", font=small_font, fg="red", bg="gray")
        instruction5_part2_label.pack(anchor="w", padx=x_offset+30, pady=10)

        # Final instruction (simple, on one line)
        instruction6_label = tk.Label(self.instructions_overlay_frame, text="5. If you lose all 3 lives, the game ends.", font=small_font, fg="white", bg="gray")
        instruction6_label.pack(anchor="w", padx=x_offset, pady=10)

        # Back button to close the instruction overlay and return to the pause overlay
        back_button = tk.Button(self.instructions_overlay_frame, text="Back", command=self.show_overlay, font=("Helvetica", 24), bg='gray', fg='white')
        back_button.pack(pady=30)





    def remove_overlay(self):
        self.overlay_frame.destroy()
        self.overlay_displayed = False

# Dummy high scores
high_scores = [
    ("ABC", 150),
    ("DEF", 120),
    ("GHI", 100),
    ("JKL", 80),
    ("MNO", 50)
]

# Generate dummy high scores
dummy_scores = [(f"Player{i:03}", random.randint(50, 100)) for i in range(1, 6)]

# Create a label for each high score and pack them into the frame
for name, score in high_scores:
    score_label = tk.Label(high_score_frame, text=f"{name}      {score}", font=("Helvetica", 24), bg="lightgray")
    score_label.pack(pady=10)  # Add some vertical padding

# Center the high score frame
high_score_frame.place(relx=0.5, rely=0.5, anchor="center")

# Back button to return to main menu
back_button = tk.Button(high_score_page, text="Back", command=back_to_main_page, font=("Helvetica", 24), bg="lightgray")
back_button.pack(side=tk.BOTTOM, pady=(20, 30))  # Add some padding at the bottom


# Initialize the LearningGame instance
app = LearningGame(root)

# Start the application
root.mainloop()

