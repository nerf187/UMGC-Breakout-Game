#
# Test file to verify Pygame installation and basic functionality.
#
import pygame
import sys

pygame.init()

#
# Set up the window dimensions
#
WIDTH, HEIGHT = 800, 600

#
# Create the main display window with our specified dimensions
#
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#
# Set the title that appears at the top of the window
#
pygame.display.set_caption("Are We There Yet?")

#
# Define colors using RGB values (Red, Green, Blue)
# Each value ranges from 0 to 255
#
WHITE = (255, 255, 255)
GREY = (212, 210, 212)
BLACK = (0, 0, 0)
BLUE = (0, 97, 148)
RED = (162, 8, 0)
ORANGE = (183, 119, 0)
GREEN = (0, 127, 33)
YELLOW = (197, 199, 37)

colors = [BLUE, WHITE]
color_index = 0  # Start with the first color (blue background)

#
# Variable to control the main game loop
#
running = True

#
# MAIN GAME LOOP
# This loop runs continuously until we set running = False
#
while running:

    #
    # EVENT HANDLING
    # Check for any events (key presses, mouse clicks, window close, etc.)
    #
    for event in pygame.event.get():

        #
        # Check if user clicked the X to close the window
        #
        if event.type == pygame.QUIT:
            running = False  # End the game loop when window is closed

        #
        # Check if a key was pressed down
        #
        elif event.type == pygame.KEYDOWN:
            #
            # Check if the pressed key was ESCAPE
            #
            if event.key == pygame.K_ESCAPE:
                running = False  # End the game loop when ESC is pressed

    #
    # DRAWING
    #
    # Fill the entire screen with a color from our list
    # Currently uses the first color (blue) since color_index = 0
    screen.fill(colors[color_index])

    #
    # Create a font object for drawing text
    # None means use the default system font, 48 is the font size
    #
    font = pygame.font.SysFont(None, 48)

    #
    # Create a text surface (an image containing our text)
    # Parameters: Text content, Anti-aliasing (True=smoothed edges), Text color, Background color
    #
    text = font.render("PyGame Works!", True, (255, 255, 255), BLACK)

    #
    # Draw (blit) the text onto the screen at position (250, 250)
    # = 250 pixels from left, 250 pixels from top
    #
    screen.blit(text, (250, 250))

    #
    # UPDATE DISPLAY
    # pygame uses double-buffering: we draw to a hidden buffer, then flip shows it
    # This prevents flickering and makes animations smooth
    #
    pygame.display.flip()

#
# CLEAN UP
# Quit pygame properly (releases resources like memory, closes windows)
#
pygame.quit()

#
# Exit the Python program completely
#
sys.exit()
