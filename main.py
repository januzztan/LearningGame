import tkinter as tk
import pygame
from main_menu import MainMenu
from game_page import GamePage
from instruction_page import InstructionPage

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Page")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="lightgray")

        # Load images for buttons
        self.volume_play_image = tk.PhotoImage(file="Assets/Volume_play.png")
        self.volume_mute_image = tk.PhotoImage(file="Assets/Volume_mute.png")
        self.play_btn_image = tk.PhotoImage(file="Assets/Start_btn.png")
        self.instruction_btn_image = tk.PhotoImage(file="Assets/Instruction_btn.png")
        self.high_score_btn_image = tk.PhotoImage(file="Assets/HighScore_btn.png")

        # Initialize Pygame mixer for sounds
        pygame.mixer.init()
        pygame.mixer.music.load("Assets/BGM.mp3")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)

        self.click_sound = pygame.mixer.Sound("Assets/mouse_click.mp3")  # Load the click sound

        # Create the main menu page
        self.main_menu_page = MainMenu(self)

        # Initialize pages
        self.game_page = GamePage(self, self.back_to_main_menu)
        self.instruction_page = InstructionPage(self)

        # Bind the Escape key to exit fullscreen
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Show the main menu
        self.main_menu_page.pack(fill="both", expand=True)

    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode."""
        self.root.attributes('-fullscreen', False)
        self.root.state('zoomed')  # Make sure the window returns to normal state

    def switch_to_game_page(self):
        self.main_menu_page.pack_forget()
        self.game_page.pack(fill="both", expand=True)
        self.game_page.start_game()

    def switch_to_instruction_page(self):
        self.main_menu_page.pack_forget()
        self.instruction_page.pack(fill="both", expand=True)

    def back_to_main_menu(self):
        self.game_page.pack_forget()
        self.instruction_page.pack_forget()
        self.main_menu_page.pack(fill="both", expand=True)

    # Function to play click sound and execute command
    def play_with_sound(self, command):
        def wrapper():
            self.click_sound.play()  # Play click sound
            command()  # Execute the actual command
        return wrapper

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
