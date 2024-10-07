import tkinter as tk
import random
import pygame
import tkinter.messagebox as messagebox  # Import the messagebox module
from PIL import Image, ImageTk

class GamePage(tk.Frame):
    """ GamePage is a class that defines the main game interface and functionality for a word and math-based game using the tkinter framework."""
    def __init__(self, app, back_to_main_page_callback):

        # Load dictionary of words from txt files
        def load_words():
            """ Reads normal words used in game from words.txt. Assigns words into list, word_list."""
            word_list = []
            try:
                with open("Assets/dictionary/words.txt", "r") as f:
                    word_list = f.read().splitlines()
            except FileNotFoundError:
                word_list = ['apple', 'banana', 'cat', 'dog', 'elephant']
            return word_list

        def load_hard_words():
            """ Reads hard words used in game from hard_words.txt. Assigns words into list, word_list."""
            word_list = []
            try:
                with open("Assets/dictionary/hard_words.txt", "r") as f:
                    word_list = f.read().splitlines()
            except FileNotFoundError:
                word_list = ['Whisper', 'Journey', 'Treasure', 'Giggle', 'Rainbow']
            return word_list

        super().__init__(app.root, bg="black")
        self.app = app
        self.points = 0
        self.lives = 3
        self.question_type = None
        self.correct_answer = None
        self.game_paused = False
        self.overlay_displayed = False
        self.timer = 21
        self.timer_active = False


        # Assign variables from Load words
        self.word_list = load_words()
        self.hard_word_list = load_hard_words()

        # Store callback to main page
        self.back_to_main_page = back_to_main_page_callback


        # Load and resize pause image
        self.pause_image_original = self.load_and_resize_image("Assets/Pictures/Pause_btn.png", (60, 60))

        # Load and resize heart images
        self.heart_full_image_original = self.load_and_resize_image("Assets/Pictures/heart_full.png", (60, 60))
        self.heart_empty_image_original = self.load_and_resize_image("Assets/Pictures/heart_empty.png", (60, 60))

        # Load and resize cross and tick images
        self.cross_image_original = self.load_and_resize_image("Assets/Pictures/cross.png", (60, 60))
        self.tick_image_original = self.load_and_resize_image("Assets/Pictures/tick.png", (60, 60))

        # Initialize current images
        self.pause_image = self.pause_image_original
        self.heart_full_image = self.heart_full_image_original
        self.heart_empty_image = self.heart_empty_image_original
        self.cross_image = self.cross_image_original
        self.tick_image = self.tick_image_original

        # Load game over image (original size, will resize dynamically)
        try:
            self.original_gameover_img = Image.open("Assets/Pictures/GameOver.png")
            self.gameover_size = (400, 300)  # Initial size, will be resized
            self.img_tk_gameover = ImageTk.PhotoImage(
                self.original_gameover_img.resize(self.gameover_size, Image.Resampling.LANCZOS)
            )
        except FileNotFoundError:
            print("Game Over image not found: Assets/Pictures/GameOver.png. Using placeholder.")
            self.original_gameover_img = Image.new('RGBA', (400, 300), (255, 0, 0, 0))
            self.img_tk_gameover = ImageTk.PhotoImage(self.original_gameover_img)

        # Configure grid weights for resizing
        self.grid_rowconfigure(0, weight=1)  # Timer, points, and pause row
        self.grid_rowconfigure(1, weight=3)  # Question frame row (resizable)
        self.grid_rowconfigure(2, weight=2)  # Input frame row (resizable)
        self.grid_rowconfigure(3, weight=1)  # Feedback row (resizable)
        self.grid_rowconfigure(4, weight=1)  # Lives row
        self.grid_columnconfigure(0, weight=1, minsize=250)
        self.grid_columnconfigure(1, weight=1, minsize=250)
        self.grid_columnconfigure(2, weight=1, minsize=250)

        # Timer Label on the left
        self.timer_frame= tk.Frame(self, bg="black")
        self.timer_label = tk.Label(
            self.timer_frame, 
            text=f"Time Left: {self.timer}s", 
            font=("Courier", 24, "bold"), 
            fg="white", 
            bg="black"
        )
        self.timer_label.pack(expand=True, padx=(10,0))
        self.timer_frame.grid(row=0, column=0, sticky="nsw")

        # Points label in the centre
        self.point_frame= tk.Frame(self, bg="black")
        self.points_label = tk.Label(
            self.point_frame, 
            text=f"Points: {self.points}", 
            font=("Courier", 24, "bold"), 
            bg="black", 
            fg="white"
        )
        self.points_label.pack(fill='both', expand=True)
        self.point_frame.grid(row=0, column=1, sticky="nsew")

        # Pause Button on the right
        self.button_frame = tk.Frame(self, bg="black")
        self.pause_button = tk.Button(
            self.button_frame, 
            image=self.pause_image, 
            command= self.app.play_with_sound(lambda:self.toggle_pause()), 
            bg="black", 
            borderwidth=0
        )
        self.pause_button.pack(fill='both', expand=True)
        self.pause_button.image = self.pause_image  # Keep a reference to avoid garbage collection
        self.button_frame.grid(row=0, column=2, sticky="nse", padx=(0,10))

        # Update the layout of hearts (smaller size, centered)
        self.lives_frame = tk.Frame(self, bg="black")
        self.lives_frame.grid(row=4, column=0, columnspan=3, sticky="ns", pady=(10, 20))  # Lives row in center column with top and bottom padding
        self.lives_labels = []  # Store heart image labels in list
        for i in range(3):
            label = tk.Label(self.lives_frame, image=self.heart_full_image, bg="black")
            label.pack(side="left", padx=5, expand=True, fill='both')  # Space between hearts
            self.lives_labels.append(label)

        # Create a frame for the question label, spanning all columns
        self.question_frame = tk.Frame(self, bg="black")
        self.question_frame.grid(
            row=1, 
            column=0, 
            columnspan=3, 
            sticky="nsew", 
            padx=20, 
            pady=10
        )  # Span across columns with padding

        # Question label inside the frame (initial smaller font)
        self.label = tk.Label(
            self.question_frame, 
            font=("Courier", 45, "bold"), 
            bg="black", 
            fg="white", 
            wraplength=800
        )  # Make the font smaller
        self.label.pack(expand=True, padx=20, pady=20)  # Center the label and add padding

        # Configure the question frame to resize
        self.question_frame.grid_rowconfigure(0, weight=1)
        self.question_frame.grid_columnconfigure(0, weight=1)

        # Bind window resize event to a function
        self.bind("<Configure>", self.resize_text)

        # Frame to hold the entry box and submit button
        self.input_frame = tk.Frame(self, bg="black")
        self.input_frame.grid(
            row=2, 
            column=0, 
            columnspan=3, 
            sticky="nsew", 
            padx=20, 
            pady=(10, 20)
        )  # Span across all columns with padding

        # Ensure the input frame is centered by configuring its weight
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)

        # Subframe to stack the entry box and submit button vertically
        self.entry_button_frame = tk.Frame(self.input_frame, bg="black")
        self.entry_button_frame.grid(row=0, column=0)

        # Entry box (centered in the subframe)
        self.entry = tk.Entry(
            self.entry_button_frame, 
            font=("Courier", 30, "bold"), 
            width=25, 
            justify="center"
        )
        self.entry.pack(pady=(10, 20))  # Add padding to space it out from the button

        # Submit button (centered below the entry box)
        self.submit_button = tk.Button(
            self.entry_button_frame, 
            text="Submit", 
            command=self.app.play_with_sound(lambda: self.check_answer()), 
            font=("Courier", 24, "bold")
        )
        self.submit_button.pack(pady=(0, 10))  # Add padding below the button

        # Frame to hold the feedback graphics, spanning all columns
        self.feedback_frame = tk.Frame(self, bg="black")
        self.feedback_frame.grid(
            row=3, 
            column=0, 
            columnspan=3, 
            sticky="nsew", 
            padx=20, 
            pady=10
        )  # Span across columns with padding

        # Cross graphic
        self.cross_label = tk.Label(self.feedback_frame, image="", bg="black")
        self.cross_label.pack(side="left", expand=True, fill="both")

        # Ensure the feedback graphics and hearts are also centered
        self.feedback_frame.grid_rowconfigure(0, weight=1)
        self.feedback_frame.grid_columnconfigure(0, weight=1)

        self.lives_frame.grid_rowconfigure(0, weight=1)

    # Instance method to load and resize images
    def load_and_resize_image(self, path, size):
        """ Instance method to load and resize images."""
        try:
            img_original = Image.open(path)
            img_resized = img_original.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img_resized)
        except FileNotFoundError:
            print(f"Image file not found: {path}. Using placeholder.")
            # Create a placeholder image (e.g., a blank image)
            placeholder = Image.new('RGBA', size, (255, 0, 0, 0))
            return ImageTk.PhotoImage(placeholder)
        except Exception as e:
            print(f"Error loading image {path}: {e}. Using placeholder.")
            placeholder = Image.new('RGBA', size, (255, 0, 0, 0))
            return ImageTk.PhotoImage(placeholder)

    # Dynamically resize the label fonts and images when the window size changes
    def resize_text(self, event):
        """ Dynamically resize the label fonts and images when the window size changes."""
        new_width = event.width

        # Ensure the font size doesn't drop below a minimum threshold
        font_size = max(int(new_width / 25) + 5, 12)  # Adjust 12 to set the minimum font size
        self.label.config(font=("Courier", font_size, "bold"))

        # Resize timer label font, ensure it doesn't drop below a minimum threshold
        timer_font_size = max(int(new_width / 60)+2, 12)  # Adjust 12 to set the minimum timer font size
        self.timer_label.config(font=("Courier", timer_font_size, "bold"))

        # Resize points label font
        points_font_size = max(int(new_width / 55)+2, 12)  # Adjust for points label
        self.points_label.config(font=("Courier", points_font_size, "bold"))

        # Dynamically resize heart, cross, and tick images based on the new width
        # Define minimum sizes to prevent them from becoming too small
        min_heart_size = (70, 70)
        min_cross_tick_size = (70, 70)

        # Calculate new sizes with minimum constraints
        new_heart_width = max(int(new_width / 10), min_heart_size[0])
        new_heart_height = max(int(new_width / 10), min_heart_size[1])
        heart_size = (new_heart_width, new_heart_height)

        new_cross_width = max(int(new_width / 10), min_cross_tick_size[0])
        new_cross_height = max(int(new_width / 10), min_cross_tick_size[1])
        cross_tick_size = (new_cross_width, new_cross_height)

        # Resize and update heart images
        self.heart_full_image = self.load_and_resize_image("Assets/Pictures/heart_full.png", heart_size)
        self.heart_empty_image = self.load_and_resize_image("Assets/Pictures/heart_empty.png", heart_size)
        for i, label in enumerate(self.lives_labels):
            if i < self.lives:
                label.config(image=self.heart_full_image)
                label.image = self.heart_full_image  # Update reference
            else:
                label.config(image=self.heart_empty_image)
                label.image = self.heart_empty_image  # Update reference

        # Resize and update cross/tick images
        self.cross_image = self.load_and_resize_image("Assets/Pictures/cross.png", cross_tick_size)
        self.tick_image = self.load_and_resize_image("Assets/Pictures/tick.png", cross_tick_size)

    # Bind the Enter key to game actions
    def bind_enter_key(self):
        """ Bind the Enter key to game actions."""
        self.app.root.bind("<Return>", lambda event: self.check_answer())

    # Unbind the Enter key when leaving the game
    def unbind_enter_key(self):
        """ Unbind the Enter key when leaving the game."""
        self.app.root.unbind("<Return>")

    # Starts game
    def start_game(self):
        """ Starts game instance."""
        self.reset_game_state()
        self.ask_question()

    #resets game / initialize default game variables
    def reset_game_state(self):
        """ Initialize default variables used at the start of the game and calls functions to display questions and lives."""
        self.game_paused = False
        self.overlay_displayed = False
        self.points = 0
        self.points_label.config(text=f"Points: {self.points}")
        self.lives = 3  # Reset lives to 3
        self.timer = 21  # Reset timer to 21 seconds
        self.pause_button.config(image=self.pause_image)  # Ensure pause button shows pause image
        self.timer_label.config(text=f"Time Left: {self.timer}s")  # Update timer display

        # Update heart images to full hearts (since lives are reset to 3)
        self.update_lives_display()

        # Remove the overlay if it's displayed
        if hasattr(self, 'overlay_frame'):
            self.overlay_frame.destroy()

        # Reset points and other game variables
        self.ask_question()  # Only need to ask the question once after resetting

    # Generates new questions
    def ask_question(self):
        """ Generates new questions."""
        if not self.game_paused:
            self.entry.delete(0, tk.END)
            self.reset_timer()
            question_type = random.choice(['math', 'word'])
            self.question_type = question_type

            if question_type == 'math':
                self.generate_random_math_problem()
                self.label.config(fg="blue")
            else:
                self.generate_random_word_problem()
                self.label.config(fg="red")
        else:
            print("Game is paused. Cannot ask a question.")  # Debugging statement

    # Round countdown timer, 21 secs per question
    def countdown_timer(self):
        """Round countdown timer, 21 secs per question"""
        if not self.game_paused and self.timer > 0 and self.timer_active:
            self.timer -= 1
            self.timer_label.config(text=f"Time Left: {self.timer}s")
            self.timer_callback_id = self.after(1000, self.countdown_timer)  # Schedule the next call of countdown_timer in 1 second (1000 ms)
        elif self.timer == 0:
            self.lose_life()
            self.incorrect_response()
            self.reset_timer()

    # Resets the timer and restarts the countdown for the next question
    def reset_timer(self):
        """ Resets the timer and restarts the countdown for the next question."""
        # Cancel the previous timer if it exists to prevent overlapping timers
        if hasattr(self, 'timer_callback_id'):
            self.after_cancel(self.timer_callback_id)  # Cancel previous timer callback

        # For new question
        self.timer = 21
        self.timer_active = True
        self.timer_label.config(text=f"Time Left: {self.timer}s")
        self.countdown_timer()  # Restart the countdown

    # Generate a math problem, starts with easy questions, increasing difficulty when score >= 200
    # Range of numbers between 1 to 10 only
    def generate_random_math_problem(self):
        """ Generates a math problem."""
        if self.points >= 200:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            op = random.choice(['+', '-', 'x', '/'])
            if op == '/':
                # Ensure a is a multiple of b for integer division
                b = random.randint(1, 10)  # Ensure b is at least 1
                a = b * random.randint(1, 10)  # Ensure a is a multiple of b
        # Easier questions for scores below 200
        else:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            op = random.choice(['+', '-'])

        if op == '+':
            self.correct_answer = a + b
        elif op == '-':
            if a < b:  # Makes sure there are questions that result in positive answers
                a, b = b, a
            self.correct_answer = a - b
        elif op == 'x':
            self.correct_answer = a * b
        elif op == '/':
            self.correct_answer = a // b

        question_text = f"What is {a} {op} {b}?"
        self.label.config(text=question_text)

    # Generate a word to type, starts with easy words, increasing difficulty when score >= 200
    def generate_random_word_problem(self):
        """ Genereates a word problem."""
        if self.points >= 200:
            word = random.choice(self.hard_word_list)
        else:
            word = random.choice(self.word_list)
        self.correct_answer = word
        question_text = f"Type the word: {word}"
        self.label.config(text=question_text)

    # Check response from player
    def check_answer(self):
        """ Check response from player."""
        if not self.game_paused:
            user_input = self.entry.get()
            if self.question_type == 'math':
                try:
                    if int(user_input) == self.correct_answer:
                        self.correct_response()
                    else:
                        self.lose_life()
                        self.incorrect_response()
                except ValueError:
                    self.lose_life()
                    self.incorrect_response()
            else:
                if user_input.lower() == self.correct_answer.lower():
                    self.correct_response()
                else:
                    self.lose_life()
                    self.incorrect_response()

    # Correct response
    def correct_response(self):
        """ Results of correct response."""
        self.play_sound('correct')
        self.points += 10
        self.points_label.config(text=f"Points: {self.points}")
        self.flash_green_tick()
        self.after(1000, self.ask_question)  # Use self.after instead of self.root.after

    # Wrong response
    def incorrect_response(self):
        """ Results of wrong response."""
        self.play_sound('incorrect')
        self.flash_red_cross()

    # Lose life
    def lose_life(self):
        """ Lose life. Updates hearts displayed on screen. Calls game over if no lives left."""
        if not self.game_paused:  # Prevent life loss if the game is paused
            self.lives -= 1
            self.update_lives_display()
            if self.lives <= 0:  # Show game over when lives reach 0
                self.show_game_over_overlay()
            else:  # Move on to the next question after 1 second
                self.after(1000, self.ask_question)

    # Change lives displayed
    def update_lives_display(self):
        """ Updates hearts displayed on screen."""
        for i in range(3):
            if i < self.lives:
                self.lives_labels[i].config(image=self.heart_full_image)
                self.lives_labels[i].image = self.heart_full_image  # Update reference
            else:
                self.lives_labels[i].config(image=self.heart_empty_image)
                self.lives_labels[i].image = self.heart_empty_image  # Update reference

    def show_game_over_overlay(self):
        """ Game over screen. Creates overlay over game page."""
        # Stop the countdown timer if it's still running
        if hasattr(self, 'timer_callback_id'):
            self.after_cancel(self.timer_callback_id)

        # Pauses game instance
        self.game_paused = True

        # Stop the global background music
        pygame.mixer.music.pause()

        # Play "game over" sound and get the sound length
        try:
            gameover_sound = pygame.mixer.Sound('Assets/SFX/gameover_sfx.mp3')
            gameover_sound.play()
            sound_length = gameover_sound.get_length()  # Get the duration of the sound
        except pygame.error as e:
            print(f"Pygame sound error (gameover_sfx.mp3): {e}")  # Debugging statement
            sound_length = 3  # Default to 3 seconds if sound fails

        # Create a "Game Over" overlay
        self.overlay_frame = tk.Frame(self, bg="black")
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Cover the whole game page
        self.overlay_frame.tkraise()

        # Load and display the "Game Over" image
        self.game_over_image_label = tk.Label(self.overlay_frame, image=self.img_tk_gameover, bg="black")
        self.game_over_image_label.pack(expand=True)  # Center the image

        # Bind the window resizing event to dynamically resize the image
        self.bind("<Configure>", self.resize_game_over_image)

        # Delay before redirecting to save game state or exit
        self.after(int(sound_length * 1000), self.redirect_to_save_file)  # Wait the length of the gameover sound

    def resize_game_over_image(self, event):
        """ Resizes game over page to be responsive"""
        # Get the current width and height of the overlay
        new_width = event.width
        new_height = event.height

        # Maintain the aspect ratio of the image
        img_aspect_ratio = self.original_gameover_img.width / self.original_gameover_img.height
        new_aspect_ratio = new_width / new_height

        if new_aspect_ratio > img_aspect_ratio:
            resized_width = int(new_height * img_aspect_ratio)
            resized_height = new_height
        else:
            resized_width = new_width
            resized_height = int(new_width / img_aspect_ratio)

        # Resize the original image to fit the new dimensions
        resized_img = self.original_gameover_img.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
        self.img_tk_gameover = ImageTk.PhotoImage(resized_img)

        # Update the image in the label
        self.game_over_image_label.config(image=self.img_tk_gameover)
        self.game_over_image_label.image = self.img_tk_gameover  # Keep reference to avoid garbage collection

    # Moves to save score page
    def redirect_to_save_file(self):
        """ Displays save score screen to prompt player to save  score into HighScoreList.txt"""
        # Resume the global background music
        self.unbind_enter_key()
        pygame.mixer.music.unpause()  # Resume the paused background music

        # Call the save score method from save_scores.py
        self.app.show_save_score_page(self.points)

    # Flash red cross with wrong response
    def flash_red_cross(self):
        """ Flash red cross with wrong response."""
        self.cross_label.config(image=self.cross_image)
        self.cross_label.image = self.cross_image  # Update reference
        self.after(1000, lambda: self.cross_label.config(image=""))  # Hide after 1 second

    # Flash green tick with correct response
    def flash_green_tick(self):
        """ Flash green tick with correct response."""
        self.cross_label.config(image=self.tick_image)
        self.cross_label.image = self.tick_image  # Update reference
        self.after(1000, lambda: self.cross_label.config(image=""))  # Hide after 1 second

    # Play correct and incorrect sound with response
    def play_sound(self, result):
        """ Plays correct and incorrect sound with corresponsing response."""
        try:
            if result == 'correct':
                correct_sound = pygame.mixer.Sound("Assets/SFX/correct.mp3")
                correct_sound.play()
            elif result == 'incorrect':
                incorrect_sound = pygame.mixer.Sound('Assets/SFX/incorrect.mp3')
                incorrect_sound.play()
        except pygame.error as e:
            print(f"Pygame sound error ({result}.mp3): {e}")  # Debugging statement
    
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
            self.countdown_timer()
            self.pause_button.config(text="Pause")
            self.remove_overlay()  # Hide pause overlay when resuming the game
            self.remove_instructions_overlay()  # Hide instructions overlay if it is displayed
        else:
            self.game_paused = True
            self.after_cancel(self.timer_callback_id)
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

    # Instructions Overlay
    def show_instructions_overlay(self):
        # Hide the pause overlay but keep it in memory to avoid state loss
        self.overlay_frame.place_forget()

        # Create the instructions overlay
        self.instructions_overlay_frame = tk.Frame(self, bg="black")
        self.instructions_overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Cover the whole game page
        self.instructions_overlay_frame.tkraise()

        # Retro-style Title
        self.overlay_label = tk.Label(self.instructions_overlay_frame, text="HOW TO PLAY", font=("Courier", 40, "bold"), fg="lime", bg="black")
        self.overlay_label.pack(pady=30)  # Top padding for the title

        # Padding and font settings
        self.x_offset = 50  # Padding from the left side
        self.small_font = ("Courier", 24, "bold")  # Smaller retro font size for instructions

        # Instruction 1 (simple, one line)
        self.instruction1_label = tk.Label(self.instructions_overlay_frame, text="1. YOU START WITH 3 LIVES AND 0 POINTS.", font=self.small_font, fg="white", bg="black")
        self.instruction1_label.pack(anchor="w", padx=self.x_offset)  # Left aligned with padding

        # Instruction 2 with "RED" highlighted
        self.part1_label = tk.Label(self.instructions_overlay_frame, text="2. IF YOU SEE:", font=self.small_font, fg="white", bg="black")
        self.part1_label.pack(anchor="w", padx=self.x_offset)

        # RED instruction in one line
        self.instruction2_frame = tk.Frame(self.instructions_overlay_frame, bg="black")
        self.instruction2_frame.pack(anchor="w", padx=self.x_offset + 30, pady=10)  # Left aligned, same line

        self.red_label = tk.Label(self.instruction2_frame, text="RED", font=self.small_font, fg="red", bg="black")
        self.red_label.pack(side=tk.LEFT)

        self.part2_label = tk.Label(self.instruction2_frame, text="WORDS, TYPE THEM EXACTLY.", font=self.small_font, fg="white", bg="black")
        self.part2_label.pack(side=tk.LEFT)

        # Instruction 3 with "BLUE" highlighted
        self.instruction3_frame = tk.Frame(self.instructions_overlay_frame, bg="black")
        self.instruction3_frame.pack(anchor="w", padx=self.x_offset + 30, pady=10)  # Left aligned, same line

        self.blue_label = tk.Label(self.instruction3_frame, text="BLUE", font=self.small_font, fg="cyan", bg="black")
        self.blue_label.pack(side=tk.LEFT)

        self.part4_label = tk.Label(self.instruction3_frame, text="WORDS, SOLVE THE MATH.", font=self.small_font, fg="white", bg="black")
        self.part4_label.pack(side=tk.LEFT)

        # Instruction 4
        self.instruction4_label = tk.Label(self.instructions_overlay_frame, text="3. GET IT RIGHT:", font=self.small_font, fg="white", bg="black")
        self.instruction4_label.pack(anchor="w", padx=self.x_offset, pady=10)  # Left aligned with padding

        self.instruction4_label1 = tk.Label(self.instructions_overlay_frame, text="YOU GET 10 POINTS!", font=self.small_font, fg="lime", bg="black")
        self.instruction4_label1.pack(anchor="w", padx=self.x_offset + 30, pady=10)  # Left aligned with padding

        # Instruction 5
        self.instruction5_frame = tk.Frame(self.instructions_overlay_frame, bg="black")
        self.instruction5_frame.pack(anchor="w", padx=self.x_offset, pady=10)

        self.instruction5_part1_label = tk.Label(self.instruction5_frame, text="4. GET IT WRONG OR TAKE TOO LONG:", font=self.small_font, fg="white", bg="black")
        self.instruction5_part1_label.pack(side=tk.LEFT)

        self.instruction5_part2_label = tk.Label(self.instructions_overlay_frame, text="YOU LOSE 1 LIFE.", font=self.small_font, fg="red", bg="black")
        self.instruction5_part2_label.pack(anchor="w", padx=self.x_offset + 30, pady=10)

        # Final instruction (simple, one line)
        self.instruction6_label = tk.Label(self.instructions_overlay_frame, text="5. LOSE ALL 3 LIVES, GAME ENDS.", font=self.small_font, fg="white", bg="black")
        self.instruction6_label.pack(anchor="w", padx=self.x_offset, pady=10)

        # Retro-style Back button
        self.back_button = tk.Button(self.instructions_overlay_frame, text="BACK", command=self.app.play_with_sound(self.hide_instructions_overlay), font=("Courier", 28, "bold"), bg="gray", fg="black", width=10, bd=5, relief="ridge")
        self.back_button.pack(pady=30)

        # Call the resize method immediately to adjust to the current window size
        self.after(100, lambda: self.resize_instructions_overlay(None))

        # Bind the resize event to adjust elements dynamically when the window is resized
        self.bind("<Configure>", self.resize_instructions_overlay)


    def resize_instructions_overlay(self, event):
        """Resize the elements in the instructions overlay dynamically."""

        # If event is None, use the current window size
        if event is None:
            new_width, new_height = self.instructions_overlay_frame.winfo_width(), self.instructions_overlay_frame.winfo_height()
        else:
            new_width, new_height = event.width, event.height

        # Get the top-level window (Tk window)
        top_level_window = self.winfo_toplevel()

        # Check if the window is in fullscreen mode
        if top_level_window.attributes('-fullscreen'):
            # Prevent resizing when the window is in fullscreen
            return

        # Define dynamic font sizes based on window height
        font_size = max(20, int(new_height / 25))  # Dynamic title font size
        small_font_size = max(12, int(new_height / 40))  # Dynamic instruction font size

        # Update the title label font size
        if self.overlay_label.winfo_exists():
            self.overlay_label.config(font=("Courier", font_size, "bold"))

        # Update the instruction labels font size
        if self.instruction1_label.winfo_exists():
            self.instruction1_label.config(font=("Courier", small_font_size, "bold"))
        if self.part1_label.winfo_exists():
            self.part1_label.config(font=("Courier", small_font_size, "bold"))
        if self.red_label.winfo_exists():
            self.red_label.config(font=("Courier", small_font_size, "bold"))
        if self.part2_label.winfo_exists():
            self.part2_label.config(font=("Courier", small_font_size, "bold"))
        if self.blue_label.winfo_exists():
            self.blue_label.config(font=("Courier", small_font_size, "bold"))
        if self.part4_label.winfo_exists():
            self.part4_label.config(font=("Courier", small_font_size, "bold"))
        if self.instruction4_label.winfo_exists():
            self.instruction4_label.config(font=("Courier", small_font_size, "bold"))
        if self.instruction4_label1.winfo_exists():
            self.instruction4_label1.config(font=("Courier", small_font_size, "bold"))
        if self.instruction5_part1_label.winfo_exists():
            self.instruction5_part1_label.config(font=("Courier", small_font_size, "bold"))
        if self.instruction5_part2_label.winfo_exists():
            self.instruction5_part2_label.config(font=("Courier", small_font_size, "bold"))
        if self.instruction6_label.winfo_exists():
            self.instruction6_label.config(font=("Courier", small_font_size, "bold"))

        # Update the back button font size if it exists
        if self.back_button.winfo_exists():
            self.back_button.config(font=("Courier", font_size - 12, "bold"))


    def hide_instructions_overlay(self):
        self.instructions_overlay_frame.destroy()
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Show the pause overlay again

    def show_overlay(self):
        if hasattr(self, 'instructions_overlay_frame'):
            self.instructions_overlay_frame.destroy()

        # Pause overlay
        self.overlay_frame = tk.Frame(self, bg="black")  # Retro black background
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Cover the whole game page
        self.overlay_frame.tkraise()

        # Create a container frame to hold all the elements and center them
        container = tk.Frame(self.overlay_frame, bg="black")  # Container with same retro background
        container.place(relx=0.5, rely=0.5, anchor="center")  # Center the container

        # Load and display the Game-Paused.png image (assuming it's a retro-style image)
        self.paused_image = tk.PhotoImage(file="Assets/Pictures/Game-Paused.png")
        paused_label = tk.Label(container, image=self.paused_image, bg="black")
        paused_label.pack(pady=30)  # Add some top padding

        # Define a fixed width for the buttons
        button_width = 20

        # Set retro font style (monospaced font, blocky look)
        retro_font = ("Courier", 20, "bold")

        # Resume button with retro styling
        resume_button = tk.Button(container, text="RESUME", command=self.app.play_with_sound(self.toggle_pause), font=retro_font, bg="lime", fg="black", width=button_width, bd=5, relief="ridge")
        resume_button.pack(padx=20, pady=20)

        # Instructions button with retro styling
        instruction_button = tk.Button(container, text="HOW TO PLAY", command=self.app.play_with_sound(self.show_instructions_overlay), font=retro_font, bg="cyan", fg="black", width=button_width, bd=5, relief="ridge")
        instruction_button.pack(padx=20, pady=20)

        # Main menu button with retro styling
        main_menu_button = tk.Button(container, text="MAIN MENU", command=self.app.play_with_sound(self.go_to_main_menu), font=retro_font, bg="red", fg="black", width=button_width, bd=5, relief="ridge")
        main_menu_button.pack(padx=20, pady=20)

        self.overlay_displayed = True


    def go_to_main_menu(self):
        # First confirmation dialog: Ask if the player is sure they want to go back to the main menu
        result = messagebox.askyesno("Confirm", "Are you sure you want to go back to the main menu?")
        
        if result:  # If the player clicks "Yes"
            # Second confirmation dialog: Ask if the player wants to save the game
            save_game = messagebox.askyesno("Save Game", "Do you want to save the game before exiting?")
            
            if save_game:  # If the player clicks "Yes" to save the game
                self.redirect_to_save_file()  # Call the function to save the game
            else:  # If the player clicks "No" to saving the game
                self.app.back_to_main_menu()  # Just go back to the main menu without saving

    def remove_overlay(self):
        self.overlay_frame.destroy()
        self.overlay_displayed = False

