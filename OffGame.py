import tkinter as tk
from tkinter import PhotoImage, messagebox
import random
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
    main_menu_frame.pack_forget()  # Hide the main menu frame
    game_page.pack(fill="both", expand=True)  # Show the game page
    
    # Automatically start the game
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
    game_page.pack_forget()  # Hide the game page
    instruction_page.pack_forget()  # Hide the instruction page
    high_score_page.pack_forget()  # Hide the high score page
    
    # Show the main menu frame
    main_menu_frame.pack(fill="both", expand=True)  

# Function to load words from an English dictionary file
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
        self.points = 0
        self.question_type = None  # Will hold 'math' or 'word'
        self.correct_answer = None
        
        # Load words
        self.word_list = load_words()

        # GUI components
        self.label = tk.Label(game_page, text="Press Start to begin!", font=("Helvetica", 40), bg="lightgray")  # Bigger font for larger screen
        self.label.pack(pady=40)
        
        self.entry = tk.Entry(game_page, font=("Helvetica", 30), width=20)  # Bigger input field
        self.entry.pack(pady=20)
        
        self.submit_button = tk.Button(game_page, text="Submit", command=self.check_answer, font=("Helvetica", 24))
        self.submit_button.pack(pady=20)
        
        self.points_label = tk.Label(game_page, text=f"Points: {self.points}", font=("Helvetica", 30), bg="lightgray")
        self.points_label.pack(pady=20)
        
        # Red cross and green tick labels (initially hidden)
        self.cross_label = tk.Label(game_page, text="", font=("Helvetica", 200), fg="red", bg="lightgray")
        self.cross_label.pack()  # Ensure the cross label is added to the layout
        
        self.tick_label = tk.Label(game_page, text="", font=("Helvetica", 200), fg="green", bg="lightgray")
        self.tick_label.pack()  # Ensure the green tick label is added to the layout
        
        self.root.bind('<Return>', lambda event: self.check_answer())
    
    def start_game(self):
        self.points = 0
        self.points_label.config(text=f"Points: {self.points}")
        self.ask_question()
    
    def ask_question(self):
        self.entry.delete(0, tk.END)  # Clear the input box
        self.cross_label.config(text="")  # Hide the red cross if visible
        self.tick_label.config(text="")  # Hide the green tick if visible
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
        user_input = self.entry.get()
        
        if self.question_type == 'math':
            try:
                if int(user_input) == self.correct_answer:
                    self.correct_response()
                else:
                    self.incorrect_response()
            except ValueError:
                messagebox.showwarning("Invalid input", "Please enter a valid number.")
        else:
            if user_input.lower() == self.correct_answer.lower():
                self.correct_response()
            else:
                self.incorrect_response()
    
    def correct_response(self):
        self.points += 1
        self.points_label.config(text=f"Points: {self.points}")
        self.flash_green_tick()  # Flash the green tick for correct answers
        self.root.after(1000, self.ask_question)  # Wait 1 second and ask the next question
    
    def incorrect_response(self):
        self.flash_red_cross()  # Flash the red cross for incorrect answers
        self.root.after(1000, self.go_to_main_menu)  # After 1 second, go to the main menu

    def go_to_main_menu(self):
        back_to_main_page()  # Go back to the main menu
    
    def flash_red_cross(self):
        self.cross_label.config(text="X")  # Show the red cross
        self.root.after(1000, lambda: self.cross_label.config(text=""))  # Hide the red cross after 1 second
    
    def flash_green_tick(self):
        self.tick_label.config(text="✓")  # Show the green tick
        self.root.after(1000, lambda: self.tick_label.config(text=""))  # Hide the green tick after 1 second

# Main application window
root = tk.Tk()
root.title("Main Page")
root.attributes('-fullscreen', True)  # Set the window to full screen
root.bind("<Escape>", lambda e: exit_fullscreen())  # Bind Escape key to exit full screen
root.configure(bg="lightgray")  # Set background color to light gray

def exit_fullscreen():
    root.attributes('-fullscreen', False)  # Exit full screen
    root.state('zoomed')
    root.attributes('-zoomed', True)

# Load the images for the buttons and title image
play_btn_image = PhotoImage(file="Assets/Start_btn.png")
instruction_btn_image = PhotoImage(file="Assets/Instruction_btn.png")  # Load instruction button image
high_score_btn_image = PhotoImage(file="Assets/HighScore_btn.png")     # Load high score button image
volume_play_image = PhotoImage(file="Assets/Volume_play.png")           # Image for volume play
volume_mute_image = PhotoImage(file="Assets/Volume_mute.png")           # Image for volume mute
title_image = PhotoImage(file="Assets/Title.png")                      # Load the title image

# Create main menu frame
main_menu_frame = tk.Frame(root, bg="black")
main_menu_frame.pack(fill="both", expand=True)  # Pack the main menu frame

# Title image label (centered)
title_image_label = tk.Label(main_menu_frame, image=title_image, bg="black")
title_image_label.pack(pady=150)  # Add padding to position it in the middle

# Music toggle button on the top right corner with image
music_toggle_button = tk.Button(main_menu_frame, image=volume_play_image, command=lambda: [play_click_sound(), toggle_music()], borderwidth=0, bg="black")
music_toggle_button.place(relx=0.98, rely=0.02, anchor="ne")  # Position the button in the top-right corner

# Main frame to hold buttons
button_frame = tk.Frame(main_menu_frame, bg="black")  # Set background color to light gray
button_frame.place(relx=0.5, rely=1.0, anchor="s")  # Position at the bottom center

# Start button
play_button = tk.Button(button_frame, image=play_btn_image, command=open_game_page, borderwidth=0, bg="lightgray")

# Instruction button
instruction_button = tk.Button(button_frame, image=instruction_btn_image, command=open_instruction_page, borderwidth=0, bg="lightgray")

# High score button
high_score_button = tk.Button(button_frame, image=high_score_btn_image, command=open_high_score_page, borderwidth=0, bg="lightgray")

# Align the buttons in a row inside the frame
play_button.pack(side=tk.LEFT, padx=40, pady=40)
instruction_button.pack(side=tk.LEFT, padx=40, pady=40)
high_score_button.pack(side=tk.LEFT, padx=40, pady=40)

# Create other frames for the game page and instruction page
game_page = tk.Frame(root, bg="lightgray")
instruction_page = tk.Frame(root, bg="lightgray")
high_score_page = tk.Frame(root, bg="lightgray")

# Initialize the LearningGame instance
app = LearningGame(root)

# Start the application
root.mainloop()
