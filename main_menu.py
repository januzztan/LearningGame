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
        title_label.pack(pady=60)

        # Load close button image
        close_image = PhotoImage(file="Assets/Exit.png")

        # Close button (Using image instead of text)
        close_button = tk.Button(self, image=close_image, command=self.confirm_close, bg="black", borderwidth=0)
        close_button.image = close_image  # Keep a reference to avoid garbage collection
        close_button.place(x=30, y=33)  # Fixed coordinates to ensure visibility at the top-left corner

        # Load close prompt sound
        self.close_sound = pygame.mixer.Sound("Assets/Close_promt.mp3")  # Close prompt sound

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
        high_score_button = tk.Button(button_frame, image=app.high_score_btn_image, command=app.play_with_sound(app.switch_to_high_score_page), borderwidth=0, bg="lightgray")

        play_button.pack(side=tk.LEFT, padx=40, pady=40)
        instruction_button.pack(side=tk.LEFT, padx=40, pady=40)
        high_score_button.pack(side=tk.LEFT, padx=40, pady=40)

        # Load GIF and set up animation
        self.gif_frames = [PhotoImage(file="Assets/star.gif", format=f"gif -index {i}") for i in range(self.get_gif_frames("Assets/star.gif"))]
        self.gif_label = tk.Label(self, bg="black")
        self.gif_label.place(relx=0.5, rely=0.65, anchor="center")
        self.animate_gif(0)

    def get_gif_frames(self, file):
        """Return the number of frames in a GIF."""
        i = 0
        while True:
            try:
                PhotoImage(file=file, format=f"gif -index {i}")
            except:
                break
            i += 1
        return i

    def animate_gif(self, frame_index):
        """Update the GIF label to the next frame and loop it."""
        frame = self.gif_frames[frame_index]
        self.gif_label.config(image=frame)
        frame_index = (frame_index + 1) % len(self.gif_frames)  # Loop the frames
        self.after(100, self.animate_gif, frame_index)  # Adjust the delay (100 ms) for speed

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

    def confirm_close(self):
        """Play sound and show a confirmation dialog when the user clicks the close button."""
        self.close_sound.play()  # Play close prompt sound
        response = messagebox.askyesno("Quit Game", "Are you sure you want to close the game?")
        if response == 1:  # If the user clicks "Yes"
            self.app.root.quit()  # This will close the game
