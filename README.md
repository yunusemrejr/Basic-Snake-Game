# Modern Snake Game - Professional Edition 🐍

A beautifully modernized version of the classic Snake game built with Python and Pygame. Features a professional UI, multiple difficulty levels, high score tracking, and smooth animations.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎮 Core Gameplay
- **Classic Snake Mechanics** - Eat food, grow longer, avoid hitting yourself
- **Smooth Controls** - Arrow keys or WASD for movement
- **Screen Wrapping** - Snake wraps around screen edges for continuous gameplay
- **Improved Collision Detection** - Fair and accurate collision system

### 🎨 Modern Visual Design
- **Dark Theme UI** - Professional color palette with gradient effects
- **Animated Elements** - Glowing food, particle effects, smooth transitions
- **Gradient Snake** - Beautiful color gradient from head to tail
- **Rounded Corners** - Modern, polished visual style
- **Grid Background** - Clean checkerboard pattern

### 🎯 Game Modes & Features
- **Three Difficulty Levels**:
  - **Easy** - Slower speed, higher score multiplier (1.2x)
  - **Medium** - Balanced gameplay (1.0x multiplier)
  - **Hard** - Fast-paced challenge (0.8x multiplier)
- **Pause System** - Press ESC or P to pause/resume
- **High Score Persistence** - Separate high scores for each difficulty level
- **Game Statistics** - Track score, food eaten, snake length, and more

### 📊 User Interface
- **Main Menu** - Clean menu with difficulty selection
- **In-Game HUD** - Score, high score, difficulty, and food counter
- **Pause Screen** - Semi-transparent overlay with instructions
- **Game Over Screen** - Detailed statistics and new high score notifications
- **Interactive Buttons** - Hover effects and smooth interactions

### 🎪 Visual Effects
- **Particle System** - Explosion effects when eating food
- **Glow Effects** - Pulsing glow around food items
- **Smooth Animations** - Polished movement and transitions
- **Shadow Effects** - Depth and dimension on UI elements

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Quick Install

1. **Clone or download this repository**
```bash
git clone <repository-url>
cd snake-game
```

2. **Install dependencies**
```bash
# Option 1: Use the install script
./install.sh

# Option 2: Manual installation
pip3 install -r requirements.txt
```

3. **Run the game**
```bash
python3 snake_game_modern.py
```

## 🎮 How to Play

### Controls
- **Arrow Keys** or **WASD** - Move the snake (Up, Down, Left, Right)
- **ESC** or **P** - Pause/Resume game
- **Q** - Return to main menu (from pause screen)
- **SPACE** - Restart game (from game over screen)
- **Mouse** - Navigate menus and click buttons

### Gameplay
1. **Start the game** - Click "Play" from the main menu
2. **Select difficulty** - Choose Easy, Medium, or Hard
3. **Control the snake** - Use arrow keys or WASD to move
4. **Eat food** - Guide the snake to the red glowing food
5. **Grow longer** - Each food item increases your length and score
6. **Avoid yourself** - Don't run into your own body
7. **Beat high scores** - Try to achieve the highest score for each difficulty!

### Scoring System
- **Easy Mode**: 12 points per food (1.2x multiplier)
- **Medium Mode**: 10 points per food (1.0x multiplier)
- **Hard Mode**: 8 points per food (0.8x multiplier)

## 📁 Project Structure

```
snake-game/
├── snake_game_modern.py    # Main game file (modern version)
├── snakeGame.py            # Original game file
├── Minimized.py            # Minimized original version
├── requirements.txt        # Python dependencies
├── install.sh             # Installation script
├── highscores.json        # High scores (auto-generated)
├── gameico.png            # Game icon
├── README.md              # This file
└── LICENSE                # License file
```

## 🎯 Game Features Breakdown

### State Management
The game uses a clean state machine with four states:
- **MENU** - Main menu with difficulty selection
- **PLAYING** - Active gameplay
- **PAUSED** - Game paused, can resume or quit
- **GAME_OVER** - Shows statistics and options to restart

### High Score System
- Scores are automatically saved to `highscores.json`
- Separate high scores for each difficulty level
- Timestamps for when high scores were achieved
- Persistent across game sessions

### Difficulty Levels
Each difficulty affects:
- **Snake Speed** - How fast the snake moves
- **Score Multiplier** - Points earned per food item
- **Challenge Level** - Overall game difficulty

## 🛠️ Technical Details

### Built With
- **Python 3.7+** - Programming language
- **Pygame 2.5.0+** - Game development library

### Code Features
- **Object-Oriented Design** - Clean class structure
- **Type Hints** - Modern Python typing for better code quality
- **Enums** - Type-safe game states and difficulty levels
- **JSON Persistence** - High score storage
- **Particle System** - Dynamic visual effects
- **Event-Driven Architecture** - Responsive input handling

### Performance
- **60 FPS** - Smooth rendering
- **Optimized Drawing** - Efficient rendering pipeline
- **Low Resource Usage** - Lightweight and fast

## 🎨 Customization

You can easily customize the game by modifying the `Colors` class in `snake_game_modern.py`:

```python
class Colors:
    BACKGROUND = (15, 15, 35)      # Background color
    SNAKE_HEAD = (100, 255, 150)   # Snake head color
    SNAKE_BODY = (50, 200, 100)    # Snake body color
    FOOD = (255, 80, 80)           # Food color
    # ... and more
```

## 🐛 Troubleshooting

### Pygame not found
```bash
pip3 install pygame
```

### Permission denied on install.sh
```bash
chmod +x install.sh
```

### Game runs too fast/slow
Adjust the difficulty level or modify the `FPS` constant in the code.

## 📝 Version History

### Version 2.0 (Modern Edition)
- Complete rewrite with modern Python practices
- Added menu system and game states
- Implemented difficulty levels
- Added high score persistence
- Enhanced visuals with particles and effects
- Improved collision detection
- Added pause functionality
- Professional UI design

### Version 1.0 (Original)
- Basic snake game functionality
- Simple graphics
- Score tracking
- Basic intro screen

## 🙏 Credits

**Original Version:**
- Based on tutorial by [Kite](https://www.youtube.com/watch?v=9bBgyOkoBQ0&ab_channel=Kite)
- Original author: Yunus Emre Vurgun (2022)

**Modern Edition:**
- Complete modernization and feature additions
- Professional UI/UX design
- Enhanced gameplay mechanics
- Advanced visual effects

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 🎮 Enjoy the Game!

Have fun playing Modern Snake Game! Try to beat your high scores and challenge yourself with different difficulty levels. 

**Pro Tips:**
- Start with Easy mode to learn the mechanics
- Plan your path ahead to avoid trapping yourself
- Use the pause feature to strategize
- Hard mode is for true Snake masters! 🏆

---

Made with ❤️ and Python
