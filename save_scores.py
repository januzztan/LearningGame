import tkinter as tk
from tkinter import messagebox
import os

class SaveScoreFrame(tk.Frame):
    def __init__(self, parent, score, back_to_main_menu, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.score = score  # Store the score passed in
        self.back_to_main_menu = back_to_main_menu  # Callback to go back to the main menu
        self.build_frame()  # Call the function to build the frame layout

    def build_frame(self):
        # Create a label for the name entry
        tk.Label(self, text="Enter your name (3 characters max):", font=("Helvetica", 16)).pack(pady=10)

        # Create an entry widget for name input
        self.name_entry = tk.Entry(self, font=("Helvetica", 16))
        self.name_entry.pack(pady=10)

        # Create a button that will save the score
        save_button = tk.Button(self, text="Save", command=self.save_score, font=("Helvetica", 16))
        save_button.pack(pady=10)

    def save_score(self):
        name = self.name_entry.get().strip()  # Remove any leading/trailing spaces

        # Validate name input: It must be between 1 and 3 characters
        if len(name) == 0:
            messagebox.showwarning("Invalid Entry", "Please enter a name with at least 1 character.")
            return
        elif len(name) > 3:
            messagebox.showerror("Invalid Entry", "Name cannot be more than 3 characters. Please re-enter.")
            return

        # Ensure the directory for saving scores exists
        os.makedirs("Assets/HighScoresList", exist_ok=True)

        # Save the name and score to a text file
        with open(os.path.join("Assets", "HighScoresList", "saved_scores.txt"), "a") as file:
            file.write(f"{name} {self.score}\n")

        # Show a confirmation message once the score is saved
        messagebox.showinfo("Score Saved", "Your score has been saved successfully!")

        # Call the callback to go back to the main menu
        self.back_to_main_menu()
