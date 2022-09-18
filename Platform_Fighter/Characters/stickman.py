# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
from Platform_Fighter.Characters.Character_Elements import hitbox
import math
import time
from Platform_Fighter.path import path

# -------------------------------------------------------------------------
# Variable Definitions
# -------------------------------------------------------------------------
vec = pygame.math.Vector2
pygame.init()

WIDTH = 800
HEIGHT = 600
BOUND = 60

display = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
BLUE = (0, 0, 255)

GROUND_FRIC = -0.12  # Movement Resistance on the ground
AIR_FRIC = -0.12  # Movement Resistance in the air
MOMENTUM_FRIC = 0.01  # Movement Resistance during momentum


# -------------------------------------------------------------------------
# Class Definition
# -------------------------------------------------------------------------
class Stickman(pygame.sprite.Sprite):  # Inherit from the sprite class
    def __init__(self, display, color=RED, spawn_position=(WIDTH / 2, HEIGHT / 2),
                 controls=(K_LEFT, K_RIGHT, K_UP, K_DOWN, K_h), stocks=3):
        super().__init__()
        self.surf = pygame.Surface((30, 50))  # Surface (hurtbox) size
        self.image = pygame.image.load(path+"Images/Stickman/stickman.png").convert_alpha()
        self.rect = self.surf.get_rect(midbottom=spawn_position)  # Position (midbottom so it's easier to work with)
        self.image_rect = self.image.get_rect(midbottom=spawn_position)

        # Movement Constants
        self.gravity = 0.25  # Gravitational constant (previously 0.17)
        self.fall_speed = 7  # Fall Speed
        self.fast_fall = 8  # Fast Fall Speed
        self.ground_acc = 0.6  # Acceleration on the ground
        self.lag_ground_acc = 0.1  # Acceleration on the ground during attack lag
        self.current_ground_acc = self.ground_acc  # Switches between the two accelerations
        self.air_acc = 0.45  # Acceleration in the air
        self.lag_air_acc = 0.4  # Acceleration in the air during attack lag
        self.current_air_acc = self.air_acc  # Switches between the two accelerations
        self.momentum_acc = 0.1  # Acceleration (Resistance) during momentum
        self.jump_acc = -5.0  # Acceleration after jumping (previously -4.8)
        self.dash_speed = 10.0

        # Character Attributes
        self.percentage = 0.0  # Percentage (is a float but only increments in integers)
        self.stocks = stocks  # Stocks set to the default (typically 3)
        self.weight = 100  # Weight stat (100 is neutral, <100 is light, >100 is heavy)

        # Vectors
        self.pos = vec(self.rect.midbottom[0], self.rect.midbottom[1])  # Position Vector
        self.vel = vec(0, 0)  # Velocity Vector
        self.acc = vec(0, 0)  # Acceleration Vector

        self.display = display  # Display (for drawing)

        # Color for Skins
        self.color = color
        self.surf.fill(self.color)

        # Control Scheme
        self.controls = controls
        self.left = self.controls[0]
        self.right = self.controls[1]
        self.up = self.controls[2]
        self.down = self.controls[3]
        self.attack = self.controls[4]

        # Jump variables
        self.tapped_up = False  # Detect a jump press (only once per press)
        self.max_jumps = 4 + 1  # Maximum air jumps (previously 4)
        self.air_jumps = self.max_jumps  # Current jumps in the air

        self.max_dash = 2
        self.num_dash = 2

        # Character States
        self.on_ground = False  # On the ground or not
        self.on_plat = False  # On platform or not
        self.direction = True  # Which direction the character is facing (True = Right)
        self.pressed_down = 0
        self.pressed_left = 0
        self.pressed_right = 0
        self.going_down = False
        self.invincibility = 0  # If the character is currently invincible (usually on respawn)
        self.frozen = 0  # If the character can't move (with no influence) (usually on respawn)
        self.lag = 0  # Attack lag
        self.hitstun = 0  # Hitstun (after being hit by an opponent)
        self.hitstop = 0
        self.hitconfirm = 0
        self.momentum = 0  # Momentum (after you gain control from hitstun, but your momentum sticks around)
        self.knockback = vec(0, 0)  # Knockback Vector (x and y)
        self.got_hit = False
        self.crouching = False

        self.idle_frames_right = [pygame.image.load(path+"Images/Stickman/Idle Cycle/Idle_%d.png" % x).convert_alpha() for x in range(1, 73)]
        self.idle_cycle_right = 0

        self.idle_frames_left = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Idle Cycle/Idle_%d.png" % x), True, False).convert_alpha() for x in range(1, 73)]
        self.idle_cycle_left = 0

        self.walk_frames_right = [pygame.image.load(path+"Images/Stickman/Walk Cycle/Walk_%d.png" % x).convert_alpha() for x in range(1, 17)]
        self.walk_cycle_right = 0

        self.walk_frames_left = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Walk Cycle/Walk_%d.png" % x), True, False).convert_alpha() for x in range(1, 17)]
        self.walk_cycle_left = 0

        self.f_tilt_frames_right = [pygame.image.load(path+"Images/Stickman/Forward Tilt/stick_char_ftilt-%d.png" % (15 - x // 2)).convert_alpha() for x in range(2, 29)]
        self.f_tilt_cycle_right = 0

        self.f_tilt_frames_left = [pygame.transform.flip(pygame.image.load(path + "Images/Stickman/Forward Tilt/stick_char_ftilt-%d.png" % (15 - x // 2)), True, False).convert_alpha() for x in range(2, 29)]
        self.f_tilt_cycle_left = 0

        self.d_tilt_frames_right = [pygame.image.load(path+"Images/Stickman/Down Tilt/stick_char_dtilt-%d.png" % (7 - x // 2)).convert_alpha() for x in range(2, 12)]
        self.d_tilt_cycle_right = 0

        self.d_tilt_frames_left = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Down Tilt/stick_char_dtilt-%d.png" % (7 - x // 2)), True, False).convert_alpha() for x in range(2, 12)]
        self.d_tilt_cycle_left = 0

        self.up_tilt_frames_right = [pygame.image.load(path+"Images/Stickman/Up Tilt/stick_char_uptilt-%d.png" % (19 - x // 2)).convert_alpha() for x in range(2, 36)]
        self.up_tilt_cycle_right = 0

        self.up_tilt_frames_left = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Up Tilt/stick_char_uptilt-%d.png" % (19 - x // 2)), True, False).convert_alpha() for x in range(2, 36)]
        self.up_tilt_cycle_left = 0

        self.nair_frames_right = [pygame.image.load(path+"Images/Stickman/Neutral Air/Nair_%d.png" % x).convert_alpha() for x in range(0, 28)]
        self.nair_cycle_right = 0

        self.nair_frames_left = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Neutral Air/Nair_%d.png" % x), True, False).convert_alpha() for x in range(0, 28)]
        self.nair_cycle_left = 0

        self.fair_frames_right = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Forward Air/stick_char_fair-%d.png" % x), True, False).convert_alpha() for x in range(1, 19)]
        self.fair_cycle_right = 0

        self.fair_frames_left = [pygame.image.load(path+"Images/Stickman/Forward Air/stick_char_fair-%d.png" % x).convert_alpha() for x in range(1, 19)]
        self.fair_cycle_left = 0

        self.up_air_frames_right = [pygame.image.load(path+"Images/Stickman/Up Air/stick_char_upair-%d.png" % (9 - x // 2)).convert_alpha() for x in range(2, 18)]
        self.up_air_cycle_right = 0

        self.up_air_frames_left = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Up Air/stick_char_upair-%d.png" % (9 - x // 2)), True, False).convert_alpha() for x in range(2, 18)]
        self.up_air_cycle_left = 0

        self.dair_frames_right = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Down Air/stick_char_dair-%d.png" % (x // 2)), True, False).convert_alpha() for x in range(2, 21)]
        self.dair_cycle_right = 0

        self.dair_frames_left = [pygame.image.load(path+"Images/Stickman/Down Air/stick_char_dair-%d.png" % (x // 2)).convert_alpha() for x in range(2, 21)]
        self.dair_cycle_left = 0

        self.bair_frames_right = [pygame.image.load(path+"Images/Stickman/Back Air/stick_char_bair-%d.png" % (14 - x // 2)).convert_alpha() for x in range(2, 28)]
        self.bair_cycle_right = 0

        self.bair_frames_left = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Back Air/stick_char_bair-%d.png" % (14 - x // 2)), True, False).convert_alpha() for x in range(2, 28)]
        self.bair_cycle_left = 0

        self.air_image_right = pygame.image.load(path+"Images/Stickman/Walk Cycle/Walk_16.png").convert_alpha()
        self.air_image_left = pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Walk Cycle/Walk_16.png"), True, False).convert_alpha()

        self.hurt_image_right = pygame.image.load(path+"Images/Stickman/Hitstun/stick_char_hitstun-1.png").convert_alpha()
        self.hurt_image_left = pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Hitstun/stick_char_hitstun-1.png"), True, False).convert_alpha()

        self.crouch_image_right = pygame.image.load(path+"Images/Stickman/Crouch/stick_char_crouch-2.png").convert_alpha()
        self.crouch_image_left = pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Crouch/stick_char_crouch-2.png"), True, False).convert_alpha()

        self.nair_image_skew = (0, 25)
        self.fair_image_skew = (0, 15)
        self.up_air_image_skew = (0, 0)
        self.dair_image_skew = (0, 0)
        self.bair_image_skew = (0, 0)
        self.f_tilt_image_skew = (0, 0)
        self.d_tilt_image_skew = (0, 0)
        self.up_tilt_image_skew = (0, 0)
        self.crouch_image_skew = (0, 0)

        self.nair_count = 0  # MAX IS 4

        # Hitboxes for each usable attack
        #                                name      size       display   lag  sf  ef dir  angle    dmg b  s  hitstun  color
        self.ng_attack = hitbox.HitBox("Neutral", (60, 30), self.display, 28, 24, 2, 1, (0.5, 0.5), 5, 1, 0.2, 10, self.color)
        self.nair_attack1 = hitbox.HitBox("Neutral", (60, 30), self.display, 10, 6, 2, 1, (0, 0.5), 1, 1, 0.2, 10, self.color)
        self.nair_attack2 = hitbox.HitBox("Neutral", (60, 30), self.display, 10, 6, 2, 1, (0.1, 0.1), 1, 1, 0.2, 10, self.color)
        self.nair_final = hitbox.HitBox("Neutral", (60, 30), self.display, 16, 8, 1, 1, (0.5, 0.5), 5, 1, 0.2, 10, self.color)
        self.f_tilt_attack = hitbox.HitBox("Forward", (40, 20), self.display, 28, 14, 8, 1, (0.6, 0.4), 7, 1.5, 0.2, 10, self.color)
        self.f_air_attack = hitbox.HitBox("Forward", (60, 30), self.display, 28, 24, 18, 1, (0.6, 0.4), 7, 1.5, 0.2, 10, self.color)
        self.b_attack = hitbox.HitBox("Back", (30, 20), self.display, 28, 10, 4, 1, (-0.65, 0.35), 8, 1, 0.2, 10, self.color)
        self.up_tilt_attack1 = hitbox.HitBox("Up", (30, 30), self.display, 20, 14, 10, 1, (-0.5, 0.5), 5, 5, 0, 10, self.color)
        self.up_tilt_attack2 = hitbox.HitBox("Up", (30, 30), self.display, 20, 14, 10, 1, (0.5, 0.5), 5, 5, 0, 10, self.color)
        self.up_tilt_final = hitbox.HitBox("Up", (15, 50), self.display, 16, 15, 5, 1, (0, 1), 4, 1.2, 0.3, 10, self.color)
        self.u_air_attack = hitbox.HitBox("Up", (40, 40), self.display, 16, 10, 5, 1, (0.15, 0.7), 4, 1.2, 0.3, 10, self.color)
        self.d_tilt_attack = hitbox.HitBox("Down", (30, 20), self.display, 12, 4, 1, 1, (0.35, 0.65), 3, 2, 0.1, 10, self.color)
        self.dair_attack = hitbox.HitBox("Down", (40, 30), self.display, 20, 15, 5, 1, (0.05, -0.6), 10, 1.5, 0.3, 10, self.color)


        # Hitbox groups
        self.all_hitboxes = [self.ng_attack, self.nair_attack1, self.nair_attack2, self.nair_final, self.f_tilt_attack, self.f_air_attack, self.b_attack, self.u_air_attack, self.up_tilt_attack1, self.up_tilt_attack2, self.up_tilt_final, self.d_tilt_attack, self.dair_attack]
        self.active_hitboxes = pygame.sprite.Group()

        self.image_skew = (0, 0)

        # End Game condition
        self.end = False

    # Draw the current
    def draw(self):
        self.display.blit(self.surf, self.rect)
        self.display.blit(self.image, self.image_rect)

    def countHitstop(self):
        if self.hitstop > 0 or self.hitconfirm > 0:
            if self.hitstop > 0:
                self.hitstop -= 1
            if self.hitconfirm > 0:
                self.hitconfirm -= 1

    # Reduce the attack lag by 1
    def countLag(self):
        if self.lag > 0:
            self.lag -= 1

    # Reduce the hitstun by 1
    def countHitstun(self):
        if self.hitstun > 0:
            self.hitstun -= 1

    # Reduce the momentum by 1
    def countMomentum(self):
        if self.momentum > 0:
            self.momentum -= 1

    # Reduce the invincibility by 1
    def countInvincibility(self):
        if self.invincibility > 0:
            self.invincibility -= 1

    # Reduce the frozen by 1
    def countFrozen(self):
        if self.frozen > 0:
            self.frozen -= 1

    def countPressedDown(self):
        if self.pressed_down > 0:
            self.pressed_down -= 1

    def countPressedLeft(self):
        if self.pressed_left > 0:
            self.pressed_left -= 1

    def countPressedRight(self):
        if self.pressed_right > 0:
            self.pressed_right -= 1

    def countWalkCycle(self):
        if self.direction:
            if self.walk_cycle_right > 0:
                self.walk_cycle_right -= 1
        else:
            if self.walk_cycle_left > 0:
                self.walk_cycle_left -= 1

    def walkCycleSet(self):
        if self.direction:
            if self.walk_cycle_right == 0:
                self.walk_cycle_right = len(self.walk_frames_right) - 1
        else:
            if self.walk_cycle_left == 0:
                self.walk_cycle_left = len(self.walk_frames_left) - 1

    def idleCycleSet(self):
        if self.on_ground and not (self.walk_cycle_right or self.walk_cycle_left):
            if self.direction:
                self.idle_cycle_left = 0
                if self.idle_cycle_right == 0:
                    self.idle_cycle_right = len(self.idle_frames_right) - 1
                else:
                    self.idle_cycle_right -= 1
            else:
                self.idle_cycle_right = 0
                if self.idle_cycle_left == 0:
                    self.idle_cycle_left = len(self.idle_frames_left) - 1
                else:
                    self.idle_cycle_left -= 1

    def ftiltCycleSet(self):
        if self.direction:
            if self.f_tilt_cycle_right == 0:
                self.f_tilt_cycle_right = len(self.f_tilt_frames_right) - 1
        else:
            if self.f_tilt_cycle_left == 0:
                self.f_tilt_cycle_left = len(self.f_tilt_frames_left) - 1

    def countFtiltCycle(self):
        if self.direction:
            if self.f_tilt_cycle_right > 0:
                self.f_tilt_cycle_right -= 1
        else:
            if self.f_tilt_cycle_left > 0:
                self.f_tilt_cycle_left -= 1

    def dtiltCycleSet(self):
        if self.direction:
            if self.d_tilt_cycle_right == 0:
                self.d_tilt_cycle_right = len(self.d_tilt_frames_right) - 1
        else:
            if self.d_tilt_cycle_left == 0:
                self.d_tilt_cycle_left = len(self.d_tilt_frames_left) - 1

    def countDtiltCycle(self):
        if self.direction:
            if self.d_tilt_cycle_right > 0:
                self.d_tilt_cycle_right -=1
        else:
            if self.d_tilt_cycle_left > 0:
                self.d_tilt_cycle_left -= 1

    def uptiltCycleSet(self):
        if self.direction:
            if self.up_tilt_cycle_right == 0:
                self.up_tilt_cycle_right = len(self.up_tilt_frames_right) - 1
        else:
            if self.up_tilt_cycle_left == 0:
                self.up_tilt_cycle_left = len(self.up_tilt_frames_left) - 1

    def countUptiltCycle(self):
        if self.direction:
            if self.up_tilt_cycle_right > 0:
                self.up_tilt_cycle_right -= 1
        else:
            if self.up_tilt_cycle_left > 0:
                self.up_tilt_cycle_left -= 1

    def nairCycleSet(self):
        if self.direction:
            if self.nair_cycle_right == 0:
                self.nair_cycle_right = len(self.nair_frames_right) - 1
        else:
            if self.nair_cycle_left == 0:
                self.nair_cycle_left = len(self.nair_frames_left) - 1

    def countNairCycle(self):
        if self.direction:
            if self.nair_cycle_right > 0:
                self.nair_cycle_right -= 1
        else:
            if self.nair_cycle_left > 0:
                self.nair_cycle_left -= 1

    def uairCycleSet(self):
        if self.direction:
            if self.up_air_cycle_right == 0:
                self.up_air_cycle_right = len(self.up_air_frames_right) - 1
        else:
            if self.up_air_cycle_left == 0:
                self.up_air_cycle_left = len(self.up_air_frames_left) - 1

    def countUairCycle(self):
        if self.direction:
            if self.up_air_cycle_right > 0:
                self.up_air_cycle_right -= 1
        else:
            if self.up_air_cycle_left > 0:
                self.up_air_cycle_left -= 1

    def fairCycleSet(self):
        if self.direction:
            if self.fair_cycle_right == 0:
                self.fair_cycle_right = len(self.fair_frames_right) - 1
        else:
            if self.fair_cycle_left == 0:
                self.fair_cycle_left = len(self.fair_frames_left) - 1

    def countFairCycle(self):
        if self.direction:
            if self.fair_cycle_right > 0:
                self.fair_cycle_right -= 1
        else:
            if self.fair_cycle_left > 0:
                self.fair_cycle_left -= 1

    def dairCycleSet(self):
        if self.direction:
            if self.dair_cycle_right == 0:
                self.dair_cycle_right = len(self.dair_frames_right) - 1
        else:
            if self.dair_cycle_left == 0:
                self.dair_cycle_left = len(self.dair_frames_left) - 1

    def countDairCycle(self):
        if self.direction:
            if self.dair_cycle_right > 0:
                self.dair_cycle_right -= 1
        else:
            if self.dair_cycle_left > 0:
                self.dair_cycle_left -= 1

    def bairCycleSet(self):
        if self.direction:
            if self.bair_cycle_right == 0:
                self.bair_cycle_right = len(self.bair_frames_right) - 1
        else:
            if self.bair_cycle_left == 0:
                self.bair_cycle_left = len(self.bair_frames_left) - 1

    def countBairCycle(self):
        if self.direction:
            if self.bair_cycle_right > 0:
                self.bair_cycle_right -= 1
        else:
            if self.bair_cycle_left > 0:
                self.bair_cycle_left -= 1

    # The formula for knockback (I stole this from SmashWiki)
    def knockbackFormula(self, angle, damage, scale, base, mod):
        velocity = mod * angle * (((((self.percentage / 10) + (self.percentage * (damage / 2) / 20) * (
                (200 / (self.weight + 100)) * 1.4) + 18) * scale) + base))
        return velocity

    # The formula for hitstun
    def hitstunFormula(self, velocity, hitstun, damage):
        return math.floor(
            velocity / (2 * self.gravity) - (2 * velocity) + (0.1 * self.percentage)) + hitstun + self.findHitstop(
            damage, 1)

    # The formula for hitstop
    @staticmethod
    def findHitstop(damage, multiplyer):
        return math.floor(((damage * 0.45) + 2) * multiplyer + 3)

    # Reset your attributes
    def reset(self):
        self.stocks -= 1
        self.percentage = 0.0
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.invincibility = 100
        self.frozen = self.invincibility - 50

    # Respawn conditions
    def respawn(self):
        # If you're in the blastzone
        if self.pos.x > WIDTH + BOUND or self.pos.x < -BOUND or self.pos.y < -BOUND or self.pos.y > HEIGHT + BOUND:
            # If the stocks is greater than 0
            if self.stocks > 0:
                # Reset
                self.reset()

    # Loss condition
    def endGame(self):
        if self.stocks == 0:
            self.end = True

    def platformCollide(self, soft_floors, under_floors):
        soft_floor_collide = pygame.sprite.spritecollide(self, soft_floors, False)
        under_floor_collide = pygame.sprite.spritecollide(self, under_floors, False)

        if soft_floor_collide and self.vel.y >= 0 and not under_floor_collide and not self.going_down:
            self.acc.y = 0
            self.vel.y = 0
            self.on_plat = True
            self.pos.y = soft_floor_collide[0].rect.top + 1
        else:
            self.acc.y = self.gravity
            self.on_plat = False

    # Floor collide check
    def floorCollide(self, floors):
        # Returns a list of floors where the rects overlap with self (Dokill = False)
        floor_collide = pygame.sprite.spritecollide(self, floors, False)

        # If floor_collide has an element, and you're moving downwards
        if floor_collide and self.vel.y >= 0:
            # Acceleration is 0, Velocity is 0, position is reset to the top of the floor
            self.acc.y = 0
            self.vel.y = 0
            self.pos.y = floor_collide[0].rect.top + 1
        else:
            # Gravity
            self.acc.y = self.gravity

    def goingDown(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[self.down] and 8 >= self.pressed_down > 0:
            self.going_down = True
            self.vel.y = self.fast_fall
        elif pressed_keys[self.down]:
            self.pressed_down = 10

    def dash(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[self.left] and 8 >= self.pressed_left > 0:
            self.vel.x = -1 * self.dash_speed
            self.vel.y = 0
        elif pressed_keys[self.left]:
            self.pressed_left = 10

        if pressed_keys[self.right] and 8 >= self.pressed_right > 0:
            self.vel.x = self.dash_speed
            self.vel.y = 0
        elif pressed_keys[self.right]:
            self.pressed_right = 10

    # def fastFall(self):
    #    if self.going_down:
    #        self.vel.y = self.fast_fall

    # Similar to the floor collide, but change the grounded state instead
    def stateChange(self, floors):
        # Returns a list of floors where the rects overlap with self (Dokill = False)
        floor_collide = pygame.sprite.spritecollide(self, floors, False)

        if floor_collide or self.on_plat:
            # If you hit the ground and weren't on the ground before
            if not self.on_ground:
                # Cancel lag and momentum
                self.lag = 0
                self.momentum = 0

                self.nair_cycle_right = 0
                self.nair_cycle_left = 0
                self.fair_cycle_right = 0
                self.fair_cycle_left = 0
                self.up_air_cycle_right = 0
                self.up_air_cycle_left = 0
                self.dair_cycle_right = 0
                self.dair_cycle_left = 0
                self.bair_cycle_right = 0
                self.bair_cycle_left = 0

                self.going_down = False
                # Reset any hitboxes
                for hitbox in self.all_hitboxes:
                    if self.active_hitboxes.has(hitbox):
                        self.active_hitboxes.remove(hitbox)
                        hitbox.reset()
                    if hitbox.running:
                        hitbox.reset()

            # If you hit the ground, you are on the ground
            self.on_ground = True
        else:
            # If you're on the ground then fall off
            if self.on_ground:
                # Cancel lag
                self.lag = 0
                # Reset any hitboxes
                for hitbox in self.all_hitboxes:
                    if self.active_hitboxes.has(hitbox):
                        self.active_hitboxes.remove(hitbox)
                        hitbox.reset()
                    if hitbox.running:
                        hitbox.reset()

            # You are now not on the ground
            self.on_ground = False

    # Change direction
    def directionChange(self):
        pressed_keys = pygame.key.get_pressed()
        # Can't change directions in the air
        if self.on_ground:
            # if you're pressing left
            if pressed_keys[self.left]:
                # Change directions
                self.direction = False
            # Otherwise if you're pressing right
            elif pressed_keys[self.right]:
                # Change directions
                self.direction = True

    def imageUpdate(self):
        if self.hitstun or self.hitstop:
            if self.direction:
                self.image = self.hurt_image_right
            else:
                self.image = self.hurt_image_left
        elif self.nair_cycle_right > 0 or self.nair_cycle_left > 0:
            self.image_skew = self.nair_image_skew
            if self.nair_cycle_right > 0:
                self.image = self.nair_frames_right[self.nair_cycle_right]
            elif self.nair_cycle_left > 0:
                self.image = self.nair_frames_left[self.nair_cycle_left]
        elif self.up_air_cycle_right > 0 or self.up_air_cycle_left > 0:
            self.image_skew = self.up_air_image_skew
            if self.up_air_cycle_right > 0:
                self.image = self.up_air_frames_right[self.up_air_cycle_right]
            elif self.up_air_cycle_left > 0:
                self.image = self.up_air_frames_left[self.up_air_cycle_left]
        elif self.fair_cycle_right > 0 or self.fair_cycle_left > 0:
            self.image_skew = self.fair_image_skew
            if self.fair_cycle_right > 0:
                self.image = self.fair_frames_right[self.fair_cycle_right]
            elif self.fair_cycle_left > 0:
                self.image = self.fair_frames_left[self.fair_cycle_left]
        elif self.dair_cycle_right > 0 or self.dair_cycle_left > 0:
            self.image_skew = self.dair_image_skew
            if self.dair_cycle_right > 0:
                self.image = self.dair_frames_right[self.dair_cycle_right]
            elif self.dair_cycle_left > 0:
                self.image = self.dair_frames_left[self.dair_cycle_left]
        elif self.bair_cycle_right > 0 or self.bair_cycle_left > 0:
            self.image_skew = self.bair_image_skew
            if self.bair_cycle_right > 0:
                self.image = self.bair_frames_right[self.bair_cycle_right]
            elif self.bair_cycle_left > 0:
                self.image = self.bair_frames_left[self.bair_cycle_left]
        elif self.f_tilt_cycle_right > 0 or self.f_tilt_cycle_left > 0:
            self.image_skew = self.f_tilt_image_skew
            if self.f_tilt_cycle_right > 0:
                self.image = self.f_tilt_frames_right[self.f_tilt_cycle_right]
            elif self.f_tilt_cycle_left > 0:
                self.image = self.f_tilt_frames_left[self.f_tilt_cycle_left]
        elif self.d_tilt_cycle_right > 0 or self.d_tilt_cycle_left > 0:
            self.image_skew = self.d_tilt_image_skew
            if self.d_tilt_cycle_right > 0:
                self.image = self.d_tilt_frames_right[self.d_tilt_cycle_right]
            elif self.d_tilt_cycle_left > 0:
                self.image = self.d_tilt_frames_left[self.d_tilt_cycle_left]
        elif self.up_tilt_cycle_right > 0 or self.up_tilt_cycle_left > 0:
            self.image_skew = self.up_tilt_image_skew
            if self.up_tilt_cycle_right > 0:
                self.image = self.up_tilt_frames_right[self.up_tilt_cycle_right]
            elif self.up_tilt_cycle_left > 0:
                self.image = self.up_tilt_frames_left[self.up_tilt_cycle_left]
        elif self.walk_cycle_right > 0 or self.walk_cycle_left > 0:
            self.image_skew = (0, 0)
            if self.walk_cycle_right > 0:
                self.image = self.walk_frames_right[self.walk_cycle_right]
            elif self.walk_cycle_left > 0:
                self.image = self.walk_frames_left[self.walk_cycle_left]
        elif not self.on_ground:
            self.image_skew = (0, 0)
            if self.direction:
                self.image = self.air_image_right
            else:
                self.image = self.air_image_left
        elif self.crouching:
            if self.direction:
                self.image = self.crouch_image_right
            else:
                self.image = self.crouch_image_left
        else:
            self.image_skew = (0, 0)
            self.idleCycleSet()
            if self.idle_cycle_right > 0:
                self.image = self.idle_frames_right[self.idle_cycle_right]
            elif self.idle_cycle_left > 0:
                self.image = self.idle_frames_left[self.idle_cycle_left]

        self.image_rect.midbottom = (self.pos.x + self.image_skew[0], self.pos.y + self.image_skew[1])

    def hurtboxShift(self):
        if self.fair_cycle_right or self.fair_cycle_left:
            if self.fair_cycle_right:
                self.surf = pygame.Surface((50, 30))
                self.rect = self.surf.get_rect(midbottom=(self.pos.x, self.pos.y - 18))
            else:
                self.surf = pygame.Surface((50, 30))
                self.rect = self.surf.get_rect(midbottom=(self.pos.x, self.pos.y - 18))
        elif self.crouching:
            self.surf = pygame.Surface((30, 40))
            self.rect = self.surf.get_rect(midbottom=self.pos)
        else:
            self.surf = pygame.Surface((30, 50))
            self.rect = self.surf.get_rect(midbottom=self.pos)

        self.surf.fill(self.color)

    def crouch(self):
        pressed_keys = pygame.key.get_pressed()

        if not self.lag and pressed_keys[self.down] and self.on_ground:
            self.crouching = True
        else:
            self.crouching = False

    # Horizontal Movements
    def move(self, walls):
        # Acceleration needs to be reset every frame
        self.acc.x = 0

        # If you aren't in lag
        if self.lag <= 0:
            # If you aren't in momentum
            if not self.momentum:
                # Normal acceleration
                self.current_ground_acc = self.ground_acc
                self.current_air_acc = self.air_acc
            else:
                # Momentum acceleration
                self.current_ground_acc = self.momentum_acc
                self.current_air_acc = self.momentum_acc
        else:
            # Lag acceleration
            self.current_ground_acc = self.lag_ground_acc
            self.current_air_acc = self.lag_air_acc

        # detect collision with self and walls (dokill = False)
        wall_collide = pygame.sprite.spritecollide(self, walls, False)

        pressed_keys = pygame.key.get_pressed()
        # If left and not hitting a wall
        if pressed_keys[self.left] and not wall_collide:
            # If you're on the ground
            if self.on_ground:
                # Increase acceleration (ground)
                self.acc.x -= self.current_ground_acc
                self.walkCycleSet()
            else:
                # Increase acceleration (air)
                self.acc.x -= self.current_air_acc
                self.walk_cycle_left = 0
        # If hitting left and the direction of a collided wall is not left
        # (assuming you'll only collide with 1 wall at a time)
        elif pressed_keys[self.left] and wall_collide[0].direction != "LEFT":
            if self.on_ground:
                self.acc.x -= self.current_ground_acc
                self.walkCycleSet()
            else:
                self.acc.x -= self.current_air_acc
                self.walk_cycle_left = 0
        # if you are colliding with the wall
        elif pressed_keys[self.left] and wall_collide:
            # If the walls direction is left
            if wall_collide[0].direction == "LEFT":
                # Stop all movement
                self.acc.x = 0
                self.vel.x = 0
        else:
            self.walk_cycle_left = 0

        # Very similar to the previous if statement, but with the directions reversed
        if pressed_keys[self.right] and not wall_collide:
            if self.on_ground:
                self.acc.x += self.current_ground_acc
                self.walkCycleSet()
            else:
                self.acc.x += self.current_air_acc
                self.walk_cycle_right = 0
        elif pressed_keys[self.right] and not wall_collide[0].direction == "RIGHT":
            if self.on_ground:
                self.acc.x += self.current_ground_acc
                self.walkCycleSet()
            else:
                self.acc.x += self.current_air_acc
                self.walk_cycle_right = 0
        elif pressed_keys[self.right] and wall_collide:
            if wall_collide[0].direction == "RIGHT":
                self.acc.x = 0
                self.vel.x = 0
        else:
            self.walk_cycle_right = 0

        # if you aren't in momentum
        if not self.momentum:
            # acceleration multiplier
            if self.on_ground:
                self.acc.x += self.vel.x * GROUND_FRIC
            else:
                self.acc.x += self.vel.x * AIR_FRIC
        else:
            # if you are in momentum, then lower your velocity by a bit
            self.vel.x *= 0.97

    # Resetting your vectors with a wall collide
    def wallCollide(self, walls):
        wall_collide = pygame.sprite.spritecollide(self, walls, False)

        # If your velocity is moving left (negative)
        if self.vel.x < 0 and wall_collide:
            # If the wall has the left property (stops you from moving left)
            if wall_collide[0].direction == "LEFT":
                # Stop acceleration and velocity
                self.acc.x = 0
                self.vel.x = 0

        # If your velocity is moving right (positive)
        if self.vel.y > 0 and wall_collide:
            # If the wall has the right property (stops you from moving right)
            if wall_collide[0].direction == "RIGHT":
                # Stops acceleration and velocity
                self.acc.x = 0
                self.vel.x = 0

    # Updates your acceleration, velocity and position
    def physicsUpdate(self):
        # Your velocity cannot exceed your fall speed
        if self.vel.y <= self.fall_speed:
            # Increase your velocity (based on acceleration)
            self.vel.y += self.acc.y
        # Update velocity by acceleration
        self.vel.x += self.acc.x
        # Update position
        self.pos += self.vel
        self.rect.midbottom = self.pos

    # when you jump
    def jump(self):
        if self.lag <= 0:  # if you aren't in attack lag
            if self.tapped_up and self.on_ground:  # If you are on the ground and pressed up
                self.acc.y = self.jump_acc  # Jump
                self.tapped_up = False  # Make sure you only press up once

            # If you are in the air and have available jumps
            if self.tapped_up and not self.on_ground and self.air_jumps > 0:
                self.going_down = False
                self.vel.y = 0  # Stop your airborne velocity
                self.acc.y = self.jump_acc  # Jump
                self.air_jumps -= 1  # One less air jump
                self.tapped_up = False  # No longer pressing up
            elif self.tapped_up and not self.on_ground and self.air_jumps <= 0:
                self.tapped_up = False  # Stop pressing up
        else:
            self.tapped_up = False  # Stop pressing up

        # Reset the number of jumps you have
        if self.on_ground:
            self.air_jumps = self.max_jumps

    # Set hitboxes into the active list, declaring them to the opponent
    def activeHitboxesSetter(self):
        for hitbox in self.all_hitboxes:  # Look through all the hitboxes
            if hitbox.count == hitbox.start_flag:  # When it first becomes active
                # Determine the direction of the hitbox (for the multiplier)
                if self.direction:
                    hitbox.direction = 1
                else:
                    hitbox.direction = -1
                # Add the hitbox to the active hitbox group
                self.active_hitboxes.add(hitbox)
            # Remove it if the hitbox becomes deactive and it is still in the group
            elif not hitbox.active and self.active_hitboxes.has(hitbox):
                self.active_hitboxes.remove(hitbox)

    def drawHitbox(self):
        for hitbox in self.all_hitboxes:
            if hitbox.active:
                hitbox.draw()

    # Neutral attack
    def neutralAttack(self):
        pressed_keys = pygame.key.get_pressed()

        # If you're attacking, and you're not in attack lag
        if pressed_keys[self.attack] and self.lag <= 0:
            # If you aren't pressing any other direction
            if not (pressed_keys[self.right] or pressed_keys[self.left] or pressed_keys[self.up] or pressed_keys[self.down]):
                self.nairCycleSet()
                # Update the hitbox position
                if self.on_ground:
                    self.ng_attack.update((self.pos.x, self.pos.y - 25))
                    # Set your attack lag
                    self.lag = self.ng_attack.lag
                else:
                    # Set your attack lag
                    self.nair_attack1.update((self.pos.x, self.pos.y - 25))
                    self.lag = self.nair_attack1.lag
        # If the hitbox is already running
        elif self.ng_attack.running:
            # Update the hitbox position
            self.ng_attack.update((self.pos.x, self.pos.y - 25))
        elif self.nair_attack1.running:
            self.nair_attack1.update((self.pos.x, self.pos.y - 25))

            if self.nair_attack1.count == 1:
                self.nair_attack2.update((self.pos.x, self.pos.y - 25))
                self.lag = self.nair_attack2.lag

        elif self.nair_attack2.running:
            self.nair_attack2.update((self.pos.x, self.pos.y - 25))

            if self.nair_attack2.count == 1:
                self.nair_final.update((self.pos.x, self.pos.y - 25))
                self.lag = self.nair_final.lag

        elif self.nair_final.running:
            self.nair_final.update((self.pos.x, self.pos.y - 25))

    # Forward attack
    def forwardAttack(self):
        pressed_keys = pygame.key.get_pressed()

        # If you're attacking, and you're not in attack lag
        if pressed_keys[self.attack] and self.lag <= 0:
            # If the pressed direction corresponds to the character direction
            if self.on_ground:
                if pressed_keys[self.right] and self.direction:
                    self.ftiltCycleSet()
                    # Update your lag and attack hitbox
                    self.f_tilt_attack.update((self.pos.x + 20, self.pos.y - 25))
                    self.lag = self.f_tilt_attack.lag

                # Same condition, but with the other side
                if pressed_keys[self.left] and not self.direction:
                    self.ftiltCycleSet()
                    # Update your lag and attack hitbox
                    self.f_tilt_attack.update((self.pos.x - 20, self.pos.y - 25))
                    self.lag = self.f_tilt_attack.lag
            else:
                if pressed_keys[self.right] and self.direction:
                    self.fairCycleSet()
                    # Update your lag and attack hitbox
                    self.f_air_attack.update((self.pos.x + 20, self.pos.y - 35))
                    self.lag = self.f_air_attack.lag

                # Same condition, but with the other side
                if pressed_keys[self.left] and not self.direction:
                    self.fairCycleSet()
                    # Update your lag and attack hitbox
                    self.f_air_attack.update((self.pos.x - 20, self.pos.y - 35))
                    self.lag = self.f_air_attack.lag
        # If the hitbox is already running
        elif self.f_tilt_attack.running:
            # Update the hitbox based on where it should go
            if self.direction:
                self.f_tilt_attack.update((self.pos.x + 20, self.pos.y - 25))
            else:
                self.f_tilt_attack.update((self.pos.x - 20, self.pos.y - 25))
        elif self.f_air_attack.running:
            # Update the hitbox based on where it should go
            if self.direction:
                self.f_air_attack.update((self.pos.x + 20, self.pos.y - 35))
            else:
                self.f_air_attack.update((self.pos.x - 20, self.pos.y - 35))

    # Back attack
    def backAttack(self):
        pressed_keys = pygame.key.get_pressed()

        # If you're attacking, and you're not in attack lag
        if pressed_keys[self.attack] and self.lag <= 0:
            # If your pressed direction and character direction are opposite
            if self.on_ground:
                pass
            else:
                if pressed_keys[self.right] and not self.direction:
                    self.bairCycleSet()
                    self.b_attack.update((self.pos.x + 35, self.pos.y - 25))
                    self.lag = self.b_attack.lag

                if pressed_keys[self.left] and self.direction:
                    self.bairCycleSet()
                    self.b_attack.update((self.pos.x - 35, self.pos.y - 25))
                    self.lag = self.b_attack.lag
        elif self.b_attack.running:
            if self.direction:
                self.b_attack.update((self.pos.x - 35, self.pos.y - 25))
            else:
                self.b_attack.update((self.pos.x + 35, self.pos.y - 25))

    # Up attack
    def upAttack(self):
        pressed_keys = pygame.key.get_pressed()
        # If you're attacking, and you're not in attack lag
        if pressed_keys[self.attack] and pressed_keys[self.up] and self.lag <= 0:
            if self.on_ground:
                self.uptiltCycleSet()
                if self.direction:
                    self.up_tilt_attack1.update((self.pos.x + 30, self.pos.y - 15))
                    self.up_tilt_attack2.update((self.pos.x - 30, self.pos.y - 15))
                else:
                    self.up_tilt_attack1.update((self.pos.x - 30, self.pos.y - 15))
                    self.up_tilt_attack2.update((self.pos.x + 30, self.pos.y - 15))
                self.lag = self.up_tilt_attack1.lag

            else:
                self.uairCycleSet()
                self.u_air_attack.update((self.pos.x, self.pos.y - 40))
                self.lag = self.u_air_attack.lag
        elif self.u_air_attack.running:
            self.u_air_attack.update((self.pos.x, self.pos.y - 40))
        elif self.up_tilt_attack1.running and self.up_tilt_attack2.running:
            if self.direction:
                self.up_tilt_attack1.update((self.pos.x + 30, self.pos.y - 15))
                self.up_tilt_attack2.update((self.pos.x - 30, self.pos.y - 15))
            else:
                self.up_tilt_attack1.update((self.pos.x - 30, self.pos.y - 15))
                self.up_tilt_attack2.update((self.pos.x + 30, self.pos.y - 15))

            if self.up_tilt_attack1.count == 1:
                self.up_tilt_final.update((self.pos.x, self.pos.y - 50))
                self.lag = self.up_tilt_final.lag
        elif self.up_tilt_final.running:
            self.up_tilt_final.update((self.pos.x,self.pos.y - 50))

    # Down attack
    def downAttack(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[self.attack] and pressed_keys[self.down] and self.lag <= 0:
            if self.on_ground:
                self.dtiltCycleSet()
                self.d_tilt_attack.update(self.pos)
                self.lag = self.d_tilt_attack.lag
            else:
                self.dairCycleSet()
                self.dair_attack.update(self.pos)
                self.lag = self.dair_attack.lag
        elif self.dair_attack.running:
            self.dair_attack.update(self.pos)
        elif self.d_tilt_attack.running:
            self.d_tilt_attack.update((self.pos.x - 10, self.pos.y - 10))

    # Detects and executes when you get hit
    def getHit(self, opponent_hitboxes):
        # A list of active hitboxes the opponent has  (Dokill = True)
        hit = pygame.sprite.spritecollide(self, opponent_hitboxes, True)
        # If one collides with you (at least 1)
        if hit:
            # Only accounts for the first hitbox you get hit by
            box = hit[0]
            self.got_hit = True

            for x in self.all_hitboxes:
                x.reset()
            self.active_hitboxes.empty()

            # Take the damage percentage of the hitbox
            self.percentage += box.damage

            # Take the knockback of the hitbox (individual to x and y)
            self.knockback.x = 1.5 * self.knockbackFormula(box.x_component, box.damage, box.knockback_scale,
                                                     box.base_knockback, 1)
            self.knockback.y = -1 * self.knockbackFormula(box.y_component, box.damage, box.knockback_scale,
                                                          box.base_knockback, 1)

            # Set your acceleration and velocity (reset and set)
            # self.acc = vec(box.direction * self.knockback.x / 10, self.knockback.y)
            self.vel = vec(box.direction * self.knockback.x, self.knockback.y)

            # calculate the players velocity in 1D (not as a vector)
            velocity = math.sqrt((self.knockback.x ** 2) + (self.knockback.y ** 2))
            # Set their hitstun and momentum based on the power of the attack
            self.hitstun = math.floor(self.hitstunFormula(velocity, box.hitstun, box.damage))
            self.hitstop = self.findHitstop(box.damage, 0.75)
            self.momentum = math.floor(self.hitstun / 2) + self.hitstun
            # self.momentum = math.floor(math.floor(self.hitstun * box.hitstun + 1) / 5)
        else:
            self.got_hit = False

    # Function containing all the previous ones, to run in one cycle
    def update(self, hard_floors, soft_floors, under_floors, walls, opponent_hitboxes):
        # RESPAWN/END FUNCTIONS (ALWAYS)
        self.respawn()
        self.endGame()

        # COUNTING FUNCTIONS (ALMOST ALWAYS)
        self.countHitstop()
        self.countInvincibility()
        self.countFrozen()

        if not self.hitstop and not self.hitconfirm:
            self.countLag()
            self.countHitstun()
            self.countMomentum()
            self.countPressedDown()
            self.countPressedLeft()
            self.countPressedRight()
            self.countWalkCycle()
            self.countNairCycle()
            self.countUairCycle()
            self.countFairCycle()
            self.countDairCycle()
            self.countBairCycle()
            self.countFtiltCycle()
            self.countDtiltCycle()
            self.countUptiltCycle()

        # CONDITIONAL MOVEMENT (CONDITIONAL)
        if not (self.frozen or self.lag or self.hitstun):
            if not self.momentum:
                self.goingDown()
                self.dash()

        if not self.frozen:  # Frozen is absolute
            # COLLISION FUNCTIONS (CONDITIONAL)
            self.floorCollide(hard_floors)
            self.platformCollide(soft_floors, under_floors)
            # self.goingDown()
            self.wallCollide(walls)
            # STATE CHANGES (CONDITIONAL)
            self.stateChange(hard_floors)
            if not (self.lag or self.hitstun):
                self.directionChange()
                self.crouch()
            # MOVEMENTS (CONDITIONAL)
            if not self.hitstun:
                self.move(walls)
                self.jump()

        if not self.frozen:
            if not self.hitstun:
                # ATTACKS (CONDITIONAL)
                # The order of the attacks indicates their priority in activation
                self.forwardAttack()
                self.backAttack()
                self.upAttack()
                self.downAttack()
                self.neutralAttack()
            # HITBOXES (CONDITIONAL)
            self.activeHitboxesSetter()
            # GETTING HIT (CONDITIONAL)
            if not self.invincibility:  # invincibility just means you can't get hit
                self.getHit(opponent_hitboxes)

        # ACC, VEL AND POS UPDATE (ALMOST ALWAYS)
        if not self.hitstop and not self.hitconfirm:
            self.physicsUpdate()

        # HURTBOX SHIFTING
        self.hurtboxShift()

        # ANIMATING (ALWAYS)
        self.drawHitbox()
        self.imageUpdate()
        self.draw()
