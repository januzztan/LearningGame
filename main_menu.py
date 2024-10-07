import tkinter as tk
from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
import pygame

class MainMenu(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg="black")
        self.app = app

        # Initialize pygame mixer
        pygame.mixer.init()

        # Split the screen into top (title) and bottom (GIF + buttons)
        self.top_frame = tk.Frame(self, bg="black")
        self.bottom_frame = tk.Frame(self, bg="black")

        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Prevent the frames from shrinking to fit the content
        self.top_frame.pack_propagate(False)
        self.bottom_frame.pack_propagate(False)

        # Load title image
        self.title_image_path = "Assets/Pictures/Title.png"
        self.title_label = tk.Label(self.top_frame, bg="black")
        self.title_label.pack(expand=True, fill=tk.BOTH)  # Fill the top half with the title

        # Store original button image paths
        self.play_btn_image_path = "Assets/Pictures/Start_btn.png"
        self.instruction_btn_image_path = "Assets/Pictures/Instruction_btn.png"
        self.high_score_btn_image_path = "Assets/Pictures/HighScore_btn.png"
        self.exit_btn_image_path = "Assets/Pictures/Exit.png"  # Exit button image path
        self.music_btn_play_image_path = "Assets/Pictures/Volume_Play.png"  # Music play image path
        self.music_btn_mute_image_path = "Assets/Pictures/Volume_Mute.png"  # Music mute image path

        # Load button images initially
        self.app.play_btn_image = PhotoImage(file=self.play_btn_image_path)
        self.app.instruction_btn_image = PhotoImage(file=self.instruction_btn_image_path)
        self.app.high_score_btn_image = PhotoImage(file=self.high_score_btn_image_path)

        # Load Exit button image
        self.exit_btn_image = PhotoImage(file=self.exit_btn_image_path)
        self.exit_button = tk.Button(
            self,
            image=self.exit_btn_image,
            command=self.app.play_with_sound(self.confirm_close),
            bg="black",
            borderwidth=0
        )
        self.exit_button.place(x=30, y=10)  # Initial placement

        # Load Music toggle button images
        self.volume_play_image = PhotoImage(file=self.music_btn_play_image_path)
        self.volume_mute_image = PhotoImage(file=self.music_btn_mute_image_path)
        self.music_toggle_button = tk.Button(
            self,
            image=self.volume_play_image,
            command=self.app.play_with_sound(self.toggle_music),
            borderwidth=0,
            bg="black"
        )
        self.music_toggle_button.place(relx=0.98, rely=0.02, anchor="ne")  # Initial placement
        self.music_playing = True

        # Load close prompt sound
        self.close_sound = pygame.mixer.Sound("Assets/SFX/Close_promt.mp3")  # Close prompt sound

        # Bottom Frame Content (GIF and Buttons)
        self.gif_frames = [PhotoImage(file="Assets/star.gif", format=f"gif -index {i}") for i in range(self.get_gif_frames("Assets/star.gif"))]
        self.gif_label = tk.Label(self.bottom_frame, bg="black")
        self.gif_label.pack(pady=0, expand=True)  # GIF in bottom frame

        self.animate_gif(0)  # Start GIF animation

        # Frame for main menu buttons (below the GIF)
        self.button_frame = tk.Frame(self.bottom_frame, bg="black")
        self.button_frame.pack(fill=tk.BOTH, pady=0, expand=True)  # Center buttons within the bottom frame

        # Create main menu buttons
        self.play_button = tk.Button(
            self.button_frame,
            image=self.app.play_btn_image,
            command=self.app.play_with_sound(lambda:app.switch_to_game_page()),
            borderwidth=0,
            bg="lightgray"
        )
        self.instruction_button = tk.Button(
            self.button_frame,
            image=self.app.instruction_btn_image,
            command=self.app.play_with_sound(lambda:app.switch_to_instruction_page()),
            borderwidth=0,
            bg="lightgray"
        )
        self.high_score_button = tk.Button(
            self.button_frame,
            image=self.app.high_score_btn_image,
            command=self.app.play_with_sound(lambda:app.switch_to_high_score_page()),
            borderwidth=0,
            bg="lightgray"
        )

        self.play_button.pack(side=tk.LEFT, padx=20, expand=True)  # Button alignment in bottom frame
        self.instruction_button.pack(side=tk.LEFT, padx=20, expand=True)
        self.high_score_button.pack(side=tk.LEFT, padx=20, expand=True)

        # Resize title image and GIF initially
        self.update_title_image()
        self.update_gif_frame_size()
        self.update_button_images()

        # Bind the resize event to the update methods with debouncing
        app.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Debounce the resize event to avoid lag."""
        if hasattr(self, 'resize_after_id'):
            self.after_cancel(self.resize_after_id)  # Cancel previous scheduled resize if it exists
        self.resize_after_id = self.after(200, self.perform_resize)  # 200 ms delay before resizing

    def perform_resize(self):
        """Perform the actual resizing of title image, GIF, and buttons."""
        if self.title_label.winfo_exists():  # Check if title_label still exists
            self.update_title_image()
        if self.gif_label.winfo_exists():  # Check if gif_label still exists
            self.update_gif_frame_size()  # Resize GIF frame
            self.animate_gif(0)  # Restart the GIF animation
        self.update_button_images()  # Resize main menu and other buttons
        # Exit and Music buttons are handled within update_button_images

    def fit_image_to_window(self, image_path, window_size):
        """Fit image to the given window size."""
        image = Image.open(image_path)
        image_width, image_height = image.size
        
        # Calculate the aspect ratio
        aspect_ratio = image_width / image_height
        
        # Get the window size
        window_width, window_height = window_size
        
        # Calculate new size keeping the aspect ratio
        if (window_width / window_height) > aspect_ratio:
            new_width = int(window_height * aspect_ratio)
            new_height = window_height
        else:
            new_width = window_width
            new_height = int(window_width / aspect_ratio)
        
        # Resize the image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    def update_title_image(self):
        """Update the title image to fit the window size."""
        window_width = self.app.root.winfo_width()
        window_height = self.app.root.winfo_height() // 2  # Title takes up half of the screen
        
        # Check if the window dimensions are valid
        if window_width > 0 and window_height > 0:
            new_image = self.fit_image_to_window(self.title_image_path, (window_width, window_height))
            self.title_label.config(image=new_image)
            self.title_label.image = new_image  # Keep a reference to avoid garbage collection

    def update_gif_frame_size(self):
        """Resize the GIF label to fit within the available space."""
        window_width = self.app.root.winfo_width()
        window_height = self.app.root.winfo_height() // 4  # Adjust GIF height as necessary
        
        # Resize the GIF label based on the calculated size
        self.gif_label.config(width=window_width, height=window_height)

    def update_button_images(self):
        """Resize the button images based on the current window size, keeping the aspect ratio."""
        window_width = self.app.root.winfo_width()
        window_height = self.app.root.winfo_height()

        # Ensure dimensions are valid before resizing
        if window_width > 0 and window_height > 0:
            button_width = int(window_width / 4)  # Each main button gets a quarter of the width

            # Make sure button width and height are valid (greater than 0)
            if button_width > 0:
                # Resize main menu buttons
                if self.play_button.winfo_exists() and self.instruction_button.winfo_exists() and self.high_score_button.winfo_exists():
                    
                    # Play Button
                    play_aspect_ratio = self.get_image_aspect_ratio(self.play_btn_image_path)
                    play_button_height = int(button_width / play_aspect_ratio)
                    if play_button_height > 0:
                        self.play_btn_image_resized = self.resize_image(self.play_btn_image_path, (button_width, play_button_height))
                        self.play_button.config(image=self.play_btn_image_resized)
                        self.play_button.image = self.play_btn_image_resized  # Keep a reference

                    # Instruction Button
                    instruction_aspect_ratio = self.get_image_aspect_ratio(self.instruction_btn_image_path)
                    instruction_button_height = int(button_width / instruction_aspect_ratio)
                    if instruction_button_height > 0:
                        self.instruction_btn_image_resized = self.resize_image(self.instruction_btn_image_path, (button_width, instruction_button_height))
                        self.instruction_button.config(image=self.instruction_btn_image_resized)
                        self.instruction_button.image = self.instruction_btn_image_resized  # Keep a reference

                    # High Score Button
                    high_score_aspect_ratio = self.get_image_aspect_ratio(self.high_score_btn_image_path)
                    high_score_button_height = int(button_width / high_score_aspect_ratio)
                    if high_score_button_height > 0:
                        self.high_score_btn_image_resized = self.resize_image(self.high_score_btn_image_path, (button_width, high_score_button_height))
                        self.high_score_button.config(image=self.high_score_btn_image_resized)
                        self.high_score_button.image = self.high_score_btn_image_resized  # Keep a reference

            # Resize Exit Button
            exit_button_size = int(window_width * 0.05)  # 5% of window width
            if exit_button_size > 0:
                self.exit_btn_image_resized = self.resize_image(self.exit_btn_image_path, (exit_button_size, exit_button_size))
                self.exit_button.config(image=self.exit_btn_image_resized)
                self.exit_button.image = self.exit_btn_image_resized  # Keep a reference

            # Resize Music Toggle Button
            music_button_size = int(window_width * 0.05)  # 5% of window width
            if music_button_size > 0:
                if self.music_playing:
                    music_image_path = self.music_btn_play_image_path
                else:
                    music_image_path = self.music_btn_mute_image_path
                self.music_btn_image_resized = self.resize_image(music_image_path, (music_button_size, music_button_size))
                self.music_toggle_button.config(image=self.music_btn_image_resized)
                self.music_toggle_button.image = self.music_btn_image_resized  # Keep a reference

    def get_image_aspect_ratio(self, image_path):
        """Return the aspect ratio of an image."""
        image = Image.open(image_path)
        return image.width / image.height

    def resize_image(self, image_path, size):
        """Resize an image to a given size (width, height)."""
        image = Image.open(image_path)
        resized_image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    def animate_gif(self, frame_index):
        """Animate GIF on the main menu."""
        frame = self.gif_frames[frame_index]
        self.gif_label.config(image=frame)
        next_frame_index = (frame_index + 1) % len(self.gif_frames)
        self.after(100, self.animate_gif, next_frame_index)

    def get_gif_frames(self, gif_path):
        """Return the number of frames in a GIF."""
        gif = Image.open(gif_path)
        return gif.n_frames

    def confirm_close(self):
        """Ask for confirmation before closing the game."""
        self.close_sound.play()  # Play close prompt sound
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit the game?"):
            self.app.root.quit()

    def toggle_music(self):
        """Toggle the background music on or off."""
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_toggle_button.config(image=self.app.volume_mute_image)
        else:
            pygame.mixer.music.unpause()
            self.music_toggle_button.config(image=self.app.volume_play_image)
        self.music_playing = not self.music_playing
        self.update_button_images()  # Update the music button image size after toggle
