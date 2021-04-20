import pygame
import random
from pygame.locals import (
    RLEACCEL,
)
from h_func import distance
from Base import Base


class Unit(Base):
    def __init__(self, screen, player, all_units, lasers_group):
        super().__init__(screen, player, all_units, lasers_group)
        self.units_group = all_units
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            player['color'],
            (5, 5), 5)
        self.orig_img = self.image.convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.player = player
        self.health = player['unit health']


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
        # self.center_p = self.rect.center
        # Selected units
        self.screen = screen
        self.color = player['color']
        self.selected = False

        # Move unit to x, y position
        self.pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.move_target = self.pos
        self.speed = player['Spd']
        self.moving = False

        # Setting attack target
        self.attack_target = None
        self.target_range = 50

        self.laser_range = player['laser range']

        # Attacking target
        self.attack_cooldown = player['Atk Spd']
        self.check_for_target = False
        self.attack_last = 2000

        # Which sprite group it belongs
        self.player_group = player['group']
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

    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount
        if self.health <= 0:
            self.player_dead()

    def player_dead(self):
        self.kill()


