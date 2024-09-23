import pygame
import sys

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basic Game with Pause Overlay and Instructions Image Button")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Load and prepare GIF (frames should be extracted from the actual GIF)
gif_images = [pygame.image.load(f'Pictures/frame_{i}.gif') for i in range(0, 5)]  # Replace with actual frame filenames
gif_index = 0
gif_delay = 100  # Delay in milliseconds
last_gif_update = pygame.time.get_ticks()  # Initialize here

# Player properties
player_pos = [screen_width // 2, screen_height // 2]
player_speed = 5
player_size = 50

# Game state
is_paused = False
show_instructions = False

# Wrapped Text
def wrap_text(text, font, max_width):
    """Wrap text to fit within the specified width."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '

    lines.append(current_line)  # Add the last line
    return lines

# Font for buttons and instructions
font = pygame.font.Font(None, 36)

# Load images for buttons
instructions_button_image = pygame.image.load('Pictures/info.png')  
instructions_button_image = pygame.transform.scale(instructions_button_image, (60, 60))

# Button dimensions and positions
pause_button_rect = pygame.Rect((screen_width - 120 - 20, 20), (120, 50))
back_button_rect = pygame.Rect((screen_width - 120 - 20, 140), (120, 50))

# Function to display colored text
def render_colored_text(text, color, font):
    return font.render(text, True, color)


# Function to display the pause button
def draw_pause_button():
    button_color = GREEN if not is_paused else RED
    button_text = "Pause" if not is_paused else "Continue"
    pygame.draw.rect(screen, button_color, pause_button_rect)
    text_surface = font.render(button_text, True, WHITE)
    screen.blit(text_surface, (pause_button_rect.x + 20, pause_button_rect.y + 10))

# Function to display the instructions button (shown only when paused)
def draw_instructions_button():
    screen.blit(instructions_button_image, (screen_width - 60 - 20, 80))

# Function to display the back button (shown only in instructions overlay)
def draw_back_button():
    pygame.draw.rect(screen, GRAY, back_button_rect)
    text_surface = font.render("Back", True, WHITE)
    screen.blit(text_surface, (back_button_rect.x + 35, back_button_rect.y + 10))

# Function to display the pause overlay
def draw_pause_overlay():
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(150)  # Semi-transparent overlay
    overlay.fill(GRAY)
    screen.blit(overlay, (0, 0))

# Function to display instructions when toggled
def draw_instructions_overlay():
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(255)
    overlay.fill(GRAY)

    # Padding from the left side of the screen
    x_offset = 50

    # Define a smaller font for the instructions (e.g., size 28)
    small_font = pygame.font.Font(None, 28)

    # Instructions text with colors
    y_offset = 50
    overlay.blit(render_colored_text("How to play:", YELLOW, font), (screen_width // 2 - font.size("How to play:")[0] // 2, y_offset))
    y_offset += 30  # Adjusted spacing

    instruction1_surface = render_colored_text("1. You start with 3 lives and 0 points.", WHITE, small_font)
    overlay.blit(instruction1_surface, (x_offset, y_offset))
    y_offset += 30

    if y_offset < screen_height - 40:  # Leave some space for the bottom
        # Define the parts of the instruction
        instruction2_part1 = "2. If you see: "
        instruction2_part2 = "RED"
        instruction2_part3 = " words, type them exactly."
        instruction2_part4 = "BLUE"
        instruction2_part5 = " words, solve the math. "

        # Render the first part of the instruction in white
        text_surface_part1 = render_colored_text(instruction2_part1, WHITE, small_font)
        overlay.blit(text_surface_part1, (x_offset, y_offset))
        y_offset += 30

        # Render the "RED" word in red, positioned right after the first part
        red_text_surface = render_colored_text(instruction2_part2, RED, small_font)
        overlay.blit(red_text_surface, (x_offset + 20, y_offset))

        # Render the rest of the sentence in white, positioned right after the "RED" word
        text_surface_part3 = render_colored_text(instruction2_part3, WHITE, small_font)
        overlay.blit(text_surface_part3, (x_offset + 20 + red_text_surface.get_width(), y_offset))

        # Move the y_offset after rendering everything in one line
        y_offset += 30  # Space for the next text

        # Update y_offset after the first instruction and GIF
        #if y_offset + 100 < screen_height:  # Check if there's space for the GIF
            #overlay.blit(gif_images[gif_index], (screen_width // 2 - gif_images[gif_index].get_width() // 2, y_offset))  # Position GIF below the first instruction
            #y_offset += 50  # Move down for the next instruction

         # Render the "BLUE" word in blue, positioned right after the second part
        blue_text_surface = render_colored_text(instruction2_part4, BLUE, small_font)
        overlay.blit(blue_text_surface, (x_offset + 20, y_offset))

        # Render the rest of the sentence in white, positioned right after the "blue" word
        text_surface_part5 = render_colored_text(instruction2_part5, WHITE, small_font)
        overlay.blit(text_surface_part5, (x_offset + 20 + blue_text_surface.get_width(), y_offset))
        
        # Move the y_offset after rendering everything in one line
        y_offset += 30  # Space for the next text
        
        if y_offset < screen_height - 40:  # Check space for the next instruction
            instruction3_part1 = render_colored_text("3. Get it right:", WHITE, small_font)
            overlay.blit(instruction3_part1, (x_offset, y_offset))
            y_offset += 30

        if y_offset < screen_height - 40:  # Check space for the next instruction
            instruction3_part2 = render_colored_text("You get 10 points!", WHITE, small_font)
            overlay.blit(instruction3_part2, (x_offset + 20, y_offset))
            y_offset += 30

        if y_offset < screen_height - 40:  # Check space for the next instruction
            instruction4_part1 = render_colored_text("4. Get it wrong or take too long:", WHITE, small_font)
            overlay.blit(instruction4_part1, (x_offset, y_offset))
            y_offset += 30
        
        if y_offset < screen_height - 40:  # Check space for the next instruction
            instruction4_part2 = render_colored_text("You lose 1 life.", WHITE, small_font)
            overlay.blit(instruction4_part2, (x_offset + 20, y_offset))
            y_offset += 30

        if y_offset < screen_height - 40:  # Check space for the next instruction
            instruction5_surface = render_colored_text("5. If you lose all 3 lives, the game ends. ", WHITE, small_font)
            overlay.blit(instruction5_surface, (x_offset, y_offset))


    # Blit the overlay to the screen
    screen.blit(overlay, (0, 0))

    # Draw the back button
    draw_back_button()  # Draw the back button on top of the overlay

# Main game loop
def game_loop():
    global is_paused, show_instructions, gif_index, last_gif_update  # Declare as global
    running = True

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    is_paused = not is_paused  # Toggle pause state
                    show_instructions = False  # Hide instructions when unpausing

                if (screen_width - 60 - 20 <= event.pos[0] <= screen_width - 20) and \
                   (80 <= event.pos[1] <= 80 + 60) and is_paused:
                    show_instructions = True  # Show instructions if paused

                if back_button_rect.collidepoint(event.pos) and show_instructions:
                    show_instructions = False  # Hide instructions and go back

        # Update GIF frame
        now = pygame.time.get_ticks()
        if now - last_gif_update > gif_delay:
            gif_index = (gif_index + 1) % len(gif_images)  # Loop through GIF frames
            last_gif_update = now

        # Drawing
        screen.fill(BLACK)

        # Draw the player (a blue square)
        pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

        # Draw the pause button
        draw_pause_button()

        # Show overlay and buttons when paused
        if is_paused:
            draw_pause_overlay()
            draw_instructions_button()
            if show_instructions:
                draw_instructions_overlay()

        # Update the display
        pygame.display.flip()

        # Frame rate control
        pygame.time.Clock().tick(30)

# Start the game loop
game_loop()
