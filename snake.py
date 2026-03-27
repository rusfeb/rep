#!/usr/bin/env python3
"""
Минималистичная игра Змейка для Arch Linux
Управление: стрелки клавиатуры
Мягкие пастельные цвета
"""

import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# Мягкие пастельные цвета
COLOR_BG = (250, 248, 240)        # Мягкий кремовый фон
COLOR_SNAKE = (135, 206, 190)     # Пастельный бирюзовый
COLOR_SNAKE_HEAD = (100, 180, 160) # Чуть темнее для головы
COLOR_FOOD = (230, 160, 160)      # Пастельный розово-красный
COLOR_TEXT = (80, 80, 90)         # Мягкий темно-серый для текста

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = RIGHT
        self.grow = False
    
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        # Запрет на разворот на 180 градусов
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def check_collision(self):
        head = self.body[0]
        # Столкновение со стенами
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        # Столкновение с собой
        if head in self.body[1:]:
            return True
        return False
    
    def eat(self):
        self.grow = True

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize([])
    
    def randomize(self, snake_body):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body:
                self.position = (x, y)
                break

def draw_grid(surface):
    """Рисует минималистичную сетку (очень тонкую)"""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, (240, 238, 230), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, (240, 238, 230), (0, y), (SCREEN_WIDTH, y))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка - Arch Linux Minimal")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    snake = Snake()
    food = Food()
    score = 0
    game_over = False
    
    running = True
    while running:
        clock.tick(FPS)
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize(snake.body)
                        score = 0
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        if not game_over:
            snake.move()
            
            # Проверка столкновений
            if snake.check_collision():
                game_over = True
            
            # Проверка поедания еды
            if snake.body[0] == food.position:
                snake.eat()
                score += 1
                food.randomize(snake.body)
        
        # Отрисовка
        screen.fill(COLOR_BG)
        draw_grid(screen)
        
        # Рисуем еду
        food_rect = pygame.Rect(
            food.position[0] * CELL_SIZE + 2,
            food.position[1] * CELL_SIZE + 2,
            CELL_SIZE - 4,
            CELL_SIZE - 4
        )
        pygame.draw.rect(screen, COLOR_FOOD, food_rect, border_radius=8)
        
        # Рисуем змейку
        for i, segment in enumerate(snake.body):
            segment_rect = pygame.Rect(
                segment[0] * CELL_SIZE + 1,
                segment[1] * CELL_SIZE + 1,
                CELL_SIZE - 2,
                CELL_SIZE - 2
            )
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE
            pygame.draw.rect(screen, color, segment_rect, border_radius=6)
        
        # Рисуем счет
        score_text = font.render(f"Счет: {score}", True, COLOR_TEXT)
        screen.blit(score_text, (10, 10))
        
        # Экран проигрыша
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))
            
            go_text = font.render("Игра окончена!", True, COLOR_TEXT)
            restart_text = font.render("Пробел - заново, Esc - выход", True, COLOR_TEXT)
            
            screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
