import tkinter as tk
from tkinter import messagebox

# Function to show instructions in a pop-up
def show_instructions():
    instructions = """
    Here are the instructions:
    1. Complete the math challenge.
    2. Click on hints for help.
    3. Answer the science question correctly to proceed.
    """
    messagebox.showinfo("Instructions", instructions)

# Function to show a hint pop-up
def show_hint():
    hint = "Hint: Try breaking the problem into smaller parts!"
    messagebox.showinfo("Hint", hint)

# Function to simulate game progression
def next_level():
    if messagebox.askyesno("Next Level", "Do you want to go to the next level?"):
        messagebox.showinfo("Level", "Level 2: Science Quiz")
    else:
        messagebox.showinfo("Exit", "Exiting the game.")

# Main game window
root = tk.Tk()
root.title("In-Game Pop-ups Example")
root.geometry("400x200")

# Button to show instructions at the start
instructions_button = tk.Button(root, text="Show Instructions", command=show_instructions)
instructions_button.pack(pady=10)

# Button to show hints during the game
hint_button = tk.Button(root, text="Show Hint", command=show_hint)
hint_button.pack(pady=10)

# Button to simulate moving to the next level
next_button = tk.Button(root, text="Next Level", command=next_level)
next_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
