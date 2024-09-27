import tkinter as tk
from tkinter import PhotoImage, messagebox
import pygame

class MainMenu(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg="black")
        self.app = app

        # Title image
        title_image = PhotoImage(file="Assets/Title.png")
        title_label = tk.Label(self, image=title_image, bg="black")
        title_label.image = title_image  # Keep a reference to avoid garbage collection
        title_label.pack(pady=150)

        # Music toggle button
        self.music_toggle_button = tk.Button(self, image=app.volume_play_image, command=app.play_with_sound(self.toggle_music), borderwidth=0, bg="black")
        self.music_toggle_button.place(relx=0.98, rely=0.02, anchor="ne")
        self.music_playing = True

        # Button frame for main menu buttons
        button_frame = tk.Frame(self, bg="black")
        button_frame.place(relx=0.5, rely=1.0, anchor="s")

        # Create buttons
        play_button = tk.Button(button_frame, image=app.play_btn_image, command=app.play_with_sound(app.switch_to_game_page), borderwidth=0, bg="lightgray")
        instruction_button = tk.Button(button_frame, image=app.instruction_btn_image, command=app.play_with_sound(app.switch_to_instruction_page), borderwidth=0, bg="lightgray")
        high_score_button = tk.Button(button_frame, image=app.high_score_btn_image, command=self.show_high_scores, borderwidth=0, bg="lightgray")

        play_button.pack(side=tk.LEFT, padx=40, pady=40)
        instruction_button.pack(side=tk.LEFT, padx=40, pady=40)
        high_score_button.pack(side=tk.LEFT, padx=40, pady=40)

    def toggle_music(self):
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_toggle_button.config(image=self.app.volume_mute_image)
        else:
            pygame.mixer.music.unpause()
            self.music_toggle_button.config(image=self.app.volume_play_image)
        self.music_playing = not self.music_playing

    def show_high_scores(self):
        # Placeholder for high score functionality
        messagebox.showinfo("High Scores", "High scores feature coming soon!")
