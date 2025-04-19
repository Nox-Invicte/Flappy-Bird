import pygame
import sys
import random  # Added for randomizing pipe height

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()
print(clock)

# Game variables
gravity = 1
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0

# Pipe variables
pipe_width = 100
pipe_gap = 150
pipe_speed = 5
pipe_distance = 300  # Distance between pipes
pipes = [{"x": SCREEN_WIDTH, "top_height": 200}]  # List to store pipes

# Load bird image
bird_default = pygame.image.load("assets/bird.png").convert_alpha()

# Load logo image
logo = pygame.image.load("assets/logo.png").convert_alpha()

# Resize bird image to fit the bird object dimensions
bird_default = pygame.transform.scale(bird_default, (75, 75))

bird_image = bird_default  # Default bird image

# Load pipe images
pipe_lower_image = pygame.image.load("assets/pipes1.png").convert_alpha()
pipe_upper_image = pygame.image.load("assets/pipes2.png").convert_alpha()

# Resize pipe images to extend beyond the width of the pipe rectangles by 1.5
pipe_lower_image = pygame.transform.scale(pipe_lower_image, (int(pipe_width * 1.15), pipe_lower_image.get_height()))
pipe_upper_image = pygame.transform.scale(pipe_upper_image, (int(pipe_width * 1.15), pipe_upper_image.get_height()))

# Load and scale background image
background_image = pygame.image.load("assets/bg.jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Background scrolling variables
bg_x = 0
bg_scroll_speed = 2

# Collision detection function
def check_collision(bird_rect, top_pipe_rect, bottom_pipe_rect):
    return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

# Initialize score
score = 0
font = pygame.font.Font(None, 50)  # Font for displaying the score

# Load number images
number_images = {str(i): pygame.transform.scale(pygame.image.load(f"assets/{i}.png").convert_alpha(), (30, 30)) for i in range(10)}

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Load button font
button_font = pygame.font.Font(None, 40)

def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=5)  # Add border radius for rounded corners
    button_text = button_font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))  # Center text within the rectangle
    screen.blit(button_text, text_rect)

def draw_credits():
    credits_text = button_font.render("Credits: Nox-Invicte (Github)", True, WHITE)
    credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
    screen.blit(credits_text, credits_rect)

def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Restart button
                if SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse_x <= SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2 and SCREEN_HEIGHT // 2 + 17.5 <= mouse_y <= SCREEN_HEIGHT // 2 + 70:
                    return True  # Restart the game
                # Exit button
                if SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse_x <= SCREEN_WIDTH // 2 + BUTTON_WIDTH // 2 and SCREEN_HEIGHT // 2 + 87.5<= mouse_y <= SCREEN_HEIGHT // 2 + 140:
                    pygame.quit()
                    sys.exit()

        # Draw background
        screen.blit(background_image, (0, 0))

        # Draw "Game Over" text with space
        game_text = pygame.font.Font(None, 100).render("Game", True, WHITE)
        over_text = pygame.font.Font(None, 100).render("Over", True, WHITE)
        game_text_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 170))
        over_text_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90))
        screen.blit(game_text, game_text_rect)
        screen.blit(over_text, over_text_rect)

        # Display final score below "Over"
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(final_score_text, final_score_rect)

        # Draw buttons
        draw_button("Restart", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE, BLACK)
        draw_button("Exit", SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 90, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE, BLACK)

        # Draw credits
        draw_credits()

        # Update display
        pygame.display.flip()

def title_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start the game when space is pressed
                    return

        # Draw background
        screen.blit(background_image, (0, 0))

        # Draw logo
        resized_logo = pygame.transform.scale(logo, (600, 200))  # Adjust dimensions as needed
        logo_rect = resized_logo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))  # Center the logo
        screen.blit(resized_logo, logo_rect.topleft)  # Draw the resized logo

        # Draw "Press Space to Start" text
        start_text = button_font.render("Press Space to Start", True, WHITE)
        start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(start_text, start_text_rect)

        # Draw credits
        draw_credits()

        # Update display
        pygame.display.flip()

# Main game loop
def main():
    global bird_y, bird_velocity, pipes, bird_image, bg_x, score

    # Show title screen
    title_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Make the bird "jump"
                    bird_velocity = -12  # Adjusted jump velocity

        # Apply gravity
        bird_velocity += gravity
        bird_y += bird_velocity

        # Prevent the bird from going outside the window
        if bird_y < 0:
            bird_y = 0
            bird_velocity = 0
        elif bird_y > SCREEN_HEIGHT - 30:  # 30 is the bird's height
            bird_y = SCREEN_HEIGHT - 30
            bird_velocity = 0

        # Move pipes to the left and generate new pipes
        for pipe in pipes:
            pipe["x"] -= pipe_speed
        if pipes[-1]["x"] < SCREEN_WIDTH - pipe_distance:
            new_top_height = random.randint(50, SCREEN_HEIGHT - pipe_gap - 50)  # Randomized height
            pipes.append({"x": SCREEN_WIDTH, "top_height": new_top_height})
        if pipes[0]["x"] + pipe_width < 0:  # Remove pipes that go off-screen
            pipes.pop(0)
            score += 1  # Increase score when a pipe is passed

        # Scroll background
        bg_x -= bg_scroll_speed
        if bg_x <= -SCREEN_WIDTH:
            bg_x = 0


        # Clear screen
        screen.fill(WHITE)

         # Draw background
        screen.blit(background_image, (bg_x, 0))
        screen.blit(background_image, (bg_x + SCREEN_WIDTH, 0))

        # Draw bird
        bird_rect = pygame.Rect(50, bird_y, 30, 30)
        rotated_bird_image = pygame.transform.rotate(bird_image, 30 if bird_velocity < 0 else 0)  # Rotate when rising
        rotated_bird_rect = rotated_bird_image.get_rect(center=bird_rect.center)  # Center the image
        screen.blit(rotated_bird_image, rotated_bird_rect.topleft)

        # Draw pipes
        for pipe in pipes:
            top_pipe_rect = pygame.Rect(pipe["x"], 0, pipe_width, pipe["top_height"])
            bottom_pipe_rect = pygame.Rect(pipe["x"], pipe["top_height"] + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe["top_height"] - pipe_gap)

            # Draw upper pipe
            upper_pipe_image_rect = pipe_upper_image.get_rect(midbottom=top_pipe_rect.midbottom)
            screen.blit(pipe_upper_image, upper_pipe_image_rect.topleft)

            # Draw lower pipe
            lower_pipe_image_rect = pipe_lower_image.get_rect(midtop=bottom_pipe_rect.midtop)
            screen.blit(pipe_lower_image, lower_pipe_image_rect.topleft)

            # Check for collisions
            if check_collision(bird_rect, top_pipe_rect, bottom_pipe_rect):
                if game_over_screen():  # Show game over screen and restart if chosen
                    bird_y = SCREEN_HEIGHT // 2
                    bird_velocity = 0
                    pipes = [{"x": SCREEN_WIDTH, "top_height": 200}]
                    score = 0
                    bg_x = 0
                    break
                else:
                    running = False

        # Display score using number images
        score_str = f"{score:02}"  # Format score with leading zero
        x_offset = SCREEN_WIDTH // 2 - (len(score_str) * 30) // 2  # Center the score
        for digit in score_str:
            screen.blit(number_images[digit], (x_offset, 50))
            x_offset += 30  # Move to the next position for the next digit

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

if __name__ == "__main__":
    main()
