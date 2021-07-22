import torch
import pygame
import random
import numpy as np
# from game import SnakeGameAI, Direction, Point
# from model import Linear_QNet, QTrainer
# from helper import plot\
from Base import Base
from units_lasers import Unit


MID_ZONE = pygame.Rect(550, 865, 330, 500)
P1_ZONE = pygame.Rect(540, 860, 63, 200)
P2_ZONE = pygame.Rect(85, 240, 365, 535)
P3_ZONE = pygame.Rect(590, 795, 625, 740)
P4_ZONE = pygame.Rect(1113, 1300, 355, 515)


class BaseAI(Base):
    def __init__(self, screen, player, all_units, lasers_group, bases):
        super().__init__(screen, player, all_units, lasers_group, bases)
        self.pos = self.rect.centerx, self.rect.centery


    # def set_target(self, action):
    #     # [Attack Mid, Attack Player x3, Defend Base]
    #
    #     if np.array_equal(action, [1, 0, 0]):
    #         # if not self.rect.collidepoint(MID_ZONE):
    #         new_postion = pygame.Vector2(MID_ZONE.centerx, MID_ZONE.centery)
    #         self.moving = True
    #     elif np.array_equal(action, [0, 1, 0]):
    #         new_postion = pygame.Vector2(P1_ZONE.centerx, P1_ZONE.centery)
    #     elif np.array_equal(action, [0, 0, 1]):
    #         new_postion = pygame.Vector2(P2_ZONE.centerx, P2_ZONE.centery)
    #     elif np.array_equal(action, [1, 0, 1]):
    #         new_postion = pygame.Vector2(P3_ZONE.centerx, P3_ZONE.centery)
    #     elif np.array_equal(action, [1, 1, 1]):
    #         new_postion = pygame.Vector2(P4_ZONE.centerx, P4_ZONE.centery)
    #
    #     self.go_to = new_postion
    #
    #     self.move_target = pygame.Vector2(new_postion)

class UnitAI(BaseAI):
    def __init__(self, screen, player, all_units, lasers_group, bases):
        super().__init__(screen, player, all_units, lasers_group, bases)
        self.units_group = all_units
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            player['color'],
            (5, 5), 5)
        self.orig_img = self.image.convert()
        self.image.set_colorkey((0, 0, 0))
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
        # self.color = player['color']
        self.selected = False

        # Move unit to x, y position
        self.pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.move_target = self.pos
        self.speed = player['Spd']
        self.moving = False

        # Setting attack target
        # self.attack_target = None
        self.target_range = 50

        self.laser_range = player['laser range']

        # Attacking target
        self.attack_cooldown = player['Atk Spd']
        self.check_for_target = False
        self.attack_last = 2000

        # Which sprite group it belongs
        self.player_group = player['group']
        self.lasers_group = lasers_group
        self.bases = bases

    def update(self):
        self.move_to()
        if self.check_for_target:
            self.find_target()
            self.check_for_target = False

        self.attack()
        self.overlapped(self.bases)

    def set_target(self, action):
        # [Attack Mid, Attack Player x3, Defend Base]

        self.new_postion = self.rect.centerx, self.rect.centery

        if np.array_equal(action, [1, 0, 0]):
            # if not self.rect.collidepoint(MID_ZONE):
            self.new_postion = pygame.Vector2(MID_ZONE.centerx, MID_ZONE.centery)
            self.moving = True
        elif np.array_equal(action, [0, 1, 0]):
            self.new_postion = pygame.Vector2(P1_ZONE.centerx, P1_ZONE.centery)
            self.moving = True
        elif np.array_equal(action, [0, 0, 1]):
            self.new_postion = pygame.Vector2(P2_ZONE.centerx, P2_ZONE.centery)
            self.moving = True
        elif np.array_equal(action, [1, 0, 1]):
            self.new_postion = pygame.Vector2(P3_ZONE.centerx, P3_ZONE.centery)
            self.moving = True
        elif np.array_equal(action, [1, 1, 1]):
            self.new_postion = pygame.Vector2(P4_ZONE.centerx, P4_ZONE.centery)
            self.move_target = pygame.Vector2(P4_ZONE.centerx, P4_ZONE.centery)
            self.moving = True

        go_to = self.new_postion

        self.move_target = pygame.Vector2(go_to)


    def move_to(self):
        # [Attack Mid, Attack Player x3, Defend Base]
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

    def overlapped(self, group_to_skip):
        for unit in self.units_group:
            if unit is self:
                continue
            if unit in group_to_skip:
                continue
            if self.rect.colliderect(unit.rect):
                if self.rect.centerx == unit.rect.centerx:
                    self.pos = (self.rect.centerx - 10, self.rect.centery)
                    unit.pos = (self.rect.centerx, self.rect.centery)
                    self.move_target = pygame.Vector2((self.move_target[0] - 5, self.move_target[1] + 10))
                    unit.move_target = pygame.Vector2((unit.move_target[0] + 5, unit.move_target[1]))
