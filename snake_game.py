#!/usr/bin/env python3
"""
Simple Snake Game using Pygame
Controls: Arrow keys to move the snake
"""

import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Set display dimensions
display_width = 800
display_height = 600

# Create game display
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# Set game clock
clock = pygame.time.Clock()

# Snake block size and speed
snake_block = 20
snake_speed = 15

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_score(score):
    """Display the current score on the screen"""
    value = score_font.render("Score: " + str(score), True, BLUE)
    display.blit(value, [10, 10])

def draw_snake(snake_block, snake_list):
    """Draw the snake on the screen"""
    for block in snake_list:
        pygame.draw.rect(display, GREEN, [block[0], block[1], snake_block, snake_block])

def message(msg, color):
    """Display a message on the screen"""
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [display_width / 6, display_height / 3])

def game_loop():
    """Main game loop"""
    game_over = False
    game_close = False
    
    # Initial snake position
    x1 = display_width / 2
    y1 = display_height / 2
    
    # Snake movement direction
    x1_change = 0
    y1_change = 0
    
    # Snake body
    snake_list = []
    length_of_snake = 1
    
    # Food position
    food_x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    food_y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
    
    while not game_over:
        
        while game_close:
            # Game over screen
            display.fill(BLACK)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_score(length_of_snake - 1)
            pygame.display.update()
            
            # Check for player input after game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
        
        # Handle keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
        
        # Check for boundary collision
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True
        
        # Update snake position
        x1 += x1_change
        y1 += y1_change
        
        # Draw game screen
        display.fill(BLACK)
        
        # Draw food
        pygame.draw.rect(display, RED, [food_x, food_y, snake_block, snake_block])
        
        # Update snake body
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        
        # Remove extra segments if snake hasn't eaten food
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        
        # Check for self collision
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True
        
        # Draw snake and score
        draw_snake(snake_block, snake_list)
        display_score(length_of_snake - 1)
        
        pygame.display.update()
        
        # Check if snake ate food
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            food_y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            length_of_snake += 1
        
        # Control game speed
        clock.tick(snake_speed)
    
    # Quit pygame
    pygame.quit()
    quit()

# Start the game
if __name__ == "__main__":
    game_loop()