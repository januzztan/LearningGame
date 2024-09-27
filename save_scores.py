import tkinter as tk

def save_name_and_score(score, back_to_main_menu):
    save_window = tk.Tk()
    save_window.title("Save Name & Score")

    tk.Label(save_window, text="Enter your name (3 characters):", font=("Helvetica", 16)).pack(pady=10)
    
    name_entry = tk.Entry(save_window, font=("Helvetica", 16))
    name_entry.pack(pady=10)

    def save_score():
        name = name_entry.get()[:3]  # Take only the first 3 characters
        with open("Assets\HighScoresList\saved_scores.txt", "a") as file:
            file.write(f"{name}: {score}\n")
        save_window.destroy()  # Close the save window after saving
        back_to_main_menu()  # Call the callback to go back to the main menu

    save_button = tk.Button(save_window, text="Save", command=save_score, font=("Helvetica", 16))
    save_button.pack(pady=10)

    save_window.mainloop()

