import os
os.environ['SDL_AUDIODRIVER'] = 'directsound'  # Windows 환경에서 권장되는 드라이버
import pygame
import sys
import array
import math  # Python 내장 math 모듈 사용

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Sounds (generate simple beeps)
def generate_beep(frequency, duration, volume=0.5):
    """Generate a beep sound without numpy."""
    sample_rate = 44100
    amplitude = 32767 * volume
    num_samples = int(sample_rate * duration)
    wave = array.array("h", [int(amplitude * math.sin(2.0 * math.pi * frequency * t / sample_rate))
                             for t in range(num_samples)])
    return pygame.mixer.Sound(buffer=wave)

brick_sound = generate_beep(440, 0.1)  # A4 note
paddle_sound = generate_beep(880, 0.1)  # A5 note
wall_sound = generate_beep(330, 0.1)  # E4 note

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 7

# Ball
BALL_RADIUS = 8
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [4, -4]
speed_increment = 0.2  # Speed increase factor

# Bricks
BRICK_ROWS, BRICK_COLS = 5, 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 20
bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
          for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]

# Initialize score
score = 0

# Clock
clock = pygame.time.Clock()

def draw_text(text, font, color, x, y):
    """Helper function to draw text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    screen.blit(text_obj, text_rect)

def draw_score():
    """Display the current score on the screen."""
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def show_start_screen():
    """Display the start screen."""
    screen.fill(BLACK)
    draw_text("Brick Breaker", font, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text("Press any key to start", small_font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_key()

def show_game_over_screen(message):
    """Display the game over screen."""
    screen.fill(BLACK)
    draw_text(message, font, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text("Press any key to restart", small_font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    """Wait for the user to press a key."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

# Show the start screen
show_start_screen()

# Game loop
while True:
    # Reset game state
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_speed = [4, -4]
    bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
              for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]
    score = 0  # Reset score
    running = True

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Automatic paddle movement
        if ball.centerx < paddle.centerx and paddle.left > 0:
            paddle.move_ip(-paddle_speed, 0)
        elif ball.centerx > paddle.centerx and paddle.right < WIDTH:
            paddle.move_ip(paddle_speed, 0)

        # Ball movement
        ball.move_ip(ball_speed)
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
            wall_sound.play()  # Play wall hit sound
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
            wall_sound.play()  # Play wall hit sound
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]
            paddle_sound.play()  # Play paddle hit sound

        # Ball and brick collision
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_speed[1] = -ball_speed[1]
                brick_sound.play()  # Play brick hit sound
                score += 10  # Increase score
                # Increase ball speed
                ball_speed[0] += speed_increment if ball_speed[0] > 0 else -speed_increment
                ball_speed[1] += speed_increment if ball_speed[1] > 0 else -speed_increment
                break

        # Check for game over
        if ball.bottom >= HEIGHT:
            show_game_over_screen(f"Game Over! Final Score: {score}")
            running = False
        if not bricks:
            show_game_over_screen(f"You Win! Final Score: {score}")
            running = False

        # Draw everything
        pygame.draw.rect(screen, BLUE, paddle)
        pygame.draw.ellipse(screen, RED, ball)
        for brick in bricks:
            pygame.draw.rect(screen, GREEN, brick)
        draw_score()  # Draw the score

        pygame.display.flip()
        clock.tick(60)
