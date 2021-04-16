import pygame
import random
from pygame.locals import (
    RLEACCEL,
)
import math

def distance(rect1, rect2):
    x1, y1 = rect1.center
    x1b, y1b = rect1.bottomright
    x2, y2 = rect2.topleft
    x2b, y2b = rect2.bottomright
    left = x2b < x1
    right = x1b < x2
    top = y2b < y1
    bottom = y1b < y2
    if bottom and left:
        return math.hypot(x2b-x1, y2-y1b)
    elif left and top:
        return math.hypot(x2b-x1, y2b-y1)
    elif top and right:
        return math.hypot(x2-x1b, y2b-y1)
    elif right and bottom:
        return math.hypot(x2-x1b, y2-y1b)
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif top:
        return y1 - y2b
    elif bottom:
        return y2 - y1b
    else:  # rectangles intersect
        return 0


class Base(pygame.sprite.Sprite):
    def __init__(self, screen, center_p, color, player_group, respawn_event):
        super(Base, self).__init__()
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (60 / 2, 60 / 2), 30)
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=center_p)
        self.color = color
        self.current_health = 200
        self.target_health = 1000
        self.maximum_health = 1000
        self.health_bar_length = 100
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.screen = screen
        self.health_change_speed = 4
        self.player_group = player_group
        self.respawn_event = respawn_event
        self.font = pygame.font.SysFont('comicsans', 30)

    def update(self):
        # self.basic_health()
        self.advanced_health()
        self.show_unit_numbers()

    def show_unit_numbers(self):
        self.text = self.font.render(str(len(self.player_group)-1), 1, (0,0,0))
        self.screen.blit(self.text, (self.rect.x + 20, self.rect.y + 20))

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.player_dead()

    def get_health(self, amount):
        print("gothealth")
        if self.target_health < self.maximum_health:

            self.target_health += amount
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health

    # def basic_health(self):
    #     pygame.draw.rect(self.screen, (255,0,0), (10,10, self.current_health/self.health_ratio, 25))
    #     pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, self.health_bar_length, 25), 4)

    def advanced_health(self):
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0, 255, 0)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / - self.health_ratio)
            transition_color = (255, 255, 0)

        health_bar_rect = pygame.Rect(self.rect.centerx - 50, self.rect.bottom + 5, self.current_health/self.health_ratio, 10)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, self.rect.bottom + 5, transition_width, 10)
        pygame.draw.rect(self.screen, (255,0,0), health_bar_rect)
        pygame.draw.rect(self.screen, transition_color,transition_bar_rect)
        pygame.draw.rect(self.screen, (255,255,255), (self.rect.centerx - 50, self.rect.bottom + 5, self.health_bar_length, 10), 1)

    def player_dead(self):
        self.kill()
        for unit in self.player_group:
            unit.kill()
        pygame.time.set_timer(self.respawn_event, 0)



class Unit(pygame.sprite.Sprite):
    def __init__(self, screen, player, color, speed, all_units_group, player_group, lasers_group):
        super(Unit, self).__init__()
        self.units_group = all_units_group
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            color,
            (5, 5), 5)
        self.orig_img = self.image.convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.player = player
        self.health = 1


        # Find spawn area
        self.left_width = player['base'].rect.centerx - 250
        self.right_width = player['base'].rect.centerx + 250
        self.top_height = player['base'].rect.centery - 95
        self.bot_height = player['base'].rect.centery + 95
        self.rect = self.image.get_rect(center=(
            random.randint(self.left_width, self.right_width),
            random.randint(self.top_height, self.bot_height),
        )
    )
        # Selected units
        self.screen = screen
        self.color = color
        self.selected = False

        # Move unit to x, y position
        self.pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.move_target = self.pos
        self.speed = speed
        self.moving = False

        # Setting attack target
        self.attack_target = None
        self.target_range = 50

        # Attacking target
        self.attack_cooldown = 2000
        self.check_for_target = False
        self.attack_last = 2000

        # Which sprite group it belongs
        self.player_group = player_group
        self.lasers_group = lasers_group

    def set_target(self, pos):
        self.move_target = pygame.Vector2(pos)

    def update(self):
        self.move_to()
        if self.check_for_target:
            self.find_target()
            self.check_for_target = False

        self.attack()

    def overlapped(self, group_to_skip):
        for unit in self.units_group:
            if unit is self:
                continue
            if unit in group_to_skip:
                continue
            if self.rect.colliderect(unit.rect):
                if self.rect.centerx == unit.rect.centerx:
                    self.pos = (self.rect.centerx - 2, self.rect.centery + 2)
                    unit.pos = (self.rect.centerx + 2, self.rect.centery - 2)
                    self.move_target = pygame.Vector2(self.pos)
                    unit.move_target = pygame.Vector2(unit.pos)

    def move_to(self):
        move = self.move_target - self.pos
        move_length = move.length()

        if self.moving:
            if move_length < self.speed:
                self.pos = self.move_target
            elif move_length != 0:
                move.normalize_ip()
                move = move * self.speed
                self.pos += move
            self.rect.topleft = list(int(v) for v in self.pos)

    def find_target(self):
        """finds new targets in range:
                for speed: only call this once every 200ms."""
        for enemy in self.units_group:
            if enemy in self.player_group:
                continue

            if distance(self.rect, enemy.rect) <= self.target_range:
                self.attack_target = pygame.Vector2(enemy.rect.center)
                return
            elif distance(self.rect, enemy.rect) > self.target_range:
                self.attack_target = None

        self.attack_target = None

    def shoot(self, target_shoot):
        dx = target_shoot[0] - self.rect.centerx
        dy = target_shoot[1] - self.rect.centery
        bullet = Laser(self.rect.centerx, self.rect.centery, dx, dy, self.units_group, self.player_group, self.player)
        self.lasers_group.add(bullet)

    def attack(self):
        """attack, if able.
        target exists? still alive? gun cooldown good?"""
        # if self.attack_target is None: return
        # if self.attack_target.health <= 0: return
        if not self.cooldown_ready(): return
        if self.attack_target:
            self.shoot(self.attack_target)

    def cooldown_ready(self):
        # gun ready to fire? has cooldown in MS elapsed.
        now = pygame.time.get_ticks()
        if now - self.attack_last >= self.attack_cooldown:
            self.attack_last = now
            return True
        return False

    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount
        if self.health <= 0:
            self.player_dead()

    def player_dead(self):
        self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, all_units, player_group, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            (255,255,255),
            (2, 2), 2)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.x = x
        self.y = y
        self.speed = 1
        self.laser_pos = pygame.math.Vector2(x, y)
        self.target_pos = pygame.math.Vector2(dx, dy).normalize()
        self.all_units = all_units
        self.player_group = player_group
        self.damage = 1
        self.player = player

    def update(self):
        self.laser_pos += self.target_pos * self.speed
        self.rect.center = (round(self.laser_pos.x), round(self.laser_pos.y))

        # Laser Range
        if self.rect.x > self.x + 100 or self.rect.x < self.x - 100:
            self.kill()
        if self.rect.y < self.y - 100 or self.rect.y > self.y + 100:
            self.kill()