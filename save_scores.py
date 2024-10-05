# save_scores.py

import tkinter as tk
from tkinter import messagebox
import os

class SaveScoreFrame(tk.Frame):
    def __init__(self, parent, score, back_to_main_menu, play_with_sound, refresh_high_scores, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.score = score
        self.back_to_main_menu = back_to_main_menu
        self.play_with_sound = play_with_sound
        self.refresh_high_scores = refresh_high_scores
        self.configure(bg="black")
        self.build_frame()
        self.bind_enter_key()
        self.configure_grid()
        self.after_id = None  # Initialize debounce identifier

    def configure_grid(self):
        """Configure grid weights to make the frame responsive."""
        self.grid_rowconfigure(0, weight=1)  # Top padding
        self.grid_rowconfigure(1, weight=1)  # Container
        self.grid_rowconfigure(2, weight=1)  # Bottom padding
        self.grid_columnconfigure(0, weight=1)  # Left padding
        self.grid_columnconfigure(1, weight=1)  # Container
        self.grid_columnconfigure(2, weight=1)  # Right padding

    def bind_enter_key(self):
        """Bind the Enter key to save actions."""
        self.master.bind("<Return>", self.save_score_event)

    def unbind_enter_key(self):
        """Unbind the Enter key when leaving the save page."""
        self.master.unbind("<Return>")

    def build_frame(self):
        # Create a container frame to center the content using grid
        container = tk.Frame(self, bg="black")
        container.grid(row=1, column=1, sticky="nsew")

        # Configure grid inside the container for responsiveness
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_rowconfigure(3, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=1)

        # Display score at the top of the window
        self.score_label = tk.Label(
            self,
            text=f"Score: {self.score}",
            font=("Courier", 28, "bold"),
            fg="white",
            bg="black"
        )
        self.score_label.grid(row=0, column=1, pady=(10, 10), sticky="n")

        # Retro-style label for the name entry
        self.name_label = tk.Label(
            container,
            text="ENTER NAME (1-3 CHARACTERS):",
            font=("Courier", 24, "bold"),
            fg="lime",
            bg="black"
        )
        self.name_label.grid(row=0, column=1, pady=(10, 5), sticky="n")

        # Entry widget for name input with validation
        vcmd = (self.register(self.validate_name), '%P')  # Validation command
        self.name_entry = tk.Entry(
            container,
            font=("Courier", 24, "bold"),
            fg="white",
            bg="gray",
            width=10,
            justify="center",
            validate="key",
            validatecommand=vcmd
        )
        self.name_entry.grid(row=1, column=1, pady=5, sticky="n")

        # Information label about name capitalization
        self.info_label = tk.Label(
            container,
            text="(All names will be saved in CAPS)",
            font=("Courier", 14, "bold"),
            fg="orange",
            bg="black"
        )
        self.info_label.grid(row=2, column=1, pady=5, sticky="n")

        # Save button with retro style
        self.save_button = tk.Button(
            container,
            text="SAVE",
            command=self.play_with_sound(self.save_score),
            font=("Courier", 16, "bold"),
            fg="yellow",
            bg="black",
            activebackground="gray",
            bd=5,
            relief="ridge",
            width=10
        )
        self.save_button.grid(row=3, column=1, pady=10, sticky="n")

        # Bind the resize event for dynamic font scaling
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Adjust font sizes based on window size with debounce."""
        if self.after_id:
            self.after_cancel(self.after_id)
        self.after_id = self.after(100, lambda: self.update_fonts(event))

    def update_fonts(self, event):
        """Update font sizes based on window size."""
        new_width = event.width
        new_height = event.height

        # Calculate a scaling factor based on width
        scale = new_width / 800  # Assuming 800 is the base width

        # Set minimum and maximum scaling factors
        scale = max(scale, 0.5)
        scale = min(scale, 2.0)

        # Update font sizes
        score_label_font = ("Courier", int(28 * scale), "bold")
        name_label_font = ("Courier", int(24 * scale), "bold")
        entry_font = ("Courier", int(24 * scale), "bold")
        info_label_font = ("Courier", int(14 * scale), "bold")
        button_font = ("Courier", int(16 * scale), "bold")

        # Update fonts
        self.score_label.config(font=score_label_font)
        self.name_label.config(font=name_label_font)
        self.name_entry.config(font=entry_font)
        self.info_label.config(font=info_label_font)
        self.save_button.config(font=button_font)

    def validate_name(self, P):
        """Validate that the entry has at most 3 characters."""
        if len(P) <= 3:
            return True
        else:
            return False

    def save_score_event(self, event):
        """Handle Enter key presses."""
        self.save_score()

    def save_score(self):
        name = self.name_entry.get().strip()

        # Validate name input: 1-3 characters
        if len(name) == 0:
            messagebox.showwarning("Invalid Entry", "Please enter a name with at least 1 character.")
            return
        elif len(name) > 3:
            messagebox.showerror("Invalid Entry", "Name cannot be more than 3 characters. Please re-enter.")
            return

        # Convert name to uppercase
        name = name.upper()

        # Ensure the directory for saving scores exists
        os.makedirs("Assets/HighScoresList", exist_ok=True)

        # Save the name and score to a text file
        try:
            with open(os.path.join("Assets", "HighScoresList", "saved_scores.txt"), "a") as file:
                file.write(f"{name} {self.score}\n")
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save score: {e}")
            return

        # Show a confirmation message
        messagebox.showinfo("Score Saved", "Your score has been saved successfully!")

        # Clear the entry field
        self.name_entry.delete(0, tk.END)

        # Refresh high scores
        self.refresh_high_scores()

        # Navigate back to the main menu
        self.back_to_main_menu()
