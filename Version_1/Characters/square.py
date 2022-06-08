import pygame
from pygame.locals import *
from Version_1.Characters.Character_Elements import hitbox
import math

vec = pygame.math.Vector2
pygame.init()

WIDTH = 800
HEIGHT = 600
BOUND = 60

display = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
DARK_GRAY = (125, 125, 150)

GROUND_FRIC = -0.12
AIR_FRIC = -0.12
MOMENTUM_FRIC = 0.01


class Square(pygame.sprite.Sprite):
    def __init__(self, display, color=RED, spawn_position=(WIDTH / 2, HEIGHT / 2),
                 controls=(K_LEFT, K_RIGHT, K_UP, K_DOWN, K_h), stocks=3):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.rect = self.surf.get_rect(midbottom=spawn_position)

        self.gravity = 0.25  # 0.17
        self.fall_speed = 3.6
        self.fast_fall = 5.6
        self.ground_acc = 0.6
        self.lag_ground_acc = 0.1
        self.current_ground_acc = self.ground_acc
        self.air_acc = 0.45
        self.lag_air_acc = 0.4
        self.current_air_acc = self.air_acc
        self.momentum_acc = 0.1
        self.jump_acc = -5.0  # -4.8

        self.percentage = 0.0
        self.stocks = stocks
        self.weight = 100

        self.pos = vec(self.rect.midbottom[0], self.rect.midbottom[1])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.display = display

        self.color = color
        self.surf.fill(self.color)

        self.controls = controls
        self.left = self.controls[0]
        self.right = self.controls[1]
        self.up = self.controls[2]
        self.down = self.controls[3]
        self.attack = self.controls[4]

        self.tapped_up = False
        self.max_jumps = 4 + 1
        self.air_jumps = self.max_jumps

        self.on_ground = False
        self.direction = True  # True = Right
        self.invincibility = 0
        self.frozen = 0

        # size, display, lag, start_flag, end_flag, direction, angle, damage, base, scale, hitstun, color=RED
        self.n_attack = hitbox.HitBox((60, 60), self.display, 20, 15, 5, 1, (0.5, 0.5), 5, 1, 0.2, 5, self.color)
        self.f_attack = hitbox.HitBox((20, 20), self.display, 20, 15, 5, 1, (0.6, 0.4), 7, 1.5, 0.2, 3, self.color)
        self.b_attack = hitbox.HitBox((40, 15), self.display, 20, 15, 5, 1, (-0.65, 0.35), 8, 1, 0.2, 3, self.color)
        self.u_attack = hitbox.HitBox((40, 30), self.display, 20, 15, 5, 1, (0.15, 0.7), 4, 1.2, 0.3, 5, self.color)
        self.d_attack = hitbox.HitBox((50, 30), self.display, 20, 15, 5, 1, (0.05, -0.6), 10, 1.5, 0.3, 5, self.color)

        self.all_hitboxes = [self.n_attack, self.f_attack, self.b_attack, self.u_attack, self.d_attack]
        self.active_hitboxes = pygame.sprite.Group()

        self.lag = 0
        self.hitstun = 0
        self.max_hitstun = 0
        self.momentum = 0
        self.knockback = vec(0, 0)

        self.end = False

    def draw(self):
        self.display.blit(self.surf, self.rect)

    def countLag(self):
        if self.lag > 0:
            self.lag -= 1

    def countHitstun(self):
        if self.hitstun > 0:
            self.hitstun -= 1

    def countMomentum(self):
        if self.momentum > 0:
            self.momentum -= 1

    def countInvincibility(self):
        if self.invincibility > 0:
            self.invincibility -= 1

    def countFrozen(self):
        if self.frozen > 0:
            self.frozen -= 1

    def knockbackFormula(self, angle, damage, scale, base, mod):
        velocity = mod * angle * (((((self.percentage / 10) + (self.percentage * (damage / 2) / 20) * (
                (200 / (self.weight + 100)) * 1.4) + 18) * scale) + base))
        return velocity

    def hitstunFormula(self, velocity, hitstun, damage):
        return math.floor(
            velocity / (2 * self.gravity) - (2 * velocity) + (0.1 * self.percentage)) + hitstun + self.findHitstop(
            damage, 1)

    @staticmethod
    def findHitstop(damage, multiplyer):
        return math.floor(((damage * 0.45) + 2) * multiplyer + 3)

    def respawn(self):
        if self.pos.x > WIDTH + BOUND or self.pos.x < -BOUND or self.pos.y < -BOUND or self.pos.y > HEIGHT + BOUND:
            if self.stocks > 0:
                self.stocks -= 1
                self.percentage = 0.0
                self.acc = vec(0, 0)
                self.vel = vec(0, 0)
                self.pos = vec(WIDTH / 2, HEIGHT / 2)
                self.invincibility = 100
                self.frozen = self.invincibility - 50

    def endGame(self):
        if self.stocks == 0:
            self.end = True

    def floorCollide(self, floors):
        floor_collide = pygame.sprite.spritecollide(self, floors, False)

        if floor_collide and self.vel.y >= 0:
            self.acc.y = 0
            self.vel.y = 0
            self.pos.y = floor_collide[0].rect.top + 1
        else:
            self.acc.y = self.gravity

    def stateChange(self, floors):
        floor_collide = pygame.sprite.spritecollide(self, floors, False)

        if floor_collide:
            if not self.on_ground:
                self.lag = 0
                self.momentum = 0
                for hitBox in self.all_hitboxes:
                    if hitBox.active:
                        hitBox.reset()

            self.on_ground = True
        else:
            if self.on_ground:
                self.lag = 0
                # self.momentum = 0
                for hitBox in self.all_hitboxes:
                    if hitBox.active:
                        hitBox.reset()

            self.on_ground = False

    def directionChange(self):
        pressed_keys = pygame.key.get_pressed()
        if self.on_ground:
            if pressed_keys[self.left]:
                self.direction = False
            elif pressed_keys[self.right]:
                self.direction = True

    def move(self, walls):
        self.acc.x = 0

        if self.lag <= 0:
            if not self.momentum:
                self.current_ground_acc = self.ground_acc
                self.current_air_acc = self.air_acc
            else:
                self.current_ground_acc = self.momentum_acc
                self.current_air_acc = self.momentum_acc
        else:
            self.current_ground_acc = self.lag_ground_acc
            self.current_air_acc = self.lag_air_acc

        wall_collide = pygame.sprite.spritecollide(self, walls, False)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[self.left] and not wall_collide:
            if self.on_ground:
                self.acc.x -= self.current_ground_acc
            else:
                self.acc.x -= self.current_air_acc
        elif pressed_keys[self.left] and not wall_collide[0].direction == "LEFT":
            if self.on_ground:
                self.acc.x -= self.current_ground_acc
            else:
                self.acc.x -= self.current_air_acc
        elif pressed_keys[self.left] and wall_collide:
            if wall_collide[0].direction == "LEFT":
                self.acc.x = 0
                self.vel.x = 0

        if pressed_keys[self.right] and not wall_collide:
            if self.on_ground:
                self.acc.x += self.current_ground_acc
            else:
                self.acc.x += self.current_air_acc
        elif pressed_keys[self.right] and not wall_collide[0].direction == "RIGHT":
            if self.on_ground:
                self.acc.x += self.current_ground_acc
            else:
                self.acc.x += self.current_air_acc
        elif pressed_keys[self.right] and wall_collide:
            if wall_collide[0].direction == "RIGHT":
                self.acc.x = 0
                self.vel.x = 0

        if not self.momentum:
            if self.on_ground:
                self.acc.x += self.vel.x * GROUND_FRIC
            else:
                self.acc.x += self.vel.x * AIR_FRIC
        else:
            self.vel.x *= 0.97

    def wallCollide(self, walls):
        wall_collide = pygame.sprite.spritecollide(self, walls, False)

        if self.vel.x < 0 and wall_collide:
            if wall_collide[0].direction == "LEFT":
                self.acc.x = 0
                self.vel.x = 0

        if self.vel.y > 0 and wall_collide:
            if wall_collide[0].direction == "RIGHT":
                self.acc.x = 0
                self.vel.x = 0

    def physicsUpdate(self):
        self.vel.y += self.acc.y
        self.vel.x += self.acc.x
        self.pos.y += self.vel.y
        self.pos.x += self.vel.x
        self.rect.midbottom = self.pos

    def jump(self):
        if self.lag <= 0:
            if self.tapped_up and self.on_ground:
                self.acc.y = self.jump_acc
                self.tapped_up = False

            if self.tapped_up and not self.on_ground and self.air_jumps > 0:
                self.vel.y = 0
                self.acc.y = self.jump_acc
                self.air_jumps -= 1
                self.tapped_up = False
            elif self.tapped_up and not self.on_ground and self.air_jumps <= 0:
                self.tapped_up = False
        else:
            self.tapped_up = False

        if self.on_ground:
            self.air_jumps = self.max_jumps

    def activeHitboxesSetter(self):
        for hitbox in self.all_hitboxes:
            if hitbox.count == hitbox.start_flag:
                if self.direction:
                    hitbox.direction = 1
                else:
                    hitbox.direction = -1
                self.active_hitboxes.add(hitbox)
            elif not hitbox.active and self.active_hitboxes.has(hitbox):
                self.active_hitboxes.remove(hitbox)

    def neutralAttack(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[self.attack] and self.lag <= 0:
            if not (pressed_keys[self.right] or pressed_keys[self.left] or pressed_keys[self.up] or pressed_keys[self.down]):
                self.n_attack.update((self.pos.x, self.pos.y - 15))
                self.lag = self.n_attack.lag
        elif self.n_attack.running:
            self.n_attack.update((self.pos.x, self.pos.y - 15))

    def forwardAttack(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[self.attack] and self.lag <= 0:
            if pressed_keys[self.right] and self.direction:
                self.f_attack.update((self.pos.x + 30, self.pos.y - 15))
                self.lag = self.f_attack.lag

            if pressed_keys[self.left] and not self.direction:
                self.f_attack.update((self.pos.x - 30, self.pos.y - 15))
                self.lag = self.f_attack.lag
        elif self.f_attack.running:
            if self.direction:
                self.f_attack.update((self.pos.x + 30, self.pos.y - 15))
            else:
                self.f_attack.update((self.pos.x - 30, self.pos.y - 15))

    def backAttack(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[self.attack] and self.lag <= 0:
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

    def upAttack(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[self.attack] and self.lag <= 0:
            if pressed_keys[self.up]:
                self.u_attack.update((self.pos.x, self.pos.y - 30))
                self.lag = self.u_attack.lag
        elif self.u_attack.running:
            self.u_attack.update((self.pos.x, self.pos.y - 30))

    def downAttack(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[self.attack] and self.lag <= 0:
            if pressed_keys[self.down]:
                self.d_attack.update(self.pos)
                self.lag = self.d_attack.lag
        elif self.d_attack.running:
            self.d_attack.update(self.pos)

    def getHit(self, opponent_hitboxes):
        hit = pygame.sprite.spritecollide(self, opponent_hitboxes, True)
        if hit:
            box = hit[0]

            self.percentage += box.damage

            self.knockback.x = self.knockbackFormula(box.x_component, box.damage, box.knockback_scale,
                                                     box.base_knockback, 1)
            self.knockback.y = -1 * self.knockbackFormula(box.y_component, box.damage, box.knockback_scale,
                                                          box.base_knockback, 1)

            self.acc = vec(box.direction * self.knockback.x / 10, self.knockback.y)
            self.vel = vec(box.direction * self.knockback.x, self.knockback.y)

            velocity = math.sqrt((self.knockback.x ** 2) + (self.knockback.y ** 2))
            self.hitstun = math.floor(self.hitstunFormula(velocity, box.hitstun, box.damage))
            self.max_hitstun = self.hitstun
            self.momentum = math.floor(self.hitstun * math.ceil(box.hitstun) + 1)
            # print(self.hitstun, self.momentum)

    def update(self, hard_floors, walls, opponent_hitboxes):
        # RESPAWN/END FUNCTIONS (ALWAYS)
        self.respawn()
        self.endGame()
        # COUNTING FUNCTIONS (ALWAYS)
        self.countLag()
        self.countHitstun()
        self.countMomentum()
        self.countInvincibility()
        self.countFrozen()
        if not self.frozen:
            # COLLISION FUNCTIONS (CONDITIONAL)
            self.floorCollide(hard_floors)
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
                self.neutralAttack()
                self.forwardAttack()
                self.backAttack()
                self.upAttack()
                self.downAttack()
            # HITBOXES (CONDITIONAL)
            self.activeHitboxesSetter()
            # GETTING HIT (CONDITIONAL)
            if not self.invincibility:
                self.getHit(opponent_hitboxes)
        # ANIMATING (ALWAYS)
        self.draw()

        # if self.end:
        #     time.sleep(2)

        # if self.hitstun or self.momentum:
            # print(self.acc.x, self.vel.x)
            # time.sleep(1)