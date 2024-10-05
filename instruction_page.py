import tkinter as tk
from PIL import Image, ImageTk
import pygame

class InstructionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Set the background to black
        self.configure(bg="black")
        
        # Load the images using PIL
        self.original_images = {
            1: Image.open("Assets/Pictures/Inst_How2Play.png"),
            2: Image.open("Assets/Pictures/Inst_LivesNPoints.png"),
            3: Image.open("Assets/Pictures/Inst_Tips2Succeed.png")
        }
        self.page_images = {
            1: ImageTk.PhotoImage(self.original_images[1]),
            2: ImageTk.PhotoImage(self.original_images[2]),
            3: ImageTk.PhotoImage(self.original_images[3]),
        }

        # Get image size and aspect ratio
        self.image_width, self.image_height = self.original_images[1].size
        self.aspect_ratio = self.image_height / self.image_width  # Height / Width

        self.current_page = 1  # Track current page
        self.is_resizing = False  # Track if the window is currently resizing
        self.last_resize_time = 0  # Track the last resize time

        # Create main layout frame
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(expand=True, fill=tk.BOTH)  # Allow expansion and fill

        # Create widgets
        self.create_widgets()

        # Resize elements immediately after initialization
        self.update_idletasks()  # Make sure widgets are rendered before resizing
        self.on_resize(None)  # Trigger initial resize
        
        # Bind the configure event to handle window resizing
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # Set grid weights for the main frame
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Image should expand
        self.main_frame.grid_rowconfigure(2, weight=0)  # Buttons should not expand vertically
        self.main_frame.grid_columnconfigure(0, weight=1)  # Whole layout should expand horizontally

        # Page title
        self.title_label = tk.Label(self.main_frame, text="How to play?", font=("Courier", 60, "bold"), fg="white", bg="black")
        self.title_label.grid(row=0, column=0, sticky="nsew")

        # Image display
        self.image_label = tk.Label(self.main_frame, image=self.page_images[self.current_page], bg="black")
        self.image_label.grid(row=1, column=0, sticky="nsew")

        # Navigation buttons frame
        self.button_frame = tk.Frame(self.main_frame, bg="black")
        self.button_frame.grid(row=2, column=0, pady=(0,10), sticky="nsew")
        
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

        self.how_to_play_button = tk.Button(self.button_frame, text="How to Play", font=self.button_font, bg=self.button_colors[1], fg="white", 
                                            command=self.controller.play_with_sound(lambda: self.show_page(1)))
        self.how_to_play_button.grid(row=0, column=0, sticky="ew", padx=10)

        self.lives_and_points_button = tk.Button(self.button_frame, text="Lives and Points", font=self.button_font, bg=self.button_colors[2], fg="white", 
                                                 command=self.controller.play_with_sound(lambda: self.show_page(2)))
        self.lives_and_points_button.grid(row=0, column=1, sticky="ew", padx=10)

        self.tips_button = tk.Button(self.button_frame, text="Tips to Succeed", font=self.button_font, bg=self.button_colors[3], fg="white", 
                                     command=self.controller.play_with_sound(lambda: self.show_page(3)))
        self.tips_button.grid(row=0, column=2, sticky="ew", padx=10)

        self.back_button = tk.Button(self.button_frame, text="Back to Main Menu", font=self.button_font, bg=self.button_colors[4], fg="white", 
                                     command=self.controller.play_with_sound(lambda: self.controller.back_to_main_menu()))
        self.back_button.grid(row=0, column=3, sticky="ew", padx=10)

        self.update_buttons_state()  # Call to disable the initial active button

    def show_page(self, page_num):
        self.current_page = page_num
        self.update_buttons_state()  # Update the button state right after setting the current page
        if page_num == 1:
            self.title_label.config(text="How to play?")
        elif page_num == 2:
            self.title_label.config(text="Lives and Points")
        elif page_num == 3:
            self.title_label.config(text="Tips to Succeed")
        self.update_image()

    def update_buttons_state(self):
        """Updates the buttons to disable the currently active button."""
        buttons = [
            self.how_to_play_button,
            self.lives_and_points_button,
            self.tips_button
        ]
        
        for i, button in enumerate(buttons):
            if i + 1 == self.current_page:  # Check if this is the active page
                button.config(state="disabled", bg="gray")  # Disable and change color
            else:
                # Restore original color when re-enabling the button
                button.config(state="normal", bg=self.button_colors[i + 1])  # Enable and restore color

    def update_image(self):
        """Updates the image display with the resized version based on the window size."""
        max_height = self.winfo_height() - self.button_frame.winfo_height() - self.title_label.winfo_height()  # Adjust for buttons and title
        max_width = self.winfo_width() - 50  # Subtract some padding for aesthetics

        # Calculate new dimensions maintaining the aspect ratio
        width_ratio = max_width / self.image_width
        height_ratio = max_height / self.image_height
        scale_factor = min(width_ratio, height_ratio)  # Use the smaller ratio to ensure no clipping

        new_width = int(self.image_width * scale_factor)
        new_height = int(self.image_height * scale_factor)

        if new_width > 0 and new_height > 0:
            resized_image = self.original_images[self.current_page].resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.page_images[self.current_page] = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=self.page_images[self.current_page])
            self.image_label.image = self.page_images[self.current_page]  # Avoid image garbage collection

    def on_resize(self, event=None):
        """Handle window resizing event and update the image and label accordingly."""
        if self.is_resizing:
            return  # Ignore if already resizing

        self.is_resizing = True  # Set flag to indicate resizing is happening
        self.after(10, self.perform_resize)  # Schedule resize after a short delay

    def perform_resize(self):
        """Actual resizing operations, called after a delay to debounce."""
        self.update_image()
        self.update_label_font()
        self.update_button_font()
        self.is_resizing = False  # Reset resizing flag

    def update_label_font(self):
        """Dynamically adjusts the label font size based on window size."""
        current_width = self.winfo_width()
        new_font_size = max(16, min(int(current_width / 25), 60))  # Limit font size between 16 and 60
        self.title_label.config(font=("Courier", new_font_size, "bold"))

    def update_button_font(self):
        """Dynamically adjust the button font size based on window size.""" 
        current_width = self.winfo_width()
        button_font_size = max(12, min(int(current_width / 60), 24))  # Limit font size between 12 and 24
        new_button_font = ("Courier", button_font_size, "bold")
        
        buttons = [self.how_to_play_button, self.lives_and_points_button, 
                   self.tips_button, self.back_button]
    
        for button in buttons:
            button.config(font=new_button_font)