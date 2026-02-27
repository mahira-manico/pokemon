"""
constant.py
Centralized configuration for game-wide settings, colors, and fonts.
This module ensures consistency across all screens and game logic.
"""

import pygame

# Initialize font module to allow font creation in this file
pygame.font.init()

# WINDOW SETTINGS
SCREEN_WIDTH= 1280
SCREEN_HEIGHT= 720

# COLOR PALETTE (RGB)
# Standard colors
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (200, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)

# UI/UX Specific colors
YELLOW= (255, 255, 0)
MAGENTA= (255, 0, 255)
CYAN= (0, 255, 255)
SKY_BLUE= (135, 206, 235)
ORANGE= (255, 165, 0)
FOREST_GREEN= (34, 139, 34)
CRIMSON= (220, 20, 60)
GOLD= (255, 215, 0) # Used for highlights and selections

# FONT SETTINGS
SMALL= 20
MEDIUM= 40
LARGE= 70

# Define global font styles used across the application
# FONT1: Used for titles and headers (Bold style)
# FONT2: Used for standard text and small UI labels (Solid style)
try:
    FONT1= pygame.font.Font("assets/fonts/bold_pokemon.ttf", 45)
    FONT2= pygame.font.Font("assets/fonts/solid_pokemon.ttf", SMALL)
except FileNotFoundError:
    # Fallback to system font if custom assets are missing
    print("Warning: Custom fonts not found. Using system fonts.")
    FONT1= pygame.font.SysFont("Arial", 45, bold=True)
    FONT2= pygame.font.SysFont("Arial", SMALL)