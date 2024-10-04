import tkinter as tk
from tkinter import PhotoImage
import random
import pygame
import tkinter.messagebox as messagebox  # Import the messagebox module
from PIL import Image, ImageTk

class GamePage(tk.Frame):
    def __init__(self, app, back_to_main_page_callback):
        # Get easy words from words.txt file
        def load_words():
            word_list = []
            try:
                with open("Assets/dictionary/words.txt", "r") as f:
                    word_list = f.read().splitlines()
            # Fall back words if file is unable to open
            except FileNotFoundError:
                word_list = ['apple', 'banana', 'cat', 'dog', 'elephant']
            return word_list
        
        # Get hard words from hard_words.txt file
        def load_hard_words():
            word_list = []
            try:
                with open("Assets/dictionary/hard_words.txt", "r") as f:
                    word_list = f.read().splitlines()
            # Fall back words if file is unable to open
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

         # Load click sound
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("Assets/SFX/mouse_click.mp3")  # Ensure correct path to the click sound file
        
        # Load words
        self.word_list = load_words()
        self.hard_word_list = load_hard_words()

        # Store callback to mainpage
        self.back_to_main_page = back_to_main_page_callback

        # Load pause image
        self.pause_image = PhotoImage(file="Assets/Pictures/Pause_btn.png")

        # Load heart images
        self.heart_full_image = PhotoImage(file="Assets/Pictures/heart_full.png")
        self.heart_empty_image = PhotoImage(file="Assets/Pictures/heart_empty.png")

        # Load cross and tick images
        self.cross_image = PhotoImage(file="Assets/Pictures/cross.png")
        self.tick_image = PhotoImage(file="Assets/Pictures/tick.png")

        # Configure grid weights for resizing
        self.grid_rowconfigure(0, weight=0)  # Timer, points, and pause row
        self.grid_rowconfigure(1, weight=1)  # Question frame row (resizable)
        self.grid_rowconfigure(2, weight=0)  # Input frame row (fixed)
        self.grid_rowconfigure(3, weight=0)  # Feedback row (fixed)
        self.grid_rowconfigure(4, weight=0)  # Lives row
        self.grid_columnconfigure(0, weight=1)  # Timer column
        self.grid_columnconfigure(1, weight=1)  # Hearts column
        self.grid_columnconfigure(2, weight=1)  # Points and pause column

        # Timer Label on the left
        self.timer_label = tk.Label(self, text=f"Time Left: {self.timer}s", font=("Courier", 24, "bold"), fg="white", bg="black")
        self.timer_label.grid(row=0, column=0, sticky="nw", padx=(10, 0))

        # Points label and pause button on the right
        self.points_label = tk.Label(self, text=f"Points: {self.points}", font=("Courier", 24, "bold"), bg="black", fg="white")
        self.points_label.grid(row=0, column=2, sticky="ne", padx=(0, 10))

        # Pause Button on the right
        self.pause_button = tk.Button(self, image=self.pause_image, command=app.play_with_sound(self.toggle_pause), bg="black", borderwidth=0)
        self.pause_button.image = self.pause_image  # Keep a reference to avoid garbage collection
        self.pause_button.grid(row=0, column=2, sticky="nse", padx=(0, 10))

        # Create a frame for the hearts in the center column
        self.lives_frame = tk.Frame(self, bg="black")
        self.lives_frame.grid(row=4, column=1, sticky="nsew")  # Lives row in center column
        self.lives_labels = []  # Store heart image labels in list
        for i in range(3):
            label = tk.Label(self.lives_frame, image=self.heart_full_image, bg="black")
            label.pack(side="left", padx=10)
            self.lives_labels.append(label)

        # Create a frame for the question label
        self.question_frame = tk.Frame(self, bg="black")
        self.question_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")  # Make it span across columns

        # Question label inside the frame
        self.label = tk.Label(self.question_frame, font=("Courier", 80, "bold"), bg="black", fg="white")
        self.label.pack(expand=True)  # Use pack to center the label

        # Configure the question frame to resize
        self.question_frame.grid_rowconfigure(0, weight=1)  # Allow the question frame to resize
        self.question_frame.grid_columnconfigure(0, weight=1)  # Center the question label within the frame

        # Frame to hold the entry box and submit button side by side
        self.input_frame = tk.Frame(self, bg="black")
        self.input_frame.grid(row=2, column=1, sticky="nsew")  # Center the input frame in the middle column

        # Entry box
        self.entry = tk.Entry(self.input_frame, font=("Courier", 30, "bold"), width=25, justify="center")
        self.entry.grid(row=0, column=0, padx=10, ipady=10)

        # Submit button beside entry box
        self.submit_button = tk.Button(self.input_frame, text="Submit", command=app.play_with_sound(self.check_answer), font=("Courier", 24, "bold"))
        self.submit_button.grid(row=0, column=1, padx=10)

        # Frame to hold the feedback graphics
        self.feedback_frame = tk.Frame(self, bg="black")
        self.feedback_frame.grid(row=3, column=1, sticky="nsew")  # Feedback row in center column

        # Cross graphic
        self.cross_label = tk.Label(self.feedback_frame, image="", bg="black")
        self.cross_label.pack(side="left")

        # Tick graphic
        self.tick_label = tk.Label(self.feedback_frame, image="", bg="black")
        self.tick_label.pack(side="left")

        # Ensure the feedback graphics and hearts are also centered
        self.feedback_frame.grid_rowconfigure(0, weight=1)
        self.feedback_frame.grid_columnconfigure(0, weight=1)

        self.lives_frame.grid_rowconfigure(0, weight=1)

    # Bind the Enter key to game actions
    def bind_enter_key(self):
        self.app.root.bind("<Return>", lambda event: self.check_answer())

    # Unbind the Enter key when leaving the game
    def unbind_enter_key(self):
        self.app.root.unbind("<Return>")

    #starts game
    def start_game(self):
        self.reset_game_state()
        self.ask_question()

    def reset_game_state(self):
        self.game_paused = False
        self.overlay_displayed = False
        self.points = 0
        self.points_label.config(text=f"Points: {self.points}")
        self.lives = 3  # Reset lives to 3
        self.timer = 21  # Reset timer to 20 seconds
        self.pause_button.config(text="Pause")
        self.timer_label.config(text=f"Time Left: {self.timer}s")  # Update timer display
        
        # Update heart images to full hearts (since lives are reset to 3)
        self.update_lives_display()

        # Remove the overlay if it's displayed
        if hasattr(self, 'overlay_frame'):
            self.overlay_frame.destroy()

        # Reset points and other game variables
        # Removed the second ask_question() here
        self.ask_question()  # Only need to ask the question once after resetting




    #generates new questions
    def ask_question(self):
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

    #Round countdown timer, 20 secs per question
    def countdown_timer(self):
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
        if self.points >= 200:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            op = random.choice(['+', '-', 'x', '/'])
            if op == '/':
                # Ensure a is a multiple of b for integer division
                b = random.randint(1, 10)  # Ensure b is at least 1
                a = b * random.randint(1, 10)  # Ensure a is a multiple of b
        # Easier questions for scores below 100
        else:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            op = random.choice(['+', '-'])

        if op == '+':
            self.correct_answer = a + b
        elif op == '-':
            if a < b: # Makes sure there are - qns that result in - ve answer
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
        if self.points >= 200:
            word = random.choice(self.hard_word_list)
        else:
            word = random.choice(self.word_list)
        self.correct_answer = word
        question_text = f"Type the word: {word}"
        self.label.config(text=question_text)

    # Check response from player
    def check_answer(self):
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
        self.play_sound('correct')
        self.points += 10
        self.points_label.config(text=f"Points: {self.points}")
        self.flash_green_tick()
        self.after(1000, self.ask_question)  # Use self.after instead of self.root.after

    # Wrong response
    def incorrect_response(self):
        self.play_sound('incorrect')
        self.flash_red_cross()

    # Lose life
    def lose_life(self):
        if not self.game_paused:  # Prevent life loss if the game is paused
            self.lives -= 1
            self.update_lives_display()
            if self.lives <= 0: # Show game over when lives reach 0
                self.show_game_over_overlay()
            else: # Move on to the next question after 1 second
                self.after(1000, self.ask_question) 

    # Change lives displayed
    def update_lives_display(self):
        for i in range(3):
            if i < self.lives:
                self.lives_labels[i].config(image=self.heart_full_image)
            else:
                self.lives_labels[i].config(image=self.heart_empty_image)

    # Game over overlay and Ending of game
    def show_game_over_overlay(self):
        # Stop the countdown timer if it's still running
        self.after_cancel(self.timer_callback_id)
        
        # Pauses game instance
        self.game_paused = True

        # Stop the global background music
        pygame.mixer.music.pause()

        # Play "game over" sound and get the sound length
        gameover_sound = pygame.mixer.Sound('Assets/SFX/gameover_sfx.mp3')
        gameover_sound.play()
        sound_length = gameover_sound.get_length()  # Get the duration of the sound

        # Create a "Game Over" overlay
        self.overlay_frame = tk.Frame(self, bg="black")
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Cover the whole game page
        self.overlay_frame.tkraise()

        # Load and display an image instead of the "Game Over" text
        img = Image.open("Assets/Pictures/GameOver.png")  # Make sure this image exists in your working directory
        img = img.resize((400, 400))  # Resize image to fit nicely
        img_tk = ImageTk.PhotoImage(img)

        game_over_image_label = tk.Label(self.overlay_frame, image=img_tk, bg="black")
        game_over_image_label.image = img_tk  # Keep a reference to avoid garbage collection

         # Center the image in the frame
        game_over_image_label.pack(expand=True)  # Expands the label to fill available space
        game_over_image_label.pack(anchor="center")  # Center the image

        # Delay before redirecting to save game state or exit
        self.after(int(sound_length * 1000), self.redirect_to_save_file)  # Wait the length of the gameover sound

    # Moves to save score page
    def redirect_to_save_file(self):
        # Resume the global background music
        self.unbind_enter_key()
        pygame.mixer.music.unpause()  # Resume the paused background music

        # Call the save score method from save_scores.py
        self.app.show_save_score_page(self.points)

    # Flash red cross with wrong response
    def flash_red_cross(self):
        self.cross_label.config(image=self.cross_image)
        self.tick_label.config(image="")  # Clear the cross image
        self.after(1000, lambda: self.cross_label.config(image=""))  # Hide after 1 second

    # Flash green tick with correct response
    def flash_green_tick(self):
        self.tick_label.config(image=self.tick_image)
        self.cross_label.config(image="")  # Clear the tick image
        self.after(1000, lambda: self.tick_label.config(image=""))  # Hide after 1 second

    # Play correct and incorrect sound with reponse
    def play_sound(self, result):
        try:
            if result == 'correct':
                pygame.mixer.Sound("Assets/SFX/correct.mp3").play()
            elif result == 'incorrect':
                pygame.mixer.Sound('Assets/SFX/incorrect.mp3').play()
        except pygame.error as e:
            print(f"Pygame sound error: {e}")  # Debugging statement
    
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

    def show_instructions_overlay(self):
        # Hide the pause overlay but keep it in memory to avoid state loss
        self.overlay_frame.place_forget()

        # Create the instructions overlay with retro black background
        self.instructions_overlay_frame = tk.Frame(self, bg="black")
        self.instructions_overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Cover the whole game page
        self.instructions_overlay_frame.tkraise()  # Ensure the overlay is on top of everything

        # Retro-style Title
        overlay_label = tk.Label(self.instructions_overlay_frame, text="HOW TO PLAY", font=("Courier", 40, "bold"), fg="lime", bg="black")
        overlay_label.pack(pady=30)  # Top padding for the title

        # Padding and font settings
        x_offset = 50  # Padding from the left side
        small_font = ("Courier", 24, "bold")  # Smaller retro font size for instructions

        # Instruction 1 (simple, one line)
        instruction1_label = tk.Label(self.instructions_overlay_frame, text="1. YOU START WITH 3 LIVES AND 0 POINTS.", font=small_font, fg="white", bg="black")
        instruction1_label.pack(anchor="w", padx=x_offset)  # Left aligned with padding

        # Instruction 2 with "RED" highlighted
        part1_label = tk.Label(self.instructions_overlay_frame, text="2. IF YOU SEE:", font=small_font, fg="white", bg="black")
        part1_label.pack(anchor="w", padx=x_offset)

        # RED instruction in one line
        instruction2_frame = tk.Frame(self.instructions_overlay_frame, bg="black")
        instruction2_frame.pack(anchor="w", padx=x_offset+30, pady=10)  # Left aligned, same line

        red_label = tk.Label(instruction2_frame, text="RED", font=small_font, fg="red", bg="black")
        red_label.pack(side=tk.LEFT)

        part2_label = tk.Label(instruction2_frame, text="WORDS, TYPE THEM EXACTLY.", font=small_font, fg="white", bg="black")
        part2_label.pack(side=tk.LEFT)

        # Instruction 3 with "BLUE" highlighted
        instruction3_frame = tk.Frame(self.instructions_overlay_frame, bg="black")
        instruction3_frame.pack(anchor="w", padx=x_offset+30, pady=10)  # Left aligned, same line

        blue_label = tk.Label(instruction3_frame, text="BLUE", font=small_font, fg="cyan", bg="black")
        blue_label.pack(side=tk.LEFT)

        part4_label = tk.Label(instruction3_frame, text="WORDS, SOLVE THE MATH.", font=small_font, fg="white", bg="black")
        part4_label.pack(side=tk.LEFT)

        # Instruction 4
        instruction4_label = tk.Label(self.instructions_overlay_frame, text="3. GET IT RIGHT:", font=small_font, fg="white", bg="black")
        instruction4_label.pack(anchor="w", padx=x_offset, pady=10)  # Left aligned with padding

        instruction4_label1 = tk.Label(self.instructions_overlay_frame, text="YOU GET 10 POINTS!", font=small_font, fg="lime", bg="black")
        instruction4_label1.pack(anchor="w", padx=x_offset+30, pady=10)  # Left aligned with padding

        # Instruction 5
        instruction5_frame = tk.Frame(self.instructions_overlay_frame, bg="black")
        instruction5_frame.pack(anchor="w", padx=x_offset, pady=10)

        instruction5_part1_label = tk.Label(instruction5_frame, text="4. GET IT WRONG OR TAKE TOO LONG:", font=small_font, fg="white", bg="black")
        instruction5_part1_label.pack(side=tk.LEFT)

        instruction5_part2_label = tk.Label(self.instructions_overlay_frame, text="YOU LOSE 1 LIFE.", font=small_font, fg="red", bg="black")
        instruction5_part2_label.pack(anchor="w", padx=x_offset+30, pady=10)

        # Final instruction (simple, on one line)
        instruction6_label = tk.Label(self.instructions_overlay_frame, text="5. LOSE ALL 3 LIVES, GAME ENDS.", font=small_font, fg="white", bg="black")
        instruction6_label.pack(anchor="w", padx=x_offset, pady=10)

        # Retro-style Back button
        back_button = tk.Button(self.instructions_overlay_frame, text="BACK", command=self.app.play_with_sound(self.hide_instructions_overlay), font=("Courier", 28, "bold"), bg="gray", fg="black", width=10, bd=5, relief="ridge")
        back_button.pack(pady=30)


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

