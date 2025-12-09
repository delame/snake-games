#!/usr/bin/env python3
"""
Minecraft-style 3D Snake Game using Pygame
Isometric view with blocky graphics
Controls: Arrow keys to move the snake
"""

import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Define Minecraft-style colors
GRASS_GREEN = (124, 174, 66)
DIRT_BROWN = (151, 109, 83)
STONE_GRAY = (112, 112, 112)
SNAKE_GREEN = (85, 170, 85)
FOOD_RED = (210, 65, 50)
SKY_BLUE = (135, 206, 235)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (50, 50, 50, 150)

# Set display dimensions
WIDTH, HEIGHT = 1000, 800

# Create game display
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minecraft 3D Snake')

# Set game clock
clock = pygame.time.Clock()

# Game settings
BLOCK_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15
SNAKE_SPEED = 8

# Font styles
font = pygame.font.SysFont('Arial', 30, bold=True)
title_font = pygame.font.SysFont('Arial', 50, bold=True)

class Block:
    """A 3D block with isometric projection"""
    def __init__(self, x, y, color, is_snake=False):
        self.x = x
        self.y = y
        self.color = color
        self.is_snake = is_snake
        
    def draw(self, surface):
        # Isometric projection
        iso_x = (self.x - self.y) * (BLOCK_SIZE // 2)
        iso_y = (self.x + self.y) * (BLOCK_SIZE // 4)
        
        # Center the grid
        center_x = WIDTH // 2
        center_y = HEIGHT // 3
        
        iso_x += center_x
        iso_y += center_y
        
        # Draw shadow
        if self.is_snake:
            shadow = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE // 2), pygame.SRCALPHA)
            shadow.fill(SHADOW_COLOR)
            surface.blit(shadow, (iso_x + 5, iso_y + 10))
        
        # Draw top face
        top_points = [
            (iso_x, iso_y),
            (iso_x + BLOCK_SIZE // 2, iso_y - BLOCK_SIZE // 4),
            (iso_x + BLOCK_SIZE, iso_y),
            (iso_x + BLOCK_SIZE // 2, iso_y + BLOCK_SIZE // 4)
        ]
        pygame.draw.polygon(surface, self.color, top_points)
        
        # Draw side faces (darker shades for 3D effect)
        side_color = [max(0, c - 30) for c in self.color]
        
        # Left side
        left_points = [
            (iso_x, iso_y),
            (iso_x + BLOCK_SIZE // 2, iso_y - BLOCK_SIZE // 4),
            (iso_x + BLOCK_SIZE // 2, iso_y + BLOCK_SIZE // 4),
            (iso_x, iso_y + BLOCK_SIZE // 2)
        ]
        pygame.draw.polygon(surface, tuple(side_color), left_points)
        
        # Right side
        right_points = [
            (iso_x + BLOCK_SIZE, iso_y),
            (iso_x + BLOCK_SIZE // 2, iso_y - BLOCK_SIZE // 4),
            (iso_x + BLOCK_SIZE // 2, iso_y + BLOCK_SIZE // 4),
            (iso_x + BLOCK_SIZE, iso_y + BLOCK_SIZE // 2)
        ]
        pygame.draw.polygon(surface, tuple(side_color), right_points)
        
        # Add outlines for Minecraft blocky look
        pygame.draw.polygon(surface, (0, 0, 0), top_points, 2)
        pygame.draw.polygon(surface, (0, 0, 0), left_points, 1)
        pygame.draw.polygon(surface, (0, 0, 0), right_points, 1)

def draw_grid():
    """Draw the Minecraft-style grass/dirt grid"""
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            # Create grass blocks with some dirt variation
            if random.random() > 0.9:  # 10% chance for dirt
                color = DIRT_BROWN
            else:
                color = GRASS_GREEN
            
            # Darker colors for blocks further away (depth effect)
            distance_factor = 1.0 - (x + y) / (GRID_WIDTH + GRID_HEIGHT) * 0.3
            adjusted_color = [int(c * distance_factor) for c in color]
            
            block = Block(x, y, tuple(adjusted_color))
            block.draw(display)

def draw_sky():
    """Draw the Minecraft-style sky background"""
    # Gradient sky
    for y in range(HEIGHT // 2):
        # Lighter at top, darker at bottom
        blue_value = min(255, 135 + y // 3)
        color = (135, blue_value, 235)
        pygame.draw.line(display, color, (0, y), (WIDTH, y))
    
    # Add some clouds
    for _ in range(10):
        cloud_x = random.randint(50, WIDTH - 50)
        cloud_y = random.randint(50, HEIGHT // 3)
        cloud_size = random.randint(30, 80)
        
        # Draw fluffy clouds
        for __ in range(5):
            pygame.draw.ellipse(display, (255, 255, 255),
                              (cloud_x + random.randint(-20, 20),
                               cloud_y + random.randint(-10, 10),
                               cloud_size // 2, cloud_size // 3))

def display_score(score):
    """Display the score with Minecraft-style text"""
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    
    # Add Minecraft-style outline
    for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
        outline_text = font.render(f"Score: {score}", True, SHADOW_COLOR)
        display.blit(outline_text, (20 + dx, 20 + dy))
    
    display.blit(score_text, (20, 20))

def game_over_screen(score):
    """Display game over screen with Minecraft aesthetic"""
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    display.blit(overlay, (0, 0))
    
    # Game over text with Minecraft style
    game_over_text = title_font.render("GAME OVER", True, FOOD_RED)
    score_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    restart_text = font.render("Press R to Restart or Q to Quit", True, TEXT_COLOR)
    
    # Add outlines
    for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
        outline = title_font.render("GAME OVER", True, SHADOW_COLOR)
        display.blit(outline, (WIDTH//2 - 150 + dx, HEIGHT//2 - 100 + dy))
        
        outline_score = font.render(f"Final Score: {score}", True, SHADOW_COLOR)
        display.blit(outline_score, (WIDTH//2 - 120 + dx, HEIGHT//2 + dx))
        
        outline_restart = font.render("Press R to Restart or Q to Quit", True, SHADOW_COLOR)
        display.blit(outline_restart, (WIDTH//2 - 180 + dx, HEIGHT//2 + 50 + dy))
    
    display.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 100))
    display.blit(score_text, (WIDTH//2 - 120, HEIGHT//2))
    display.blit(restart_text, (WIDTH//2 - 180, HEIGHT//2 + 50))

def game_loop():
    """Main game loop for 3D Minecraft Snake"""
    
    # Initial snake position (in grid coordinates)
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (1, 0)  # Start moving right
    
    # Generate food
    def generate_food():
        while True:
            food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food_pos not in snake:
                return food_pos
    
    food_pos = generate_food()
    score = 0
    
    game_over = False
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)
                elif event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
        
        # Move snake
        head_x, head_y = snake[0]
        new_head = (head_x + snake_direction[0], head_y + snake_direction[1])
        
        # Check collisions
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in snake):
            
            # Game over sequence
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return  # Restart game
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                
                # Draw game over screen
                draw_sky()
                draw_grid()
                
                # Draw final snake
                for i, (x, y) in enumerate(snake):
                    # Head is brighter green
                    if i == 0:
                        color = (100, 200, 100)
                    else:
                        color = SNAKE_GREEN
                    block = Block(x, y, color, is_snake=True)
                    block.draw(display)
                
                # Draw food
                food_block = Block(food_pos[0], food_pos[1], FOOD_RED)
                food_block.draw(display)
                
                game_over_screen(score)
                pygame.display.update()
                clock.tick(SNAKE_SPEED)
        
        # Add new head
        snake.insert(0, new_head)
        
        # Check if snake ate food
        if new_head == food_pos:
            score += 1
            food_pos = generate_food()
        else:
            # Remove tail if no food eaten
            snake.pop()
        
        # Draw everything
        draw_sky()
        draw_grid()
        
        # Draw snake
        for i, (x, y) in enumerate(snake):
            # Head is brighter green
            if i == 0:
                color = (100, 200, 100)
            else:
                color = SNAKE_GREEN
            block = Block(x, y, color, is_snake=True)
            block.draw(display)
        
        # Draw food
        food_block = Block(food_pos[0], food_pos[1], FOOD_RED)
        food_block.draw(display)
        
        # Draw score
        display_score(score)
        
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

# Start the game with a loading screen
def main():
    """Main function with loading screen"""
    
    # Loading screen
    display.fill(SKY_BLUE)
    loading_text = title_font.render("Minecraft 3D Snake", True, TEXT_COLOR)
    loading_subtext = font.render("Loading...", True, TEXT_COLOR)
    
    display.blit(loading_text, (WIDTH//2 - 200, HEIGHT//2 - 50))
    display.blit(loading_subtext, (WIDTH//2 - 80, HEIGHT//2 + 20))
    pygame.display.update()
    
    # Wait a moment for dramatic effect
    pygame.time.wait(1000)
    
    # Start game loop
    while True:
        game_loop()

if __name__ == "__main__":
    main()