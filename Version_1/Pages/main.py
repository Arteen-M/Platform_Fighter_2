# -------------------------------------------------------------------------
# Program: Platform Fighter 2
# Author: Arteen Mirzaei
# Date: 2022-06-07
#
# Platform Fighter is exactly what it sounds like, a platform fighter akin to Super Smash Bros,
# where the objective is to knock your opponent off the screen (called a stage) and make them pass
# the death barrier (called the blast zone). You achieve this by using a collection of attacking,
# defending and movement options to dodge your opponent and attack them. Every time you or your
# opponent successfully attack, you will deal damage in the form of percentage. The more percentage
# your opponent accumulates, they become more susceptible to being launched (called knockback).
# Knock them out of the blast zone to eliminate their lives (known as stocks).
# Eliminate all their stocks to win.
#
#
# Input: Keyboard and Mouse inputs
# Output: No distinct output (GUI)
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
from Version_1.Pages import game
from Version_1.Pages import welcome
from Version_1.Pages import character_select

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
next_page = ""  # String to define where the program goes after returning from a page (Default Welcome)
time = 1  # Time in minutes (Default 1)
stocks = 3  # Stocks (Default 3)
characters = [None, None]  # Characters selected for each player
skins = [None, None]  # Skins for each player (attached to each character)
controls = None  # List of controls for each player


# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
while True:
    # Settings page (Not implemented)
    if next_page == "Settings":
        next_page, time, stocks = ["Game", None, None]
    # Character Select (Determines characters, skins and controls)
    elif next_page == "Character Select":
        next_page, characters, skins, controls = character_select.characterSelect()
    # Main game loop
    elif next_page == "Game":
        game.gameLoop(characters, controls, skins, time, stocks)
        next_page = "Character Select"
    # Start Screen
    else:
        next_page = welcome.startScreen()
