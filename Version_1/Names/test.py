import pandas as pd
from pygame.locals import *

data = {"Player 1": {0:K_LEFT, 1:K_RIGHT, 2:K_UP, 3:K_DOWN, 4:K_h},
        "Player 2": {0:K_a, 1:K_d, 2:K_w, 3:K_s, 4:K_t}}

df = pd.DataFrame(data)
df.to_csv("Names.csv")


