import tkinter as tk

class InstructionPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg="lightgray")
        self.app = app

        instruction_label = tk.Label(self, text="Instructions", font=("Helvetica", 40), bg="lightgray")
        instruction_label.pack(pady=50)

        instruction_text = """1. Press 'Start' to begin the game.
2. Answer the questions displayed.
3. Submit your answer using the 'Submit' button.
4. Points will be awarded for correct answers.
5. You can pause the game at any time.
6. To return to the main menu, use the appropriate button.
"""
        instruction_message = tk.Label(self, text=instruction_text, font=("Helvetica", 20), bg="lightgray", justify="left")
        instruction_message.pack(padx=50)

        back_button = tk.Button(self, text="Back to Main Menu", command=self.app.back_to_main_menu, font=("Helvetica", 24), bg="lightgray")
        back_button.pack(pady=20)
