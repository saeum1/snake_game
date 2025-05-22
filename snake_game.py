import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 10

# Snake and food initialization
snake = [(100, 100), (90, 100), (80, 100)]  # Initial snake body
snake_dir = (CELL_SIZE, 0)  # Initial direction (moving right)
food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
        random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
score = 0

def draw_snake(snake):
    """Draw the snake on the screen."""
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def draw_food(food):
    """Draw the food on the screen."""
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

def show_game_over():
    """Display the game over screen."""
    font = pygame.font.Font(None, 74)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.fill(BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def get_next_direction(snake, food):
    """Calculate the next direction for the snake to move towards the food."""
    head_x, head_y = snake[0]
    food_x, food_y = food

    if head_x < food_x:
        return (CELL_SIZE, 0)  # Move right
    elif head_x > food_x:
        return (-CELL_SIZE, 0)  # Move left
    elif head_y < food_y:
        return (0, CELL_SIZE)  # Move down
    elif head_y > food_y:
        return (0, -CELL_SIZE)  # Move up
    return snake_dir  # Keep current direction if aligned

# Game loop
while True:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Automatic snake movement
    snake_dir = get_next_direction(snake, food)

    # Move the snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake = [new_head] + snake[:-1]

    # Check for collisions
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake[1:]):  # Collision with walls or itself
        show_game_over()

    # Check if the snake eats the food
    if new_head == food:
        snake.append(snake[-1])  # Grow the snake
        score += 10
        food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    # Draw everything
    draw_snake(snake)
    draw_food(food)

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)
