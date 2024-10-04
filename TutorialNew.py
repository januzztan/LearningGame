import pygame
import sys
from tkinter import PhotoImage

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Game Tutorial Menu")

# Load the font
font = pygame.font.Font("Assets/PixelOperatorSC-Bold.ttf", 70)
font2 = pygame.font.Font("Assets/PixelOperatorSC-Bold.ttf", 28)

# Load images for each page
page1_image = pygame.image.load("Assets/Tutorial_How2Play.png")
page1_image = pygame.transform.scale(page1_image, (1920 * 0.85, 760 * 0.85))
page2_image = pygame.image.load("Assets/Tutorial_LivesNPoints.png") 
page2_image = pygame.transform.scale(page2_image, (1920 * 0.85, 760 * 0.85))
page3_image = pygame.image.load("Assets/Tutorial_Tips2Succeed.png")
page3_image = pygame.transform.scale(page3_image, (1920 * 0.85, 760 * 0.85))

# Button class for creating buttons
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 0, 0)
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font_surface = font2.render(self.text, True, (255, 255, 255))
        font_rect = font_surface.get_rect(center=self.rect.center)
        surface.blit(font_surface, font_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Functions for each page

def draw_main_menu():
    screen.fill((255, 255, 255))
    title_surface = font.render("Main Menu", True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(960, 180))
    screen.blit(title_surface, title_rect)
    
    # Draw buttons
    start_button.draw(screen)
    quit_game_button.draw(screen)  # Button to quit the entire game

def draw_page1():
    screen.fill((255, 255, 255))
    title_surface = font.render("How to play?", True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(960, 180))
    screen.blit(title_surface, title_rect)
    
    # Display the image
    image_rect = page1_image.get_rect(center=(960, 520))
    screen.blit(page1_image, image_rect)
    
    # Draw buttons
    lives_and_points_button_page1.draw(screen)
    tips_button.draw(screen)
    back_to_main_menu_button.draw(screen)

def draw_page2():
    screen.fill((255, 255, 255))
    title_surface = font.render("Lives and Points", True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(960, 180))
    screen.blit(title_surface, title_rect)
    
    # Display the image
    image_rect = page2_image.get_rect(center=(960, 520))
    screen.blit(page2_image, image_rect)
    
    # Draw buttons
    how_to_play_button.draw(screen)
    tips_button.draw(screen)
    back_to_main_menu_button.draw(screen)

def draw_page3():
    screen.fill((255, 255, 255))
    title_surface = font.render("Tips to Succeed", True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(960, 180))
    screen.blit(title_surface, title_rect)
    
    # Display the image
    image_rect = page3_image.get_rect(center=(960, 520))
    screen.blit(page3_image, image_rect)
    
    # Draw buttons
    how_to_play_button.draw(screen)
    lives_and_points_button_page3.draw(screen)
    back_to_main_menu_button.draw(screen)

# Initialize buttons
button_width = 280  # Wider buttons for higher resolution
button_height = 70  # Taller buttons
button_spacing = 50

# Main menu buttons
start_button = Button("Start Game", 960 - button_width // 2, 780, button_width, button_height, action="page1")
quit_game_button = Button("Quit Game", 960 - button_width // 2, 880, button_width, button_height, action="quit")

# Page buttons (arranged horizontally)
button_y = 830

how_to_play_button = Button("How to play", 960 - (button_width // 2) - button_width - button_spacing, button_y, button_width, button_height, action="page1")
lives_and_points_button_page1 = Button("Lives and Points", 960 - (button_width // 2) - button_width - button_spacing, button_y, button_width, button_height, action="page2")
lives_and_points_button_page3 = Button("Lives and Points", 960 - (button_width // 2), button_y, button_width, button_height, action="page2")
tips_button = Button("Tips to succeed", 960 - (button_width // 2), button_y, button_width, button_height, action="page3")
back_to_main_menu_button = Button("Back to Main Menu", 960 + button_width // 2 + button_spacing, button_y, button_width, button_height, action="main_menu")


# Main loop
current_page = "main_menu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if current_page == "main_menu":
                if start_button.is_clicked(mouse_pos):
                    current_page = "page1"
                elif quit_game_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()
            elif current_page == "page1":
                if lives_and_points_button_page1.is_clicked(mouse_pos):
                    current_page = "page2"
                elif tips_button.is_clicked(mouse_pos):
                    current_page = "page3"
                elif back_to_main_menu_button.is_clicked(mouse_pos):
                    current_page = "main_menu"
            elif current_page == "page2":
                if how_to_play_button.is_clicked(mouse_pos):
                    current_page = "page1"
                elif tips_button.is_clicked(mouse_pos):
                    current_page = "page3"
                elif back_to_main_menu_button.is_clicked(mouse_pos):
                    current_page = "main_menu"
            elif current_page == "page3":
                if how_to_play_button.is_clicked(mouse_pos):
                    current_page = "page1"
                elif lives_and_points_button_page3.is_clicked(mouse_pos):
                    current_page = "page2"
                elif back_to_main_menu_button.is_clicked(mouse_pos):
                    current_page = "main_menu"

    # Draw the appropriate page
    if current_page == "main_menu":
        draw_main_menu()
    elif current_page == "page1":
        draw_page1()
    elif current_page == "page2":
        draw_page2()
    elif current_page == "page3":
        draw_page3()

    pygame.display.flip()
