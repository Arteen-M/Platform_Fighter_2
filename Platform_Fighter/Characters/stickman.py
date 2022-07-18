# -------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------
import pygame
from pygame.locals import *
from Platform_Fighter.Characters.Character_Elements import hitbox
import math
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
        self.momentum = 0  # Momentum (after you gain control from hitstun, but your momentum sticks around)
        self.knockback = vec(0, 0)  # Knockback Vector (x and y)
        self.got_hit = False

        self.idle_frames_right = [pygame.image.load(path+"Images/Stickman/Idle Cycle/Idle_%d.png" % x).convert_alpha() for x in range(1, 73)]
        self.idle_cycle_right = 0

        self.idle_frames_left = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Idle Cycle/Idle_%d.png" % x), True, False).convert_alpha() for x in range(1, 73)]
        self.idle_cycle_left = 0

        self.walk_frames_right = [pygame.image.load(path+"Images/Stickman/Walk Cycle/Walk_%d.png" % x).convert_alpha() for x in range(1, 17)]
        self.walk_cycle_right = 0

        self.walk_frames_left = [pygame.transform.flip(pygame.image.load(path+"Images/Stickman/Walk Cycle/Walk_%d.png" % x), True, False).convert_alpha() for x in range(1, 17)]
        self.walk_cycle_left = 0

        self.NairFrames = [pygame.image.load(path+"Images/Stickman/Neutral Air/Nair_%d.png" % x).convert_alpha() for x in range(0, 28)]

        # Hitboxes for each usable attack
        #                                name      size       display   lag  sf  ef dir  angle    dmg b  s  hitstun  color
        self.n_attack = hitbox.HitBox("Neutral", (60, 60), self.display, 20, 15, 5, 1, (0.5, 0.5), 5, 1, 0.2, 5, self.color)
        self.f_attack = hitbox.HitBox("Forward", (20, 20), self.display, 20, 15, 5, 1, (0.6, 0.4), 7, 1.5, 0.2, 3, self.color)
        self.b_attack = hitbox.HitBox("Back", (40, 15), self.display, 20, 15, 5, 1, (-0.65, 0.35), 8, 1, 0.2, 3, self.color)
        self.u_attack = hitbox.HitBox("Up", (40, 30), self.display, 20, 15, 5, 1, (0.15, 0.7), 4, 1.2, 0.3, 5, self.color)
        self.d_attack = hitbox.HitBox("Down", (50, 30), self.display, 20, 15, 5, 1, (0.05, -0.6), 10, 1.5, 0.3, 5, self.color)

        # Hitbox groupss
        self.all_hitboxes = [self.n_attack, self.f_attack, self.b_attack, self.u_attack, self.d_attack]
        self.active_hitboxes = pygame.sprite.Group()

        # End Game condition
        self.end = False

    # Draw the current
    def draw(self):
        self.display.blit(self.surf, self.rect)
        self.display.blit(self.image, self.image_rect)

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

    def idleCycle(self):
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
        if self.walk_cycle_right > 0 or self.walk_cycle_left > 0:
            if self.walk_cycle_right > 0:
                self.image = self.walk_frames_right[self.walk_cycle_right]
            elif self.walk_cycle_left > 0:
                self.image = self.walk_frames_left[self.walk_cycle_left]
        else:
            self.idleCycle()
            if self.idle_cycle_right > 0:
                self.image = self.idle_frames_right[self.idle_cycle_right]
            elif self.idle_cycle_left > 0:
                self.image = self.idle_frames_left[self.idle_cycle_left]

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
        self.image_rect.midbottom = self.pos

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
                # Update the hitbox position
                self.n_attack.update((self.pos.x, self.pos.y - 15))
                # Set your attack lag
                self.lag = self.n_attack.lag
        # If the hitbox is already running
        elif self.n_attack.running:
            # Update the hitbox position
            self.n_attack.update((self.pos.x, self.pos.y - 15))

    # Forward attack
    def forwardAttack(self):
        pressed_keys = pygame.key.get_pressed()

        # If you're attacking, and you're not in attack lag
        if pressed_keys[self.attack] and self.lag <= 0:
            # If the pressed direction corresponds to the character direction
            if pressed_keys[self.right] and self.direction:
                # Update your lag and attack hitbox
                self.f_attack.update((self.pos.x + 30, self.pos.y - 15))
                self.lag = self.f_attack.lag

            # Same condition, but with the other side
            if pressed_keys[self.left] and not self.direction:
                # Update your lag and attack hitbox
                self.f_attack.update((self.pos.x - 30, self.pos.y - 15))
                self.lag = self.f_attack.lag
        # If the hitbox is already running
        elif self.f_attack.running:
            # Update the hitbox based on where it should go
            if self.direction:
                self.f_attack.update((self.pos.x + 30, self.pos.y - 15))
            else:
                self.f_attack.update((self.pos.x - 30, self.pos.y - 15))

    # Back attack
    def backAttack(self):
        pressed_keys = pygame.key.get_pressed()

        # If you're attacking, and you're not in attack lag
        if pressed_keys[self.attack] and self.lag <= 0:
            # If your pressed direction and character direction are opposite
            if pressed_keys[self.right] and not self.direction:
                self.b_attack.update((self.pos.x + 35, self.pos.y - 15))
                self.lag = self.b_attack.lag

            if pressed_keys[self.left] and self.direction:
                self.b_attack.update((self.pos.x - 35, self.pos.y - 15))
                self.lag = self.b_attack.lag
        elif self.b_attack.running:
            if self.direction:
                self.b_attack.update((self.pos.x - 35, self.pos.y - 15))
            else:
                self.b_attack.update((self.pos.x + 35, self.pos.y - 15))

    # Up attack
    def upAttack(self):
        pressed_keys = pygame.key.get_pressed()

        # If you're attacking, and you're not in attack lag
        if pressed_keys[self.attack] and self.lag <= 0:
            # If you're pressing up
            if pressed_keys[self.up]:
                self.u_attack.update((self.pos.x, self.pos.y - 30))
                self.lag = self.u_attack.lag
        elif self.u_attack.running:
            self.u_attack.update((self.pos.x, self.pos.y - 30))

    # Down attack
    def downAttack(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[self.attack] and self.lag <= 0:
            # if you're pressing down
            if pressed_keys[self.down]:
                self.d_attack.update(self.pos)
                self.lag = self.d_attack.lag
        elif self.d_attack.running:
            self.d_attack.update(self.pos)

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

            # Take the percentage damage of the hitbox
            self.percentage += box.damage

            # Take the knockback of the hitbox (individual to x and y)
            self.knockback.x = self.knockbackFormula(box.x_component, box.damage, box.knockback_scale,
                                                     box.base_knockback, 1)
            self.knockback.y = -1 * self.knockbackFormula(box.y_component, box.damage, box.knockback_scale,
                                                          box.base_knockback, 1)

            # Set your acceleration and velocity (reset and set)
            self.acc = vec(box.direction * self.knockback.x / 10, self.knockback.y)
            self.vel = vec(box.direction * self.knockback.x, self.knockback.y)

            # calculate the players velocity in 1D (not as a vector)
            velocity = math.sqrt((self.knockback.x ** 2) + (self.knockback.y ** 2))
            # Set their hitstun and momentum based on the power of the attack
            self.hitstun = math.floor(self.hitstunFormula(velocity, box.hitstun, box.damage))
            self.momentum = math.floor(self.hitstun * math.ceil(box.hitstun) + 1)
        else:
            self.got_hit = False

    # Function containing all the previous ones, to run in one cycle
    def update(self, hard_floors, soft_floors, under_floors, walls, opponent_hitboxes):
        # RESPAWN/END FUNCTIONS (ALWAYS)
        self.respawn()
        self.endGame()
        # COUNTING FUNCTIONS (ALWAYS)
        self.countLag()
        self.countHitstun()
        self.countMomentum()
        self.countInvincibility()
        self.countFrozen()
        self.countPressedDown()
        self.countPressedLeft()
        self.countPressedRight()
        self.countWalkCycle()

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
            # MOVEMENTS (CONDITIONAL)
            if not self.hitstun:
                self.move(walls)
                self.jump()

        # ACC, VEL AND POS UPDATE (ALWAYS)
        self.physicsUpdate()

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
        # ANIMATING (ALWAYS)
        self.drawHitbox()
        self.imageUpdate()
        self.draw()
