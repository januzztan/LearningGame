import tkinter as tk
from PIL import Image, ImageTk

# instruction_page.py

import tkinter as tk
from PIL import Image, ImageTk

class InstructionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Load the images using PIL
        self.page1_image = ImageTk.PhotoImage(Image.open("Assets/Tutorial_How2Play.png").resize((1632, 646)))
        self.page2_image = ImageTk.PhotoImage(Image.open("Assets/Tutorial_LivesNPoints.png").resize((1632, 646)))
        self.page3_image = ImageTk.PhotoImage(Image.open("Assets/Tutorial_Tips2Succeed.png").resize((1632, 646)))

        self.create_widgets()

    def create_widgets(self):
        # Page title
        self.title_label = tk.Label(self, text="How to play?", font=("PixelOperatorSC-Bold", 70), bg="white")
        self.title_label.pack(pady=20)

        # Image display
        self.image_label = tk.Label(self, image=self.page1_image)
        self.image_label.pack(pady=20)

        # Navigation buttons
        self.how_to_play_button = tk.Button(self, text="How to Play", command=lambda: self.show_page(1))
        self.lives_and_points_button = tk.Button(self, text="Lives and Points", command=lambda: self.show_page(2))
        self.tips_button = tk.Button(self, text="Tips to Succeed", command=lambda: self.show_page(3))
        self.back_button = tk.Button(self, text="Back to Main Menu", command=self.controller.back_to_main_menu)

        self.how_to_play_button.pack(side="left", padx=20)
        self.lives_and_points_button.pack(side="left", padx=20)
        self.tips_button.pack(side="left", padx=20)
        self.back_button.pack(side="right", padx=20)

    def show_page(self, page_num):
        if page_num == 1:
            self.title_label.config(text="How to play?")
            self.image_label.config(image=self.page1_image)
        elif page_num == 2:
            self.title_label.config(text="Lives and Points")
            self.image_label.config(image=self.page2_image)
        elif page_num == 3:
            self.title_label.config(text="Tips to Succeed")
            self.image_label.config(image=self.page3_image)

