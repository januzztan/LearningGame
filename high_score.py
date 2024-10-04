import tkinter as tk
from tkinter import messagebox

class HighScoreFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg="black")
        self.app = app
        self.file_path = "Assets/HighScoresList/saved_scores.txt"
        
        # Create GUI components
        self.create_widgets()
    
    def create_widgets(self):
        # Title Label with retro style
        title_label = tk.Label(
            self,
            text="High Scores",
            font=("Press Start 2P", 48),  # Increased font size for visibility
            fg="yellow",
            bg="black"
        )
        title_label.pack(pady=(30, 10))

        # Create a frame for the high score entries
        self.list_frame = tk.Frame(self, bg="black")  # Make this an instance variable
        self.list_frame.pack(pady=(10, 10), fill=tk.BOTH, expand=True)  # Fill available space
        
        # Header Labels with retro style
        self.create_header_labels()

        # Separator below headers
        separator = tk.Frame(self.list_frame, bg="white", height=2)
        separator.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="ew")
        
        # Configure weight for proper resizing
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(1, weight=2)
        self.list_frame.grid_columnconfigure(2, weight=1)
        
        # Load and display high scores (Top 5)
        self.display_high_scores()

        # Back Button
        back_button = tk.Button(
            self,
            text="Back to Main Menu",
            command=self.app.back_to_main_menu,
            font=("Press Start 2P", 24),  # Increased font size for button
            bg="red",
            fg="white",
            borderwidth=0,
            activebackground="darkred",
            activeforeground="white"
        )
        back_button.pack(pady=30)

    def create_header_labels(self):
        """Create header labels for the high score list."""
        header_rank = tk.Label(
            self.list_frame,
            text="Rank",
            font=("Press Start 2P", 36, "bold"),
            fg="yellow",
            bg="black",
            width=10
        )
        header_rank.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        header_name = tk.Label(
            self.list_frame,
            text="Name",
            font=("Press Start 2P", 36, "bold"),
            fg="yellow",
            bg="black",
            width=20
        )
        header_name.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        header_score = tk.Label(
            self.list_frame,
            text="Score",
            font=("Press Start 2P", 36, "bold"),
            fg="yellow",
            bg="black",
            width=10
        )
        header_score.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

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
                width=10,
                anchor="center"  # Center the text
            )
            rank_label.grid(row=idx + 1, column=0, padx=10, pady=5, sticky="ew")
        
            name_label = tk.Label(
                self.list_frame,
                text=name,
                font=("Press Start 2P", 30),  # Increased font size
                fg="white",
                bg="black",
                width=20,
                anchor="center"  # Center the text
            )
            name_label.grid(row=idx + 1, column=1, padx=10, pady=5, sticky="ew")
        
            score_label = tk.Label(
                self.list_frame,
                text=f"{score}",
                font=("Press Start 2P", 30),  # Increased font size
                fg="white",
                bg="black",
                width=10,
                anchor="center"  # Center the text
            )
            score_label.grid(row=idx + 1, column=2, padx=10, pady=5, sticky="ew")

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
            # If file doesn't exist, return an empty list
            high_scores = []
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading high scores:\n{e}")
            high_scores = []
        return high_scores
