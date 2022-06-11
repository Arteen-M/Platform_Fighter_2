import pygame
import pandas as pd
from Version_2.GUI_Elements import button
from Version_2.GUI_Elements import text
from Version_2.GUI_Elements.text import font

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
RED = (255, 0, 0)


# The dropdown for the names (only player 1 and 2 right now)
class nameDrop:
    def __init__(self, pos, display):
        self.font = font
        self.names = pd.read_csv("../Names/Names.csv").to_dict()
        if 'Unnamed: 0' in list(self.names.keys()):
            self.names.pop('Unnamed: 0')

        self.name = 'Player 1'
        self.controls = self.names[self.name]

        self.all_texts = []
        self.key_lists = list(self.names.keys())
        # self.key_lists.append("New Name")
        self.value_lists = list(self.names.values())
        # As many text items as there are names (in theory, an infinite amount)
        for count, name in enumerate(self.key_lists):
            self.all_texts.append(text.Text(name, self.font, 36, WHITE, (pos[0] + 100, pos[1] + 25 + (50 * (count + 1))), display))

        self.nameText = text.Text(self.name, self.font, 36, WHITE, (pos[0] + 100, pos[1]), display)
        self.pos = pos
        self.display = display

        # The dropdown button (triangle)
        self.button = button.Button(self.pos[0], self.pos[1] - 7, 30, 30, ((self.pos[0], self.pos[1]), (self.pos[0] + 30, self.pos[1]), (self.pos[0] + 15, self.pos[1] + 15)), GRAY, RED, self.display, rect=False, draw=True, border=False)
        # The buttons to select each name
        self.buttons_list = [
            button.Button(self.pos[0], self.pos[1] + (50 * (x + 1)), 200, 50, None, None, None, self.display, False, False, False) for x in range(len(self.key_lists))]

        self.pressed = False

    def update(self):
        # Update and draw the button/ text
        self.button.update()
        self.nameText.draw()

        # If pressed
        if self.button.pressed or self.pressed:
            # Keep it pressed until something else makes it false
            self.pressed = True
            # Draw
            pygame.draw.rect(self.display, BLACK, (self.pos[0], self.pos[1], 200, 50 * (len(self.names) + 1)))
            pygame.draw.rect(self.display, GRAY, (self.pos[0], self.pos[1], 200, 50 * (len(self.names) + 1)), 1)

            for count, name in enumerate(self.key_lists):
                self.buttons_list[count].update()
                if self.buttons_list[count].pressed:
                    # if it's not a new name
                    if name != "New Name":
                        self.name = name
                        self.controls = self.names[self.name]
                        self.nameText.update(self.name, self.nameText.pos)
                        self.pressed = False

                        # Return the new controls
                        return self.controls
                    else:
                        self.pressed = False

                # Draw all the names in the menu if it was pressed
                self.all_texts[count].draw()

        return None

    # Pressed detector
    def get_pressed(self, click):
        self.button.get_pressed(click)
        for x in self.buttons_list:
            x.get_pressed(click)

    # Write the controls to the file
    def saveControls(self, controls):
        self.names[self.name] = {0: controls[0], 1: controls[1], 2: controls[2], 3: controls[3], 4: controls[4]}
        df = pd.DataFrame(self.names)
        df.to_csv("../Names/Names.csv")
