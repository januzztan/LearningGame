import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class TutorialMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Game Tutorial")
        self.geometry("1920x1080")

        # Load the background image 
        self.bg_image = Image.open("Assets/TutorialBg.png")
        self.bg_image = self.bg_image.resize((600, 400), Image.LANCZOS)  # Resize to fit the window size
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Create a label to display the background image
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window with the background imag
        #self.bg_label.pack(fill="both", expand=True)

        # Lower the background label to make sure it's at the bottom of the stacking order
        #self.bg_label.lower()

        # Variables to track the current page
        self.page = 1

        # Create the pages' content
        self.pages = [self.page1_content, self.page2_content, self.page3_content]

        # Initialize the UI with the first page
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        
        # Navigation Buttons
        self.nav_frame = tk.Frame(self.frame)
        self.nav_frame.pack(side="bottom", pady=100)

        self.prev_button = ttk.Button(self.nav_frame, text="<<", command=self.prev_page)
        self.next_button = ttk.Button(self.nav_frame, text=">>", command=self.next_page)
        self.exit_button = ttk.Button(self.nav_frame, text="Exit", command=self.quit)

        self.prev_button.grid(row=0, column=0, padx=50)
        self.next_button.grid(row=0, column=1, padx=50)
        self.exit_button.grid(row=0, column=2, padx=50)

        self.show_page()


    def show_page(self):
        for widget in self.frame.winfo_children():
            if widget != self.nav_frame:
                widget.destroy()

        # Display the content of the current page
        self.pages[self.page - 1]()

    def page1_content(self):
        title = tk.Label(self.frame, text="How to play?", font=("Arial", 60))
        title.pack(pady=50)

        description1 = tk.Label(self.frame, text="The game is designed to test both your typing speed and accuracy as well as your ability to solve basic addition and subtraction problems.", font=("Arial", 24), wraplength=1500, justify="center")
        description1.pack(pady=(10, 5))  # Add some space below the first description

        description2 = tk.Label(self.frame, text="You will be shown in either red or blue text:",font=("Arial", 24), wraplength=1500, justify="center")
        description2.pack(pady=(5, 10))  # Add space above and below the second description

        # Instructions layout
        instruction_frame = tk.Frame(self.frame)
        instruction_frame.pack()

        # Upper row
        upper_left = tk.Label(instruction_frame, text="For red text, type exactly what you see", font=("Arial", 24), wraplength=800)
        upper_left.grid(row=0, column=0, padx=10, pady=10)
        upper_right = tk.Label(instruction_frame, text="[Image of red text typing]", font=("Arial", 24), wraplength=800)
        upper_right.grid(row=0, column=1, padx=10, pady=10)

        # Lower row
        lower_left = tk.Label(instruction_frame, text="For blue text, solve a simple math problem", font=("Arial", 24), wraplength=800)
        lower_left.grid(row=1, column=0, padx=10, pady=10)
        lower_right = tk.Label(instruction_frame, text="[Image of math problem]", font=("Arial", 24), wraplength=800)
        lower_right.grid(row=1, column=1, padx=10, pady=10)

    def page2_content(self):
        title = tk.Label(self.frame, text="Lives and Points System", font=("Arial", 60))
        title.pack(pady=50)

        # Instructions layout
        instruction_frame = tk.Frame(self.frame)
        instruction_frame.pack()

        # Upper row
        upper_left = tk.Label(instruction_frame, text="Each correct answer gives you 10 points. Failure to answer in 20 seconds or a wrong answer does not deduct points.", font=("Arial", 24), wraplength=800)
        upper_left.grid(row=0, column=0, padx=10, pady=10)
        upper_right = tk.Label(instruction_frame, text="[Image of points system]", font=("Arial", 24), wraplength=800)
        upper_right.grid(row=0, column=1, padx=10, pady=10)

        # Lower row
        lower_left = tk.Label(instruction_frame, text="You start with 3 lives. Failure to answer within 20 seconds or wrong answer loses 1 life.", font=("Arial", 24), wraplength=800)
        lower_left.grid(row=1, column=0, padx=10, pady=10)
        lower_right = tk.Label(instruction_frame, text="[Image of lives system]", font=("Arial", 24), wraplength=800)
        lower_right.grid(row=1, column=1, padx=10, pady=10)

        description = tk.Label(self.frame, text="If all 3 lives are lost, the game ends and displays your total points.", font=("Arial", 24), wraplength=1500, justify="center")
        description.pack(pady=10)

    def page3_content(self):
        title = tk.Label(self.frame, text="Tips for Success", font=("Arial", 60))
        title.pack(pady=50)

        # Tips layout
        tips_frame = tk.Frame(self.frame)
        tips_frame.pack()

        # Upper row (images)
        img1 = tk.Label(tips_frame, text="[Image 1]", font=("Arial", 24), wraplength=400)
        img1.grid(row=0, column=0, padx=10, pady=10)
        img2 = tk.Label(tips_frame, text="[Image 2]", font=("Arial", 24), wraplength=400)
        img2.grid(row=0, column=1, padx=10, pady=10)
        img3 = tk.Label(tips_frame, text="[Image 3]", font=("Arial", 24), wraplength=400)
        img3.grid(row=0, column=2, padx=10, pady=10)

        # Lower row (content)
        title1 = tk.Label(tips_frame, text="Look at the questions carefully", font=("Arial", 18), wraplength=400)
        title1.grid(row=1, column=0, padx=10, pady=10)
        content1 = tk.Label(tips_frame, text="Don't get too rushed. Otherwise, you may misinterpret.", font=("Arial", 18), wraplength=400)
        content1.grid(row=2, column=0, padx=10, pady=10)

        title2 = tk.Label(tips_frame, text="Make good use of your time", font=("Arial", 18), wraplength=400)
        title2.grid(row=1, column=1, padx=10, pady=10)
        content2 = tk.Label(tips_frame, text="You will only get limited time on each question. Spend time wisely.", font=("Arial", 18), wraplength=400)
        content2.grid(row=2, column=1, padx=10, pady=10)

        title3 = tk.Label(tips_frame, text="Be confident in yourself", font=("Arial", 18), wraplength=400)
        title3.grid(row=1, column=2, padx=10, pady=10)
        content3 = tk.Label(tips_frame, text="Don't be afraid to make mistakes. Have fun learning!", font=("Arial", 18), wraplength=400)
        content3.grid(row=2, column=2, padx=10, pady=10)

    def next_page(self):
        if self.page < 3:
            self.page += 1
            self.show_page()

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.show_page()

# Run the tutorial menu
if __name__ == "__main__":
    app = TutorialMenu()
    app.mainloop()
