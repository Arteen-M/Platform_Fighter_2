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
# Input: Keyboard and Mouse inputs
# Output: No distinct output (GUI)
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
from Pages import game
from Pages import welcome
from Pages import character_select
import pygame

# --------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
next_page = ""  # String to define where the program goes after returning from a page (Default Welcome)
time = 3  # Time in minutes (Default 3)
stocks = 3  # Stocks (Default 3)
characters = [None, None]  # Characters selected for each player
skins = [None, None]  # Skins for each player (attached to each character)
controls = None  # List of controls for each player
debug = False

# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
while True:
    # Character Select (Determines characters, skins and controls)
    if next_page == "Character Select":
        next_page, characters, skins, controls, time, stocks, debug = character_select.characterSelect()
    # Main game loop
    elif next_page == "Game":
        game.gameLoop(characters, controls, skins, time, stocks, debug)
        next_page = "Character Select"
    # Start Screen
    else:
        next_page = welcome.startScreen()
