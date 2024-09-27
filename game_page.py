import tkinter as tk
import random
import pygame

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
        
        self.word_list = load_words()

        self.back_to_main_page = back_to_main_page_callback  # Store the callback

        # GUI components for the game
        self.label = tk.Label(self, text="Press Start to begin!", font=("Helvetica", 40), bg="lightgray")
        self.label.pack(pady=(80,40))
        
        self.entry = tk.Entry(self, font=("Helvetica", 30), width=20)
        self.entry.pack(pady=20)
        
        self.submit_button = tk.Button(self, text="Submit", command=self.check_answer, font=("Helvetica", 24))
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
        self.pause_button = tk.Button(self, text="Pause", command=self.toggle_pause, font=("Helvetica", 24))
        self.pause_button.place(relx=0.98, rely=0.02, anchor="ne")  # Top-right corner

        # Bind the Return key to check the answer
        self.bind_all('<Return>', lambda event: self.check_answer())

    def start_game(self):
        print("Game started.")  # Debugging statement
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
            print("Asking a new question...")  # Debugging statement
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
        print(f"Generated math question: {question_text}")  # Debugging statement
        self.label.config(text=question_text)

    def generate_random_word_problem(self):
        word = random.choice(self.word_list)
        self.correct_answer = word
        question_text = f"Type the word: {word}"
        print(f"Generated word question: {question_text}")  # Debugging statement
        self.label.config(text=question_text)

    def check_answer(self):
        if not self.game_paused:
            user_input = self.entry.get()
            print(f"User input: {user_input}")  # Debugging statement
            if self.question_type == 'math':
                try:
                    if int(user_input) == self.correct_answer:
                        print("Correct answer for math question.")  # Debugging statement
                        self.correct_response()
                    else:
                        print("Incorrect answer for math question.")  # Debugging statement
                        self.incorrect_response()
                except ValueError:
                    print("Invalid input for math question.")  # Debugging statement
                    self.incorrect_response()
            else:
                if user_input.lower() == self.correct_answer.lower():
                    print("Correct answer for word question.")  # Debugging statement
                    self.correct_response()
                else:
                    print("Incorrect answer for word question.")  # Debugging statement
                    self.incorrect_response()

    def correct_response(self):
        print("Handling correct response.")  # Debugging statement
        self.play_sound('correct')
        self.points += 10
        self.points_label.config(text=f"Points: {self.points}")
        self.flash_green_tick()
        self.after(1000, self.ask_question)  # Use self.after instead of self.root.after

    def incorrect_response(self):
        print("Handling incorrect response.")  # Debugging statement
        self.play_sound('incorrect')
        self.flash_red_cross()
        self.after(1000, self.go_to_main_menu)  # Use self.after instead of self.app.root.after
    
    def go_to_main_menu(self):
        print("Returning to main menu.")  # Debugging statement
        self.back_to_main_page()

    def flash_red_cross(self):
        print("Flashing red cross.")  # Debugging statement
        self.cross_label.config(text="X")
        self.tick_label.config(text="")
        self.after(1000, lambda: self.cross_label.config(text=""))  # Use self.after

    def flash_green_tick(self):
        print("Flashing green tick.")  # Debugging statement
        self.tick_label.config(text="✓")
        self.cross_label.config(text="")
        self.after(1000, lambda: self.tick_label.config(text=""))  # Use self.after

    def play_sound(self, result):
        print(f"Playing sound for: {result}")  # Debugging statement
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
        print("Toggling pause state.")  # Debugging statement
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
            print("Removing instructions overlay.")  # Debugging statement
            self.instructions_overlay_frame.destroy()  # Destroy the instructions overlay if it exists

    def toggle_overlay(self):
        if self.overlay_displayed:
            self.remove_overlay()
        else:
            self.show_overlay()

    def show_instructions_overlay(self):
        print("Showing instructions overlay.")  # Debugging statement
        # Hide the pause overlay but keep it in memory to avoid state loss
        self.overlay_frame.place_forget()

        # Create the instructions overlay
        self.instructions_overlay_frame = tk.Frame(self, bg="gray")
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

        # Back button to return to the pause overlay
        back_button = tk.Button(self.instructions_overlay_frame, text="Back", command=self.hide_instructions_overlay, font=("Helvetica", 24), bg='gray', fg='white')
        back_button.pack(pady=30)

    def hide_instructions_overlay(self):
        print("Hiding instructions overlay.")  # Debugging statement
        self.instructions_overlay_frame.destroy()
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Show the pause overlay again

    # Adjust show_overlay to hide the instructions overlay if it exists
    def show_overlay(self):
        print("Showing pause overlay.")  # Debugging statement
        if hasattr(self, 'instructions_overlay_frame'):
            self.instructions_overlay_frame.destroy()

        # Pause overlay
        self.overlay_frame = tk.Frame(self, bg="GRAY")
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Cover the whole game page
        self.overlay_frame.tkraise()

        # Create overlay text
        overlay_label = tk.Label(self.overlay_frame, text="Game Paused", font=("Helvetica", 48), fg="YELLOW", bg="GRAY")
        overlay_label.pack(pady=30)  # Add some top padding

        # Resume button
        resume_button = tk.Button(self.overlay_frame, text="Resume Game", command=self.toggle_pause, font=("Helvetica", 24), bg="GREEN", fg="WHITE")
        resume_button.pack(padx=20, pady=20)

        # Instructions button
        instruction_button = tk.Button(self.overlay_frame, text="Show Instructions", command=self.show_instructions_overlay, font=("Helvetica", 24), bg="BLUE", fg="WHITE")
        instruction_button.pack(padx=20, pady=20)

        # Main menu button
        main_menu_button = tk.Button(self.overlay_frame, text="Main Menu", command=self.go_to_main_menu, font=("Helvetica", 24), bg="RED", fg="WHITE")
        main_menu_button.pack(padx=20, pady=20)

        self.overlay_displayed = True


    def remove_overlay(self):
        print("Removing pause overlay.")  # Debugging statement
        self.overlay_frame.destroy()
        self.overlay_displayed = False

