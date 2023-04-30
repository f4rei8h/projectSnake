import pygame
import random

# Initialize Pygame
pygame.init()

# Define the game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20
FPS = 7

# Define the game colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define the game fonts
FONT = pygame.font.Font(None, 36)

# Define the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")


# Define the Snake class
class Snake:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = BLOCK_SIZE
        self.dy = 0
        self.body = []
        self.length = 1
        self.score = 0
        self.add_body()

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.check_boundaries()
        self.check_collisions()
        self.body.insert(0, (self.x, self.y))
        if len(self.body) > self.length:
            self.body.pop()

    def add_body(self):
        for i in range(self.length):
            self.body.append((self.x - i * BLOCK_SIZE, self.y))

    def check_boundaries(self):
        if self.x < 0:
            self.x = SCREEN_WIDTH - BLOCK_SIZE
        elif self.x >= SCREEN_WIDTH:
            self.x = 0
        elif self.y < 0:
            self.y = SCREEN_HEIGHT - BLOCK_SIZE
        elif self.y >= SCREEN_HEIGHT:
            self.y = 0

    def check_collisions(self):
        for i in range(1, len(self.body)):
            if self.x == self.body[i][0] and self.y == self.body[i][1]:
                self.game_over()

    def game_over(self):
        game_over_text = FONT.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        self.__init__()

    def draw(self):
        for x, y in self.body:
            block = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, GREEN, block)
            pygame.draw.rect(screen, BLACK, block, 1)
        self.draw_score()

    def draw_score(self):
        score_text = FONT.render("Score: {}".format(self.score), True, WHITE)
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(score_text, score_rect)


# Define the Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.y = random.randint(0, SCREEN_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE

    def draw(self):
        block = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, RED, block)
        pygame.draw.rect(screen, BLACK, block, 1)


# Initialize the game objects
snake = Snake()
food = Food()

# Start the game loop
clock = pygame.time.Clock()
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if snake.dx == 0:
                    snake.dx = -BLOCK_SIZE
                    snake.dy = 0
            elif event.key == pygame.K_RIGHT:
                if snake.dx == 0:
                    snake.dx = BLOCK_SIZE
                    snake.dy = 0
            elif event.key == pygame.K_UP:
                if snake.dy == 0:
                    snake.dx = 0
                    snake.dy = -BLOCK_SIZE
            elif event.key == pygame.K_DOWN:
                if snake.dy == 0:
                    snake.dx = 0
                    snake.dy = BLOCK_SIZE

    # Move the snake
    snake.move()

    # Check for collisions with food
    if snake.x == food.x and snake.y == food.y:
        snake.length += 1
        snake.score += 10
        food = Food()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the game objects
    snake.draw()
    food.draw()

    # Update the screen
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(FPS)
