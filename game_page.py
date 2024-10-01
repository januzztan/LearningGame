import tkinter as tk
import random
import pygame
import tkinter.messagebox as messagebox  # Import the messagebox module
from PIL import Image, ImageTk

class GamePage(tk.Frame):
    def __init__(self, app, back_to_main_page_callback):
        def load_words():
            word_list = []
            try:
                with open("Assets/dictionary/words.txt", "r") as f:
                    word_list = f.read().splitlines()
            except FileNotFoundError:
                word_list = ['apple', 'banana', 'cat', 'dog', 'elephant']
            return word_list
        
        super().__init__(app.root, bg="lightgray")
        self.app = app
        self.points = 0
        self.question_type = None
        self.correct_answer = None
        self.game_paused = False
        self.overlay_displayed = False

         # Load click sound
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("Assets/mouse_click.mp3")  # Ensure correct path to the click sound file
        
        self.word_list = load_words()

        self.back_to_main_page = back_to_main_page_callback  # Store the callback

        # GUI components for the game
        self.label = tk.Label(self, text="Press Start to begin!", font=("Helvetica", 40), bg="lightgray")
        self.label.pack(pady=(80,40))
        
        self.entry = tk.Entry(self, font=("Helvetica", 30), width=20)
        self.entry.pack(pady=20)
        
        self.submit_button = tk.Button(self, text="Submit", command=app.play_with_sound(self.check_answer), font=("Helvetica", 24))
        self.submit_button.pack(pady=20)
        
        self.points_label = tk.Label(self, text=f"Points: {self.points}", font=("Helvetica", 30), bg="lightgray")
        self.points_label.pack(pady=20)

        self.feedback_frame = tk.Frame(self, bg="lightgray")
        self.feedback_frame.pack(pady=20)

        self.cross_label = tk.Label(self.feedback_frame, text="", font=("Helvetica", 200), fg="red", bg="lightgray")
        self.cross_label.grid(row=0, column=0)

        self.tick_label = tk.Label(self.feedback_frame, text="", font=("Helvetica", 200), fg="green", bg="lightgray")
        self.tick_label.grid(row=0, column=0)

        # Add Pause/Unpause button
        self.pause_button = tk.Button(self, text="Pause", command=app.play_with_sound(self.toggle_pause), font=("Helvetica", 24))
        self.pause_button.place(relx=0.98, rely=0.02, anchor="ne")  # Top-right corner

    def bind_enter_key(self):
        """Bind the Enter key to game actions."""
        self.app.root.bind("<Return>", lambda event: self.check_answer())

    def unbind_enter_key(self):
        """Unbind the Enter key when leaving the game."""
        self.app.root.unbind("<Return>")


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
        else:
            print("Game is paused. Cannot ask a question.")  # Debugging statement

    def generate_random_math_problem(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-'])
        if op == '+':
            self.correct_answer = a + b
        else:
            self.correct_answer = a - b
        question_text = f"What is {a} {op} {b}?"
        self.label.config(text=question_text)

    def generate_random_word_problem(self):
        word = random.choice(self.word_list)
        self.correct_answer = word
        question_text = f"Type the word: {word}"
        self.label.config(text=question_text)

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
        self.after(1000, self.ask_question)  # Use self.after instead of self.root.after

    def incorrect_response(self):
        self.play_sound('incorrect')
        self.flash_red_cross()

        # Show Game Over overlay before redirecting
        self.after(1000, self.show_game_over_overlay)

    def show_game_over_overlay(self):
        # Stop the global background music
        pygame.mixer.music.pause()  # Pause the background music

        # Play "game over" sound and get the sound length
        gameover_sound = pygame.mixer.Sound('Assets/gameover_sfx.mp3')
        gameover_sound.play()
        sound_length = gameover_sound.get_length()  # Get the duration of the sound

        # Create a "Game Over" overlay
        self.overlay_frame = tk.Frame(self, bg="black")
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Cover the whole game page
        self.overlay_frame.tkraise()

        # Load and display an image instead of the "Game Over" text
        img = Image.open("Assets/GameOver.png")  # Make sure this image exists in your working directory
        img = img.resize((400, 400))  # Resize image to fit nicely
        img_tk = ImageTk.PhotoImage(img)

        game_over_image_label = tk.Label(self.overlay_frame, image=img_tk, bg="black")
        game_over_image_label.image = img_tk  # Keep a reference to avoid garbage collection

         # Center the image in the frame
        game_over_image_label.pack(expand=True)  # Expands the label to fill available space
        game_over_image_label.pack(anchor="center")  # Center the image

        # Delay before redirecting to save game state or exit
        self.after(int(sound_length * 1000), self.redirect_to_save_file)  # Wait the length of the gameover sound


    def redirect_to_save_file(self):
        # Resume the global background music
        self.unbind_enter_key()
        pygame.mixer.music.unpause()  # Resume the paused background music

        # Call the save score method from save_scores.py
        self.after(2000, lambda: self.app.show_save_score_page(self.points))


    def flash_red_cross(self):
        self.cross_label.config(text="X")
        self.tick_label.config(text="")
        self.after(1000, lambda: self.cross_label.config(text=""))  # Use self.after

    def flash_green_tick(self):
        self.tick_label.config(text="✓")
        self.cross_label.config(text="")
        self.after(1000, lambda: self.tick_label.config(text=""))  # Use self.after

    def play_sound(self, result):
        try:
            if result == 'correct':
                pygame.mixer.Sound("Assets/correct.mp3").play()
            elif result == 'incorrect':
                pygame.mixer.Sound('Assets/incorrect.mp3').play()
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
        self.paused_image = tk.PhotoImage(file="Assets/Game-Paused.png")
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

