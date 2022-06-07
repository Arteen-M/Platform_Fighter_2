from Pages import game
from Pages import welcome
from Pages import character_select

next_page = ""
time = 1
stocks = 3
characters = [None, None]
skins = [None, None]
control_list = None


while True:
    if next_page == "Settings":
        next_page, time, stocks = ["Game", None, None]
    elif next_page == "Character Select":
        next_page, characters, skins, control_list = character_select.characterSelect()
    elif next_page == "Game":
        game.gameLoop(characters, control_list, skins, time, stocks)
        next_page = "Character Select"
    else:
        next_page = welcome.startScreen()
