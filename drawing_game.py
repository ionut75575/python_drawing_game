import pygame
import pygame_gui
import sys
from PIL import Image

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
FPS = 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Canvas Drawing Game")
clock = pygame.time.Clock()

# Create a UI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Initialize variables for the infinite canvas
canvas_offset_x = 0
canvas_offset_y = 0
drawing_color = (255, 0, 0)  # Default to red
canvas = {}

# Create sliders for RGB values
red_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(10, 10, 200, 20),
    start_value=255,
    value_range=(0, 255),
    manager=manager
)

green_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(10, 40, 200, 20),
    start_value=0,
    value_range=(0, 255),
    manager=manager
)

blue_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(10, 70, 200, 20),
    start_value=0,
    value_range=(0, 255),
    manager=manager
)

# Create a rectangle to display the current color
color_display_rect = pygame.Rect(220, 10, 50, 50)

def draw_grid():
    """Draw the grid on the screen."""
    for x in range(-canvas_offset_x % GRID_SIZE, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(-canvas_offset_y % GRID_SIZE, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

def draw_canvas():
    """Draw the colored squares on the canvas."""
    for (x, y), color in canvas.items():
        pygame.draw.rect(screen, color, (x + canvas_offset_x, y + canvas_offset_y, GRID_SIZE, GRID_SIZE))

def save_canvas_as_png(filename):
    """Save the current canvas as a PNG file."""
    # Create a blank image with white background
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")

    # Draw the canvas onto the image
    for (x, y), color in canvas.items():
        for dx in range(GRID_SIZE):
            for dy in range(GRID_SIZE):
                if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
                    image.putpixel((x + dx, y + dy), color)

    # Save the image
    image.save(filename)

def main():
    global canvas_offset_x, canvas_offset_y, drawing_color

    while True:
        time_delta = clock.tick(FPS) / 1000.0  # Amount of seconds since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_canvas_as_png("canvas_image.png")  # Save the canvas on exit
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_canvas_as_png("canvas_image.png")  # Save the canvas on exit
                    pygame.quit()
                    sys.exit()
            # Process events for the UI manager
            manager.process_events(event)

        # Handle snapping movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            canvas_offset_y += GRID_SIZE  # Snap up
        if keys[pygame.K_s]:
            canvas_offset_y -= GRID_SIZE  # Snap down
        if keys[pygame.K_a]:
            canvas_offset_x += GRID_SIZE  # Snap left
        if keys[pygame.K_d]:
            canvas_offset_x -= GRID_SIZE  # Snap right

        # Update drawing color based on slider values
        drawing_color = (
            int(red_slider.get_current_value()),
            int(green_slider.get_current_value()),
            int(blue_slider.get_current_value())
        )

        # Drawing on canvas
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = (mouse_x - canvas_offset_x) // GRID_SIZE * GRID_SIZE
        grid_y = (mouse_y - canvas_offset_y) // GRID_SIZE * GRID_SIZE

        if pygame.mouse.get_pressed()[0]:  # Left mouse button for drawing
            canvas[(grid_x, grid_y)] = drawing_color
        elif pygame.mouse.get_pressed()[2]:  # Right mouse button for deleting
            if (grid_x, grid_y) in canvas:
                del canvas[(grid_x, grid_y)]  # Remove the pixel

        # Clear the screen and draw everything
        screen.fill((255, 255, 255))  # Clear screen to white
        draw_grid()
        draw_canvas()

        # Draw the color display rectangle
        pygame.draw.rect(screen, drawing_color, color_display_rect)

        # Update the UI manager and draw the sliders
        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()  # Update the display

if __name__ == "__main__":
    main()
