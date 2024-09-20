import tkinter as tk
from tkinter import messagebox
import random
import pygame
import os

# Initialize pygame
pygame.mixer.init()

# Function to load words from an English dictionary file
def load_words():
    word_list = []

    try:
        # Assuming we have a word list file with one word per line
        with open("Assets/dictionary/words.txt", "r") as f:
            word_list = f.read().splitlines()
    except FileNotFoundError:
        # If the dictionary file is not found, use a fallback word list
        word_list = ['apple', 'banana', 'cat', 'dog', 'elephant']
    return word_list

# Game data
word_list = load_words()

# Main Game Class
class LearningGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Learning Game for Kids")
        self.root.geometry("1920x1080")  # Set window size to 1920x1080
        
        self.points = 0
        self.question_type = None  # Will hold 'math' or 'word'
        self.correct_answer = None
        
        # GUI components
        self.label = tk.Label(root, text="Press Start to begin!", font=("Helvetica", 40))  # Bigger font for larger screen
        self.label.pack(pady=40)
        
        self.entry = tk.Entry(root, font=("Helvetica", 30), width=20)  # Bigger input field
        self.entry.pack(pady=20)
        
        self.submit_button = tk.Button(root, text="Submit", command=self.check_answer, font=("Helvetica", 24))
        self.submit_button.pack(pady=20)
        
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game, font=("Helvetica", 24))
        self.start_button.pack(pady=20)
        
        self.points_label = tk.Label(root, text=f"Points: {self.points}", font=("Helvetica", 30))
        self.points_label.pack(pady=20)
        
        # Red cross and green tick labels (initially hidden)
        self.cross_label = tk.Label(root, text="", font=("Helvetica", 200), fg="red")
        self.cross_label.pack()  # Ensure the cross label is added to the layout
        
        self.tick_label = tk.Label(root, text="", font=("Helvetica", 200), fg="green")
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
        word = random.choice(word_list)
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
        self.play_sound('correct')
        self.points += 1
        self.points_label.config(text=f"Points: {self.points}")
        self.flash_green_tick()  # Flash the green tick for correct answers
        self.root.after(1000, self.ask_question)  # Wait 1 second and ask the next question
    
    def incorrect_response(self):
        self.play_sound('incorrect')
        self.flash_red_cross()  # Flash the red cross for incorrect answers
        self.root.after(1000, self.ask_question)  # Wait 1 second and ask the next question
    
    def flash_red_cross(self):
        self.cross_label.config(text="X")  # Show the red cross
        self.root.after(1000, lambda: self.cross_label.config(text=""))  # Hide the red cross after 1 second
    
    def flash_green_tick(self):
        self.tick_label.config(text="✓")  # Show the green tick
        self.root.after(1000, lambda: self.tick_label.config(text=""))  # Hide the green tick after 1 second
    
    def play_sound(self, result):
        if result == 'correct':
            pygame.mixer.Sound("Assets/correct.mp3").play()
        elif result == 'incorrect':
            pygame.mixer.Sound('Assets/incorrect.mp3').play()

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = LearningGame(root)
    root.mainloop()
