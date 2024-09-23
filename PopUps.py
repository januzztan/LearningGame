import tkinter as tk
from tkinter import Toplevel, messagebox
from PIL import Image, ImageTk  # Pillow for image handling

# Function to show a custom pop-up with instructions and an image
def show_instructions_with_image():
    popup = Toplevel(root)
    popup.title("Instructions")
    popup.geometry("400x400")
    
    # Add text instructions to the pop-up
    instructions = """
    Welcome to the game!
    
    Instructions:
    1. Solve math problems to score points.
    2. Use hints when stuck.
    3. Complete science quizzes to proceed.
    
    Good luck!
    """
    instructions_label = tk.Label(popup, text=instructions, justify="left", padx=10, pady=10)
    instructions_label.pack()

    # Add an image (replace 'image.png' with your actual image file)
    img = Image.open("Pictures/Exclaim.png")
    img = img.resize((200, 200))  # Resize image to fit in the pop-up
    photo = ImageTk.PhotoImage(img)

    image_label = tk.Label(popup, image=photo)
    image_label.image = photo  # Keep reference to avoid garbage collection
    image_label.pack(pady=20)

# Function to show a pop-up with a clickable image button
def show_popup_with_image_button():
    popup = Toplevel(root)
    popup.title("Game Hint")
    popup.geometry("300x300")
    
    # Load image and resize for the button
    img = Image.open("Pictures/info.png")
    img = img.resize((150, 150))
    photo = ImageTk.PhotoImage(img)

    def on_image_button_click():
        print("Image Button Clicked!")
        messagebox.showinfo("Hint", "Hint: Break the problem into smaller parts!")
        popup.destroy()  # Close pop-up after the button is clicked

    # Create a button with the image
    image_button = tk.Button(popup, image=photo, command=on_image_button_click)
    image_button.image = photo  # Keep reference to avoid garbage collection
    image_button.pack(pady=20)

    # Add text for the button
    label = tk.Label(popup, text="Click the image for a hint!", pady=10)
    label.pack()

# Function to show text-based hints
def show_hint():
    hint = "Hint: Try breaking the problem into smaller parts!"
    messagebox.showinfo("Hint", hint)

# Function to simulate moving to the next level
def next_level():
    if messagebox.askyesno("Next Level", "Do you want to go to the next level?"):
        messagebox.showinfo("Level", "Level 2: Science Quiz")
    else:
        messagebox.showinfo("Exit", "Exiting the game.")

# Main game window
root = tk.Tk()
root.title("Game Window")
root.geometry("400x300")

# Button to show instructions with image
instructions_button = tk.Button(root, text="Show Instructions with Image", command=show_instructions_with_image)
instructions_button.pack(pady=10)

# Button to show the pop-up with an image button
image_button_popup = tk.Button(root, text="Show Pop-Up with Image Button", command=show_popup_with_image_button)
image_button_popup.pack(pady=10)

# Button to show text-based hints
hint_button = tk.Button(root, text="Show Hint", command=show_hint)
hint_button.pack(pady=10)

# Button to simulate moving to the next level
next_button = tk.Button(root, text="Next Level", command=next_level)
next_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
