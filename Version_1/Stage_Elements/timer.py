# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import math
import time
from Version_1.GUI_Elements import text


# -------------------------------------------------------------------------
# Class Definition
# -------------------------------------------------------------------------
class Timer:
    def __init__(self, timer, font, size, color, pos, display):
        self.max_time = timer  # Max time (Default is 1 minute)
        self.timer = "%d:00" % timer  # Current Time (Str)
        self.start_time = time.time()  # Start time of the game
        self.font = font  # Font
        self.color = color  # Text Color (Associated with player)
        self.current_time = 0  # Updated Time
        self.min = 0  # Minutes Remaining
        self.sec = 0  # Seconds Remaining
        self.pos = pos  # Timer Position
        self.display = display  # Display
        self.time_out = False  # When Time Runs out (Becomes True)

        # Timer Text
        self.textTimer = text.Text(self.timer, self.font, size, self.color, self.pos, self.display)

    def update(self):
        self.current_time = time.time()  # Updates to new time

        # Updates the minutes and seconds
        self.min = (self.max_time * 60 - math.floor(self.current_time - self.start_time)) // 60
        self.sec = self.max_time * 60 - math.floor(self.current_time - self.start_time) - self.min * 60

        # print(self.min, self.sec)

        # Updates the Timer string
        if self.sec < 10:
            self.timer = "%d:0%d" % (self.min, self.sec)
        else:
            self.timer = "%d:%d" % (self.min, self.sec)

        # Updates the display and draws it
        self.textTimer.update(text=self.timer)
        self.textTimer.draw()

        # If the time is 0
        if self.min == 0 and self.sec == 0:
            self.time_out = True
        else:
            self.time_out = False

    # When you pause, the timer needs to pause as well. This simulates pausing by resetting the timer
    # to where it was before the pause. Since the timer works in real time (for accuracy),
    # I can't pause it traditionally
    def reInit(self):
        self.max_time = self.min + (self.sec / 60)  # Set the time back to a decimal number (EX: 1.5 = 1:30)
        self.start_time = time.time()  # Reset the start time

