import tkinter as tk

# Functions to open different pages
def open_game_page():
    hide_main_page()
    game_page.pack()

def open_instruction_page():
    hide_main_page()
    instruction_page.pack()

def open_high_score_page():
    hide_main_page()
    high_score_page.pack()

def hide_main_page():
    main_frame.pack_forget()

def back_to_main_page():
    game_page.pack_forget()
    instruction_page.pack_forget()
    high_score_page.pack_forget()
    main_frame.pack()

# Main application window
root = tk.Tk()
root.title("Main Page")
root.geometry("400x300")

# Main frame
main_frame = tk.Frame(root)
main_frame.pack()

# Buttons on the main page with specific background colors
game_button = tk.Button(main_frame, text="Game", command=open_game_page, bg="green", fg="white")
instruction_button = tk.Button(main_frame, text="Instructions", command=open_instruction_page, bg="purple", fg="white")
high_score_button = tk.Button(main_frame, text="High Scores", command=open_high_score_page, bg="blue", fg="white")

game_button.pack(pady=10)
instruction_button.pack(pady=10)
high_score_button.pack(pady=10)

# Game Page
game_page = tk.Frame(root)
tk.Label(game_page, text="Game Page").pack()
back_button_game = tk.Button(game_page, text="Back to Main", command=back_to_main_page)
back_button_game.pack()

# Instruction Page
instruction_page = tk.Frame(root)
tk.Label(instruction_page, text="Instruction Page").pack()
back_button_instruction = tk.Button(instruction_page, text="Back to Main", command=back_to_main_page)
back_button_instruction.pack()

# High Score Page
high_score_page = tk.Frame(root)
tk.Label(high_score_page, text="High Score Page").pack()
back_button_high_score = tk.Button(high_score_page, text="Back to Main", command=back_to_main_page)
back_button_high_score.pack()

# Start the main loop
root.mainloop()
