"""
Modern Snake Game - Professional Edition
A modernized version of the classic Snake game with enhanced features.
"""

import sys
import random
import pygame
import json
from pathlib import Path
from typing import Tuple, List, Optional
from enum import Enum
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60

# Modern Color Palette
class Colors:
    # Dark theme
    BACKGROUND = (15, 15, 35)
    GRID_DARK = (20, 20, 45)
    GRID_LIGHT = (25, 25, 50)
    
    # Snake colors with gradient
    SNAKE_HEAD = (100, 255, 150)
    SNAKE_BODY = (50, 200, 100)
    SNAKE_TAIL = (30, 150, 80)
    
    # Food colors
    FOOD = (255, 80, 80)
    FOOD_GLOW = (255, 120, 120)
    
    # UI colors
    TEXT_PRIMARY = (255, 255, 255)
    TEXT_SECONDARY = (180, 180, 200)
    TEXT_ACCENT = (100, 255, 150)
    BUTTON_BG = (40, 40, 70)
    BUTTON_HOVER = (60, 60, 100)
    BUTTON_ACTIVE = (80, 80, 120)
    
    # Effects
    PARTICLE = (255, 200, 100)
    SHADOW = (0, 0, 0, 100)

# Game States
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

# Difficulty Levels
class Difficulty(Enum):
    EASY = ("Easy", 8, 1.2)
    MEDIUM = ("Medium", 12, 1.0)
    HARD = ("Hard", 18, 0.8)
    
    def __init__(self, name: str, speed: int, food_multiplier: float):
        self.display_name = name
        self.speed = speed
        self.food_multiplier = food_multiplier

# Direction vectors
class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Particle:
    """Visual particle effect for food collection"""
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 30
        self.color = color
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity
        self.life -= 1
    
    def draw(self, surface: pygame.Surface):
        if self.life > 0:
            alpha = int((self.life / 30) * 255)
            color = (*self.color, alpha)
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (self.size, self.size), self.size)
            surface.blit(s, (int(self.x), int(self.y)))

class Snake:
    """Modern Snake class with enhanced features"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset snake to initial state"""
        self.length = 3
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
        self.next_direction = self.direction
        self.score = 0
        self.food_eaten = 0
        self.growing = False
    
    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]
    
    def turn(self, direction: Tuple[int, int]):
        """Change direction if valid"""
        # Prevent 180-degree turns
        if self.length > 1:
            opposite = (-self.direction[0], -self.direction[1])
            if direction == opposite:
                return
        self.next_direction = direction
    
    def move(self) -> bool:
        """Move snake and return True if alive, False if collision"""
        self.direction = self.next_direction
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        
        # Calculate new head position with wrapping
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        
        # Check self-collision (skip first few segments for better gameplay)
        if len(self.positions) > 4 and new_head in self.positions[1:]:
            return False
        
        # Add new head
        self.positions.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.growing:
            if len(self.positions) > self.length:
                self.positions.pop()
        else:
            self.growing = False
        
        return True
    
    def grow(self):
        """Increase snake length"""
        self.length += 1
        self.growing = True
        self.food_eaten += 1
    
    def draw(self, surface: pygame.Surface):
        """Draw snake with gradient effect"""
        for i, pos in enumerate(self.positions):
            # Calculate color gradient from head to tail
            if i == 0:
                color = Colors.SNAKE_HEAD
                size = GRID_SIZE
            else:
                ratio = i / max(len(self.positions) - 1, 1)
                color = self._interpolate_color(Colors.SNAKE_BODY, Colors.SNAKE_TAIL, ratio)
                size = GRID_SIZE - 1
            
            # Draw segment with rounded corners
            rect = pygame.Rect(pos[0], pos[1], size, size)
            pygame.draw.rect(surface, color, rect, border_radius=5)
            
            # Add highlight to head
            if i == 0:
                highlight = pygame.Rect(pos[0] + 2, pos[1] + 2, size - 4, size - 4)
                pygame.draw.rect(surface, (150, 255, 180), highlight, 2, border_radius=3)
    
    @staticmethod
    def _interpolate_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
        """Interpolate between two colors"""
        return tuple(int(c1 + (c2 - c1) * ratio) for c1, c2 in zip(color1, color2))

class Food:
    """Food class with glow effect"""
    
    def __init__(self):
        self.position = (0, 0)
        self.glow_radius = 0
        self.glow_direction = 1
        self.randomize_position()
    
    def randomize_position(self, snake_positions: Optional[List[Tuple[int, int]]] = None):
        """Place food at random position, avoiding snake"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            
            if snake_positions is None or self.position not in snake_positions:
                break
    
    def update(self):
        """Update glow animation"""
        self.glow_radius += self.glow_direction * 0.5
        if self.glow_radius >= 8:
            self.glow_direction = -1
        elif self.glow_radius <= 0:
            self.glow_direction = 1
    
    def draw(self, surface: pygame.Surface):
        """Draw food with glow effect"""
        x, y = self.position
        
        # Draw glow
        glow_surface = pygame.Surface((GRID_SIZE * 3, GRID_SIZE * 3), pygame.SRCALPHA)
        glow_rect = glow_surface.get_rect(center=(GRID_SIZE * 1.5, GRID_SIZE * 1.5))
        pygame.draw.circle(glow_surface, (*Colors.FOOD_GLOW, 50), 
                         (GRID_SIZE * 1.5, GRID_SIZE * 1.5), 
                         GRID_SIZE + self.glow_radius)
        surface.blit(glow_surface, (x - GRID_SIZE, y - GRID_SIZE))
        
        # Draw food
        rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, Colors.FOOD, rect, border_radius=8)
        
        # Add shine
        shine = pygame.Rect(x + 4, y + 4, GRID_SIZE - 8, GRID_SIZE - 8)
        pygame.draw.rect(surface, (255, 150, 150), shine, 2, border_radius=5)

class Button:
    """Interactive button for menus"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
        self.clicked = False
    
    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> bool:
        """Update button state and return True if clicked"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered and mouse_clicked:
            self.clicked = True
            return True
        
        return False
    
    def draw(self, surface: pygame.Surface):
        """Draw button with hover effect"""
        color = Colors.BUTTON_HOVER if self.hovered else Colors.BUTTON_BG
        
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect, border_radius=10)
        
        # Draw button
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, Colors.TEXT_ACCENT, self.rect, 2, border_radius=10)
        
        # Draw text
        text_surface = self.font.render(self.text, True, Colors.TEXT_PRIMARY)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class HighScoreManager:
    """Manage high scores with persistence"""
    
    def __init__(self, filename: str = "highscores.json"):
        self.filename = filename
        self.scores = self.load_scores()
    
    def load_scores(self) -> dict:
        """Load scores from file"""
        try:
            if Path(self.filename).exists():
                with open(self.filename, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading scores: {e}")
        
        return {
            "easy": {"score": 0, "date": ""},
            "medium": {"score": 0, "date": ""},
            "hard": {"score": 0, "date": ""}
        }
    
    def save_scores(self):
        """Save scores to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Error saving scores: {e}")
    
    def update_score(self, difficulty: str, score: int) -> bool:
        """Update high score if new score is higher"""
        difficulty_key = difficulty.lower()
        if score > self.scores[difficulty_key]["score"]:
            self.scores[difficulty_key] = {
                "score": score,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.save_scores()
            return True
        return False
    
    def get_high_score(self, difficulty: str) -> int:
        """Get high score for difficulty"""
        return self.scores[difficulty.lower()]["score"]

class SnakeGame:
    """Main game class"""
    
    def __init__(self):
        # Setup display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Modern Snake Game - Professional Edition')
        
        # Load icon if exists
        try:
            icon = pygame.image.load('gameico.png')
            pygame.display.set_icon(icon)
        except:
            pass
        
        # Game objects
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.particles: List[Particle] = []
        self.high_score_manager = HighScoreManager()
        
        # Game state
        self.state = GameState.MENU
        self.difficulty = Difficulty.MEDIUM
        self.running = True
        self.new_high_score = False
        
        # Timing
        self.move_timer = 0
        self.game_start_time = 0
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Menu buttons
        self.setup_menu_buttons()
    
    def setup_menu_buttons(self):
        """Setup menu buttons"""
        center_x = SCREEN_WIDTH // 2
        
        # Main menu buttons
        self.btn_play = Button(center_x - 100, 250, 200, 50, "Play", self.font_small)
        self.btn_easy = Button(center_x - 250, 330, 150, 40, "Easy", self.font_tiny)
        self.btn_medium = Button(center_x - 75, 330, 150, 40, "Medium", self.font_tiny)
        self.btn_hard = Button(center_x + 100, 330, 150, 40, "Hard", self.font_tiny)
        self.btn_quit = Button(center_x - 100, 400, 200, 50, "Quit", self.font_small)
        
        # Game over buttons
        self.btn_restart = Button(center_x - 100, 350, 200, 50, "Restart", self.font_small)
        self.btn_menu = Button(center_x - 100, 420, 200, 50, "Main Menu", self.font_small)
    
    def handle_events(self):
        """Handle input events"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
            
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.PLAYING:
                    # Movement controls (Arrow keys + WASD)
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.turn(Direction.UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.turn(Direction.DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.turn(Direction.LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.turn(Direction.RIGHT)
                    
                    # Pause
                    elif event.key in (pygame.K_ESCAPE, pygame.K_p):
                        self.state = GameState.PAUSED
                
                elif self.state == GameState.PAUSED:
                    if event.key in (pygame.K_ESCAPE, pygame.K_p):
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        self.state = GameState.MENU
                
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
        
        # Handle menu interactions
        if self.state == GameState.MENU:
            if self.btn_play.update(mouse_pos, mouse_clicked):
                self.start_game()
            elif self.btn_easy.update(mouse_pos, mouse_clicked):
                self.difficulty = Difficulty.EASY
            elif self.btn_medium.update(mouse_pos, mouse_clicked):
                self.difficulty = Difficulty.MEDIUM
            elif self.btn_hard.update(mouse_pos, mouse_clicked):
                self.difficulty = Difficulty.HARD
            elif self.btn_quit.update(mouse_pos, mouse_clicked):
                self.running = False
        
        elif self.state == GameState.GAME_OVER:
            if self.btn_restart.update(mouse_pos, mouse_clicked):
                self.start_game()
            elif self.btn_menu.update(mouse_pos, mouse_clicked):
                self.state = GameState.MENU
    
    def start_game(self):
        """Start new game"""
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        self.particles.clear()
        self.state = GameState.PLAYING
        self.new_high_score = False
        self.game_start_time = pygame.time.get_ticks()
    
    def update(self):
        """Update game logic"""
        if self.state == GameState.PLAYING:
            # Update move timer
            self.move_timer += 1
            
            if self.move_timer >= (FPS // self.difficulty.speed):
                self.move_timer = 0
                
                # Move snake
                if not self.snake.move():
                    # Game over
                    self.state = GameState.GAME_OVER
                    self.new_high_score = self.high_score_manager.update_score(
                        self.difficulty.display_name,
                        self.snake.score
                    )
                    return
                
                # Check food collision
                if self.snake.get_head_position() == self.food.position:
                    self.snake.grow()
                    self.snake.score += int(10 * self.difficulty.food_multiplier)
                    
                    # Create particles
                    fx, fy = self.food.position
                    for _ in range(15):
                        self.particles.append(Particle(fx + GRID_SIZE // 2, fy + GRID_SIZE // 2, Colors.PARTICLE))
                    
                    self.food.randomize_position(self.snake.positions)
            
            # Update food animation
            self.food.update()
        
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
    
    def draw_grid(self):
        """Draw background grid"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = Colors.GRID_DARK if (x + y) % 2 == 0 else Colors.GRID_LIGHT
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, color, rect)
    
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(Colors.BACKGROUND)
        
        # Title
        title = self.font_large.render("SNAKE", True, Colors.TEXT_ACCENT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_tiny.render("Professional Edition", True, Colors.TEXT_SECONDARY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 170))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Difficulty selection label
        diff_label = self.font_tiny.render("Select Difficulty:", True, Colors.TEXT_PRIMARY)
        diff_rect = diff_label.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(diff_label, diff_rect)
        
        # Highlight selected difficulty
        if self.difficulty == Difficulty.EASY:
            pygame.draw.rect(self.screen, Colors.TEXT_ACCENT, self.btn_easy.rect, 3, border_radius=10)
        elif self.difficulty == Difficulty.MEDIUM:
            pygame.draw.rect(self.screen, Colors.TEXT_ACCENT, self.btn_medium.rect, 3, border_radius=10)
        elif self.difficulty == Difficulty.HARD:
            pygame.draw.rect(self.screen, Colors.TEXT_ACCENT, self.btn_hard.rect, 3, border_radius=10)
        
        # Draw buttons
        self.btn_play.draw(self.screen)
        self.btn_easy.draw(self.screen)
        self.btn_medium.draw(self.screen)
        self.btn_hard.draw(self.screen)
        self.btn_quit.draw(self.screen)
        
        # High scores
        y_offset = 500
        hs_title = self.font_small.render("High Scores", True, Colors.TEXT_PRIMARY)
        hs_rect = hs_title.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        self.screen.blit(hs_title, hs_rect)
        
        y_offset += 40
        for diff in [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]:
            score = self.high_score_manager.get_high_score(diff.display_name)
            text = self.font_tiny.render(f"{diff.display_name}: {score}", True, Colors.TEXT_SECONDARY)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
    
    def draw_game(self):
        """Draw game screen"""
        self.draw_grid()
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw HUD
        score_text = self.font_medium.render(f"Score: {self.snake.score}", True, Colors.TEXT_PRIMARY)
        self.screen.blit(score_text, (20, 20))
        
        # High score
        high_score = self.high_score_manager.get_high_score(self.difficulty.display_name)
        hs_text = self.font_small.render(f"Best: {high_score}", True, Colors.TEXT_SECONDARY)
        self.screen.blit(hs_text, (20, 70))
        
        # Difficulty
        diff_text = self.font_tiny.render(f"Difficulty: {self.difficulty.display_name}", True, Colors.TEXT_SECONDARY)
        self.screen.blit(diff_text, (SCREEN_WIDTH - 200, 20))
        
        # Food count
        food_text = self.font_tiny.render(f"Food: {self.snake.food_eaten}", True, Colors.TEXT_SECONDARY)
        self.screen.blit(food_text, (SCREEN_WIDTH - 200, 50))
        
        # Controls hint
        hint = self.font_tiny.render("ESC/P: Pause", True, Colors.TEXT_SECONDARY)
        self.screen.blit(hint, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30))
    
    def draw_pause(self):
        """Draw pause overlay"""
        self.draw_game()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, Colors.TEXT_ACCENT)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        resume_text = self.font_small.render("Press ESC/P to Resume", True, Colors.TEXT_PRIMARY)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(resume_text, resume_rect)
        
        quit_text = self.font_small.render("Press Q for Main Menu", True, Colors.TEXT_SECONDARY)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.draw_grid()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, Colors.FOOD)
        go_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(game_over_text, go_rect)
        
        # New high score
        if self.new_high_score:
            new_hs_text = self.font_medium.render("NEW HIGH SCORE!", True, Colors.TEXT_ACCENT)
            new_hs_rect = new_hs_text.get_rect(center=(SCREEN_WIDTH // 2, 210))
            self.screen.blit(new_hs_text, new_hs_rect)
        
        # Stats
        y_offset = 270
        stats = [
            f"Final Score: {self.snake.score}",
            f"Food Eaten: {self.snake.food_eaten}",
            f"Snake Length: {self.snake.length}",
            f"Difficulty: {self.difficulty.display_name}"
        ]
        
        for stat in stats:
            stat_text = self.font_small.render(stat, True, Colors.TEXT_PRIMARY)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(stat_text, stat_rect)
            y_offset += 40
        
        # Buttons
        self.btn_restart.draw(self.screen)
        self.btn_menu.draw(self.screen)
        
        # Hint
        hint = self.font_tiny.render("SPACE: Restart | ESC: Menu", True, Colors.TEXT_SECONDARY)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(hint, hint_rect)
    
    def draw(self):
        """Draw current game state"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_pause()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point"""
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()
