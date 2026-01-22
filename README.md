# Dinosaur Run

A Chrome dinosaur-style endless runner game built with Pygame.

## How to Play

- **Space** or **Up Arrow**: Jump
- **Down Arrow**: Duck (hold to stay down)
- **Mouse Click**: Click replay button to restart after game over

## Features

- Animated dinosaur with running animation
- Cactus obstacles (big and small)
- Flying pterodactyl birds at two heights
- Ducking mechanic to avoid low-flying birds
- Scrolling ground and clouds
- Score tracking with persistent high score
- Game over screen with replay button

## Requirements

- Python 3.x
- Pygame

## Installation

```bash
pip install pygame
```

## Running the Game

```bash
python Dinasour.py
```

## Controls

| Key | Action |
|-----|--------|
| Space / Up | Jump |
| Down | Duck |
| Mouse Click | Restart (on game over) |

## Game Mechanics

- Jump over cacti and low birds
- Duck under low birds (or jump over them)
- High birds pass over the standing dinosaur - no action needed
- Score increases every frame while playing
- High score is saved to `high_score.txt`

## Sprites

Place the following sprites in the `sprites/` folder:
- `dino.png` - Dinosaur sprite sheet (3 frames)
- `cacti-big.png` - Big cactus sprite sheet
- `cacti-small.png` - Small cactus sprite sheet
- `ptera.png` - Pterodactyl sprite sheet (2 frames)
- `ground.png` - Ground/terrain image
- `replay_button.png` - Replay button icon
