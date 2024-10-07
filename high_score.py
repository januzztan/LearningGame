import tkinter as tk
from tkinter import messagebox

class HighScoreFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg="black")
        self.app = app
        self.file_path = "Assets/HighScoresList/saved_scores.txt"
        
        # Create GUI components
        self.create_widgets()

        # Configure grid to ensure proper resizing
        self.configure_grid()

    def create_widgets(self):
        # Title Label with retro style
        title_label = tk.Label(
            self,
            text="High Scores",
            font=("Press Start 2P", 48),  # Increased font size for visibility
            fg="yellow",
            bg="black"
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky="nsew")  # Fill the space and center title

        # Create a frame for the high score entries
        self.list_frame = tk.Frame(self, bg="black")
        self.list_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")  # Fill the space

        # Header Labels with retro style
        self.create_header_labels()

        # Separator below headers
        separator = tk.Frame(self.list_frame, bg="white", height=2)
        separator.grid(row=1, column=0, columnspan=3, sticky="ew")
        
        # Load and display high scores (Top 5)
        self.display_high_scores()

        # Back Button
        back_button = tk.Button(
            self,
            text="Back to Main Menu",
            command=self.app.play_with_sound(self.app.back_to_main_menu),
            font=("Press Start 2P", 24),  # Increased font size for button
            bg="red",
            fg="white",
            borderwidth=0,
            activebackground="darkred",
            activeforeground="white"
        )
        back_button.grid(row=2, column=0, columnspan=3, pady=30)  # Center button

    def create_header_labels(self):
        """Create header labels for the high score list."""
        header_labels = [("Rank", 0), ("Name", 1), ("Score", 2)]
        for text, col in header_labels:
            label = tk.Label(
                self.list_frame,
                text=text,
                font=("Press Start 2P", 36, "bold"),
                fg="yellow",
                bg="black"
            )
            label.grid(row=0, column=col, sticky="nsew")

    def display_high_scores(self):
        """
        Load high scores from the text file and display them.
        """
        high_scores = self.load_high_scores()[:5]  # Only keep top 5 scores

        # Clear previous entries in the list_frame
        for widget in self.list_frame.winfo_children():
            widget.destroy()  # Clear all widgets in the list frame

        # Recreate header labels
        self.create_header_labels()

        # Display each high score
        for idx, (name, score) in enumerate(high_scores, start=1):
            rank_label = tk.Label(
                self.list_frame,
                text=f"{idx}",
                font=("Press Start 2P", 30),  # Increased font size
                fg="white",
                bg="black",
                anchor="center"  # Center the text
            )
            rank_label.grid(row=idx + 1, column=0, sticky="nsew")
        
            name_label = tk.Label(
                self.list_frame,
                text=name,
                font=("Press Start 2P", 30),  # Increased font size
                fg="white",
                bg="black",
                anchor="center"  # Center the text
            )
            name_label.grid(row=idx + 1, column=1, sticky="nsew")
        
            score_label = tk.Label(
                self.list_frame,
                text=f"{score}",
                font=("Press Start 2P", 30),  # Increased font size
                fg="white",
                bg="black",
                anchor="center"  # Center the text
            )
            score_label.grid(row=idx + 1, column=2, sticky="nsew")

    def load_high_scores(self):
        """
        Load high scores from a text file.
        Each line should contain a name and a score separated by a space.
        Example:
            Alice 150
            Bob 120
        """
        high_scores = []
        try:
            with open(self.file_path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) != 2:
                        continue  # Skip malformed lines
                    name, score = parts
                    high_scores.append((name, int(score)))
            # Sort high scores in descending order
            high_scores.sort(key=lambda x: x[1], reverse=True)
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", "No saved scores found. Please play the game to generate high scores.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading high scores:\n{e}")
        return high_scores

    def configure_grid(self):
        """Configure the grid layout for resizing."""
        # Set the weight for rows and columns
        self.grid_rowconfigure(0, weight=0)  # Title row
        self.grid_rowconfigure(1, weight=1)  # High score list row
        self.grid_rowconfigure(2, weight=0)  # Back button row

        # Make the main frame resizeable
        self.grid_columnconfigure(0, weight=1)  # Rank column
        self.grid_columnconfigure(1, weight=1)  # Name column
        self.grid_columnconfigure(2, weight=1)  # Score column

        # Allow list_frame to fill available space
        self.list_frame.grid_rowconfigure(0, weight=1)  # Header row
        self.list_frame.grid_rowconfigure(1, weight=1)  # Separator row
        self.list_frame.grid_rowconfigure(2, weight=1)  # Content rows for scores

        # Configure each row to have equal height and fill space
        for i in range(1, 6):  # Adjust for 5 high scores
            self.list_frame.grid_rowconfigure(i, weight=1)  # Give equal weight to each row

        # Configure columns of the list frame for resizing
        self.list_frame.grid_columnconfigure(0, weight=1)  # Rank column
        self.list_frame.grid_columnconfigure(1, weight=1)  # Name column
        self.list_frame.grid_columnconfigure(2, weight=1)  # Score column

