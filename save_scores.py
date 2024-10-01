import tkinter as tk
from tkinter import messagebox
import os

class SaveScoreFrame(tk.Frame):
    def __init__(self, parent, score, back_to_main_menu, play_with_sound, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.score = score  # Store the score passed in
        self.back_to_main_menu = back_to_main_menu  # Callback to go back to the main menu
        self.play_with_sound = play_with_sound  # Reference to play_with_sound function from MainApplication
        self.build_frame()  # Call the function to build the frame layout

    def bind_enter_key(self):
        """Bind the Enter key to save actions."""
        self.master.bind("<Return>",  self.save_score_event)

    def unbind_enter_key(self):
        """Unbind the Enter key when leaving the save page."""
        self.master.unbind("<Return>")

    def build_frame(self):
        # Create a label for the name entry
        tk.Label(self, text="Enter your name (3 characters max):", font=("Helvetica", 16)).pack(pady=10)

        # Create an entry widget for name input
        self.name_entry = tk.Entry(self, font=("Helvetica", 16))
        self.name_entry.pack(pady=10)

        # Create a button that will save the score with sound
        save_button = tk.Button(self, text="Save", command=self.play_with_sound(self.save_score), font=("Helvetica", 16))
        save_button.pack(pady=10)

    def save_score_event(self, event):
        """This method will handle Enter key presses"""
        self.save_score()  # Call save_score method when Enter key is pressed

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
