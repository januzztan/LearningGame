import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import os
from collections import OrderedDict

class InstructionPage(tk.Frame):
    """
    A Tkinter Frame subclass that displays instructional pages with images and navigation buttons.
    It supports dynamic resizing, image caching, and error handling for robust performance.
    """

    # Maximum number of cached resized images and PhotoImages
    MAX_RESIZED_CACHE = 100
    MAX_TK_CACHE = 100

    def __init__(self, parent, controller):
        """
        Initialize the InstructionPage frame.

        Args:
            parent (tk.Widget): The parent widget.
            controller (object): The controller managing navigation and sound playback.
        """
        super().__init__(parent)
        self.controller = controller

        # Initialize pygame mixer for sound playback
        pygame.mixer.init()

        # Set the background to black
        self.configure(bg="black")

        # Dynamically construct image paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_directory = os.path.join(script_dir, "Assets", "Pictures")
        image_paths = {
            1: os.path.join(image_directory, "Inst_How2Play.png"),
            2: os.path.join(image_directory, "Inst_LivesNPoints.png"),
            3: os.path.join(image_directory, "Inst_Tips2Succeed.png")
        }

        # Load the images with error handling
        self.original_images = {}
        for key, path in image_paths.items():
            if os.path.exists(path):
                try:
                    self.original_images[key] = Image.open(path)
                except Exception as e:
                    messagebox.showerror("Image Load Error", f"Failed to load image '{path}': {e}")
                    self.original_images[key] = None  # Assign None to indicate loading failure
            else:
                messagebox.showerror("Image Not Found", f"Image file not found: '{path}'")
                self.original_images[key] = None  # Assign None to indicate missing image

        # Initialize caches as OrderedDicts for LRU functionality
        self.resized_images_cache = OrderedDict()
        self.tk_images_cache = OrderedDict()

        # Get image size and aspect ratio from the first available image
        available_images = [img for img in self.original_images.values() if img is not None]
        if available_images:
            self.image_width, self.image_height = available_images[0].size
            self.aspect_ratio = self.image_height / self.image_width  # Height / Width
        else:
            self.image_width, self.image_height = 800, 600  # Default size if no images are loaded
            self.aspect_ratio = 0.75

        self.current_page = 1  # Track current page
        self.is_resizing = False  # Track if the window is currently resizing
        self.previous_size = (0, 0)  # Store previous window size for optimization

        # Determine the appropriate resampling method
        try:
            resample_method = Image.Resampling.LANCZOS
        except AttributeError:
            resample_method = Image.ANTIALIAS  # For older Pillow versions
        self.resample_method = resample_method

        # Create main layout frame
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Create widgets
        self.create_widgets()

        # Resize elements immediately after initialization
        self.update_idletasks()  # Ensure widgets are rendered before resizing
        self.show_page(1)  # Always start on page one

        # Bind the configure event to handle window resizing
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        """Create and layout all widgets within the main frame."""
        # Set grid weights for the main frame
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Image should expand
        self.main_frame.grid_rowconfigure(2, weight=0)  # Buttons should not expand vertically
        self.main_frame.grid_columnconfigure(0, weight=1)  # Whole layout should expand horizontally

        # Page title
        self.title_label = tk.Label(
            self.main_frame,
            text="How to play?",
            font=("Courier", 60, "bold"),
            fg="white",
            bg="black"
        )
        self.title_label.grid(row=0, column=0, sticky="nsew")

        # Image display
        self.image_label = tk.Label(self.main_frame, bg="black")
        self.image_label.grid(row=1, column=0, sticky="nsew")

        # Navigation buttons frame
        self.button_frame = tk.Frame(self.main_frame, bg="black")
        self.button_frame.grid(row=2, column=0, pady=(0, 10), sticky="nsew")

        # Set grid column weights for button resizing
        for col in range(4):
            self.button_frame.grid_columnconfigure(col, weight=1)

        # Initial button font
        self.button_font = ("Courier", 24, "bold")

        # Navigation buttons and their original colors
        self.button_colors = {
            1: "purple",
            2: "orange",
            3: "green",
            4: "blue"
        }

        # How to Play Button
        self.how_to_play_button = tk.Button(
            self.button_frame,
            text="How to Play",
            font=self.button_font,
            bg=self.button_colors[1],
            fg="white",
            command=self.controller.play_with_sound(lambda: self.show_page(1))
        )
        self.how_to_play_button.grid(row=0, column=0, sticky="ew", padx=10)

        # Lives and Points Button
        self.lives_and_points_button = tk.Button(
            self.button_frame,
            text="Lives and Points",
            font=self.button_font,
            bg=self.button_colors[2],
            fg="white",
            command=self.controller.play_with_sound(lambda: self.show_page(2))
        )
        self.lives_and_points_button.grid(row=0, column=1, sticky="ew", padx=10)

        # Tips to Succeed Button
        self.tips_button = tk.Button(
            self.button_frame,
            text="Tips to Succeed",
            font=self.button_font,
            bg=self.button_colors[3],
            fg="white",
            command=self.controller.play_with_sound(lambda: self.show_page(3))
        )
        self.tips_button.grid(row=0, column=2, sticky="ew", padx=10)

        # Back to Main Menu Button
        self.back_button = tk.Button(
            self.button_frame,
            text="Back to Main Menu",
            font=self.button_font,
            bg=self.button_colors[4],
            fg="white",
            command=self.controller.play_with_sound(lambda: self.controller.back_to_main_menu())
        )
        self.back_button.grid(row=0, column=3, sticky="ew", padx=10)

        self.update_buttons_state()  # Disable the initial active button

    def show_page(self, page_num):
        """
        Display the specified instruction page.

        Args:
            page_num (int): The page number to display (1, 2, or 3).
        """
        self.current_page = page_num
        self.update_buttons_state()  # Update button states based on the current page

        # Update the title based on the current page
        if page_num == 1:
            self.title_label.config(text="How to Play?")
        elif page_num == 2:
            self.title_label.config(text="Lives and Points")
        elif page_num == 3:
            self.title_label.config(text="Tips to Succeed")
        else:
            self.title_label.config(text="Instructions")

        self.update_image()

    def update_buttons_state(self):
        """
        Updates the navigation buttons to disable the currently active button and enable others.
        The active button is grayed out to indicate the current page.
        """
        buttons = [
            self.how_to_play_button,
            self.lives_and_points_button,
            self.tips_button
        ]

        for i, button in enumerate(buttons, start=1):
            if i == self.current_page:
                button.config(state="disabled", bg="gray")  # Disable and gray out the active button
            else:
                # Restore original color and enable the button
                button.config(state="normal", bg=self.button_colors[i])

    def update_image(self):
        """
        Updates the image display with the resized version based on the current window size.
        Utilizes caching to optimize performance.
        """
        max_height = self.winfo_height() - self.button_frame.winfo_height() - self.title_label.winfo_height() - 40  # Adjust for buttons and title with padding
        max_width = self.winfo_width() - 100  # Subtract padding for aesthetics

        # Calculate new dimensions maintaining the aspect ratio
        width_ratio = max_width / self.image_width
        height_ratio = max_height / self.image_height
        scale_factor = min(width_ratio, height_ratio)  # Use the smaller ratio to ensure no clipping

        new_width = max(1, int(self.image_width * scale_factor))
        new_height = max(1, int(self.image_height * scale_factor))

        # Check if the image for the current size and page is already cached
        cache_key = (new_width, new_height, self.current_page)
        if cache_key in self.resized_images_cache:
            resized_image = self.resized_images_cache.pop(cache_key)
            self.resized_images_cache[cache_key] = resized_image  # Move to the end to indicate recent use
        else:
            original_image = self.original_images.get(self.current_page)
            if original_image is not None:
                try:
                    resized_image = original_image.resize(
                        (new_width, new_height),
                        resample=self.resample_method
                    )
                    self.resized_images_cache[cache_key] = resized_image
                    # Ensure cache size does not exceed maximum
                    if len(self.resized_images_cache) > self.MAX_RESIZED_CACHE:
                        self.resized_images_cache.popitem(last=False)  # Remove the oldest item
                except Exception as e:
                    messagebox.showerror("Image Resize Error", f"Failed to resize image for page {self.current_page}: {e}")
                    return
            else:
                # If image is not available, clear the image label
                self.image_label.config(image='')
                return

        # Cache the PhotoImage object
        if cache_key in self.tk_images_cache:
            photo_image = self.tk_images_cache.pop(cache_key)
            self.tk_images_cache[cache_key] = photo_image  # Move to the end to indicate recent use
        else:
            try:
                photo_image = ImageTk.PhotoImage(self.resized_images_cache[cache_key])
                self.tk_images_cache[cache_key] = photo_image
                # Ensure cache size does not exceed maximum
                if len(self.tk_images_cache) > self.MAX_TK_CACHE:
                    self.tk_images_cache.popitem(last=False)  # Remove the oldest item
            except Exception as e:
                messagebox.showerror("Image Conversion Error", f"Failed to convert image for page {self.current_page}: {e}")
                return

        # Set the image label with the PhotoImage
        self.image_label.config(image=photo_image)
        self.image_label.image = photo_image  # Keep a reference to prevent garbage collection

    def on_resize(self, event=None):
        """
        Handle window resizing events. Debounces rapid resize events to optimize performance.

        Args:
            event (tk.Event, optional): The event object. Defaults to None.
        """
        new_size = (self.winfo_width(), self.winfo_height())

        # Check if the size has changed significantly before resizing
        if (abs(new_size[0] - self.previous_size[0]) > 10) or (abs(new_size[1] - self.previous_size[1]) > 10):
            self.previous_size = new_size
            if not self.is_resizing:
                self.is_resizing = True
                self.after(100, self.perform_resize)  # Increased debounce delay to 100ms

    def perform_resize(self):
        """
        Perform the actual resizing operations, such as updating images and fonts.
        Called after a debounce delay to prevent excessive processing during rapid resizing.
        """
        self.update_image()
        self.update_label_font()
        self.update_button_font()
        self.is_resizing = False  # Reset resizing flag

    def update_label_font(self):
        """
        Dynamically adjusts the title label's font size based on the current window width.
        Ensures the font size remains within a readable range.
        """
        current_width = self.winfo_width()
        new_font_size = max(16, min(int(current_width / 25), 60))  # Limit font size between 16 and 60
        self.title_label.config(font=("Courier", new_font_size, "bold"))

    def update_button_font(self):
        """
        Dynamically adjusts the navigation buttons' font sizes based on the current window width.
        Ensures the font size remains within a readable range.
        """
        current_width = self.winfo_width()
        button_font_size = max(12, min(int(current_width / 60), 24))  # Limit font size between 12 and 24
        new_button_font = ("Courier", button_font_size, "bold")

        buttons = [
            self.how_to_play_button,
            self.lives_and_points_button,
            self.tips_button,
            self.back_button
        ]
        for button in buttons:
            button.config(font=new_button_font)