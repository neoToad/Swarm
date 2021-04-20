import pygame
from pygame.locals import (
    RLEACCEL,
)
from h_func import distance
# from units_lasers import Laser


class Base(pygame.sprite.Sprite):
    def __init__(self, screen, player, all_units, lasers_group):
        super().__init__()
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(self.image, player['color'], (60 / 2, 60 / 2), 30)
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=player['base loc'])
        self.color = player['color']
        self.current_health = 200
        self.target_health = 1000
        self.maximum_health = 1000
        self.health_bar_length = 100
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.screen = screen
        self.health_change_speed = 4
        self.player_group = player['group']
        self.respawn_event = player['respawn event']
        self.font = pygame.font.SysFont('comicsans', 30)

        self.lasers_group = lasers_group
        self.player = player

        self.attack_target = None
        self.target_range = 300
        self.laser_range = 325
        self.attack_cooldown = 1500
        self.units_group = all_units

        self.check_for_target = False

        self.attack_last = 2000

    def update(self):
        # self.basic_health()
        self.advanced_health()
        self.show_unit_numbers()

        if self.check_for_target:
            self.find_target()
            self.check_for_target = False

        self.attack()

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

    def attack(self):
        """attack, if able.
        target exists? still alive? gun cooldown good?"""
        # if self.attack_target is None: return
        # if self.attack_target.health <= 0: return
        if not self.cooldown_ready(): return
        if self.attack_target:
            self.shoot(self.attack_target, self.player)

    def cooldown_ready(self):
        # gun ready to fire? has cooldown in MS elapsed.
        now = pygame.time.get_ticks()
        if now - self.attack_last >= self.attack_cooldown:
            self.attack_last = now
            return True
        return False

    def shoot(self, target_shoot, player):
        dx = target_shoot[0] - self.rect.centerx
        dy = target_shoot[1] - self.rect.centery
        bullet = Laser(self.rect.centerx, self.rect.centery, dx, dy, self.units_group, self.player_group, player, self.laser_range)
        self.lasers_group.add(bullet)


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, all_units, player_group, player, laser_range):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            (255,255,255),
            (2, 2), 2)
        self.start_rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.x = x
        self.y = y
        self.speed = 1
        self.laser_pos = pygame.math.Vector2(x, y)
        self.target_pos = pygame.math.Vector2(dx, dy).normalize()
        self.all_units = all_units
        self.player_group = player_group
        self.damage = player['Atk Dmg']
        self.player = player

        self.laser_range = laser_range

    def update(self):
        self.laser_pos += self.target_pos * self.speed
        self.rect.center = (round(self.laser_pos.x), round(self.laser_pos.y))

        # Laser Range
        if self.rect.x > self.x + self.laser_range or self.rect.x < self.x - self.laser_range:
            self.kill()
        if self.rect.y < self.y - self.laser_range or self.rect.y > self.y + self.laser_range:
            self.kill()

