"""
next_page = “”
time = 0
stocks = 0
while True:
	if next_page == “settings”:
		next_page, time, stocks = settings()
	elif next_page == “Character Select”:
		next_page = characterSelection()
	elif next_page == “Game”:
		gameLoop(time, stocks)
		next_page = “Character Select”
	else:
        next_page = welcome()
"""
