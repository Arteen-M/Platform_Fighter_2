# -------------------------------------------------------------------------
# IMPORTS (and 1 variable)
# -------------------------------------------------------------------------
import pygame
RED = (255, 0, 0)


# -------------------------------------------------------------------------
# Class definition
# -------------------------------------------------------------------------
class HitBox(pygame.sprite.Sprite):
    def __init__(self, size, display, lag, start_flag, end_flag, direction, angle, damage, base, scale, hitstun, color=RED):
        super().__init__()
        # Hitbox size and position
        self.surf = pygame.Surface(size)
        self.surf.set_alpha(100)  # Drawn with transparency, to indicate that it is a hitbox, not hurtbox
        self.rect = self.surf.get_rect(center=(0, 0))  # Default center is (0, 0)
        self.surf.fill(color)  # Fill it with color

        # Properties
        self._lag = lag  # Total Run Time (and lag time)
        self.start_flag = start_flag  # When the move starts  (lag - frames)
        self.end_flag = end_flag  # When the move ends (frames)

        # Variables
        self.count = self._lag  # The amount of time left in the attack
        self._active = False  # If the moves hitbox is active (in between start_flag and end_flag)
        self.running = False  # If the attack is running (lag is counting down)
        self._direction = direction  # What modifier to apply to the hitbox's x-knockback

        self.x_component = angle[0]  # Modifier to apply to the x-knockback (in a percentage)
        self.y_component = angle[1]  # Modifier to apply to the y-knockback
        self.damage = damage  # Damage the move does
        self.base_knockback = base  # Knockback independent of percentage
        self.knockback_scale = scale  # Knockback dependent on percentage
        self.hitstun = hitstun  # Minimum hitstun an attack can deal

        self.display = display

    # Outside classes need these variables, so I encapsulated them, but they are changed within the class only
    @property
    def lag(self):
        return self._lag

    @property
    def active(self):
        return self._active

    # Update the hitbox (when it's running)
    def update(self, pos):
        self.running = True  # The attack is running
        self.rect = self.surf.get_rect(center=pos)  # Update the hitbox position (center is easiest)

        # When to activate and deactivate the hitbox
        if self.count == self.start_flag:
            self._active = True
        if self.count == self.end_flag:
            self._active = False

        # Lag goes down every frame
        self.count -= 1

        # When it gets to 0
        if self.count <= 0:
            self.reset()  # Reset the hitbox

        # If it's active, draw the hitbox
        if self._active:
            self.draw()

    # Direction is influenced by outside functions
    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    # Draw the hitbox
    def draw(self):
        self.display.blit(self.surf, self.rect)

    # Reset the variable attributes
    def reset(self):
        self.count = self._lag
        self._active = False
        self.running = False
