from Pages import game
from Pages import welcome

next_page = ""
time = 1
stocks = 3

while True:
    if next_page == "Settings":
        next_page, time, stocks = ["Game", None, None]
    elif next_page == "Character Select":
        next_page = "Game"
    elif next_page == "Game":
        game.gameLoop(time, stocks)
        next_page = "Character Select"
    else:
        next_page = welcome.startScreen()
