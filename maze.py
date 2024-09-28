import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_HEIGHT = 70

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Woah, a Random Maze!")

# Font setup
font = pygame.font.SysFont(None, 48)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color = BLUE

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# Maze generation
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []
        if x > 1 and maze[y][x - 2] == 1:
            neighbors.append((x - 2, y))
        if x < width - 2 and maze[y][x + 2] == 1:
            neighbors.append((x + 2, y))
        if y > 1 and maze[y - 2][x] == 1:
            neighbors.append((x, y - 2))
        if y < height - 2 and maze[y + 2][x] == 1:
            neighbors.append((x, y + 2))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[ny + (y - ny) // 2][nx + (x - nx) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

def draw_maze(maze):
    block_size = (SCREEN_HEIGHT - BUTTON_HEIGHT) // len(maze)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = WHITE if cell == 1 else BLACK
            pygame.draw.rect(screen, color, (x * block_size, BUTTON_HEIGHT + y * block_size, block_size, block_size))

# Game function
def game():
    maze = generate_maze(39, 29)
    player_pos = [1, 1]
    block_size = (SCREEN_HEIGHT - BUTTON_HEIGHT) // len(maze)
    running = True

    def back_to_menu():
        nonlocal running
        running = False

    def quit_game():
        pygame.quit()
        sys.exit()

    buttons = [
        Button("Back to Menu", SCREEN_WIDTH // 2 - 200, 10, 180, 50, back_to_menu),
        Button("Quit", SCREEN_WIDTH // 2 + 20, 10, 180, 50, quit_game)
    ]

    clock = pygame.time.Clock()

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for button in buttons:
                button.click(event)

        new_pos = player_pos[:]
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_pos[1] -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_pos[1] += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            new_pos[0] -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            new_pos[0] += 1

        # Check for wall collision
        if 0 <= new_pos[0] < len(maze[0]) and 0 <= new_pos[1] < len(maze) and maze[new_pos[1]][new_pos[0]] == 0:
            player_pos = new_pos

        screen.fill(BLACK)
        draw_maze(maze)
        pygame.draw.rect(screen, RED, (player_pos[0] * block_size, BUTTON_HEIGHT + player_pos[1] * block_size, block_size, block_size))

        for button in buttons:
            button.draw()

        pygame.display.flip()
        clock.tick(30)  # Increase frame rate for more responsive controls

    main_menu()

completed_mazes = 0

# Main menu
def main_menu():
    global completed_mazes

    def start_game():
        global completed_mazes
        completed_mazes += 1
        game()

    def quit_game():
        pygame.quit()
        sys.exit()

    buttons = [
        Button("Start New Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, start_game),
        Button("Quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10, 200, 50, quit_game)
    ]

    running = True
    while running:
        screen.fill(BLACK)
        title_surf = font.render("Woah, a Random Maze!", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title_surf, title_rect)

        counter_surf = font.render(f"Mazes Completed: {completed_mazes}", True, WHITE)
        counter_rect = counter_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        screen.blit(counter_surf, counter_rect)

        for button in buttons:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.click(event)

        pygame.display.flip()

# Start the game
main_menu()
