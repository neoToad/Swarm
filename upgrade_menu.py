import pygame
pygame.init()
font = pygame.font.SysFont('comicsans', 30)


def show_gold(screen, gold_amount):
    text = font.render("Gold: " + str(gold_amount), 1, (255, 255, 255))
    screen.blit(text, (10, 10))


class UpgradeMenu():
    def __init__(self, screen):
        self.screen_width = 1400
        self.height = 100
        self.menu = pygame.Surface((1400, 100), pygame.SRCALPHA)
        self.rect = self.menu.get_rect()
        pygame.draw.rect(self.menu, (100,100,100), self.rect)
        self.x, self.y = 0, 800
        self.screen = screen

        # self.upgrade_dmg = Button()
        # self.buttons = [10]

    def update(self):
        self.screen.blit(self.menu, (self.x, self.y))
        # screen.blit(self.upgrade_dmg.image, (self.upgrade_dmg.x, self.upgrade_dmg.y))


class Button(UpgradeMenu):
    def __init__(self, screen, menu_btn_num, btn_name, player):
        super().__init__(screen)
        self.screen = screen
        self.width = 100
        self.height = 80
        self.btn_posx = menu_btn_num * 100
        self.btn_posy = 810
        self.image = pygame.Surface((100, 80), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (100, 200, 200), self.rect)
        self.font = pygame.font.SysFont('comicsans', 30)
        self.name = btn_name
        self.player = player

    def update(self):
        self.rect.x = self.btn_posx
        self.rect.y = self.btn_posy
        self.screen.blit(self.image, self.rect)
        # pygame.draw.rect(self.image, (100, 200, 200), self.rect)
        self.show_name()

    def show_name(self):
        self.text = self.font.render(self.name, 1, (100,50,0))
        self.screen.blit(self.text, (self.btn_posx + 10, self.btn_posy + 30))

    def check_for_click(self):
        self.per_btn_action()

    def per_btn_action(self):
        if self.name == 'Atk Dmg' or self.name == 'Spd':
            self.player[self.name] += 1

        if self.name == 'Atk Spd':
            self.player[self.name] -= 100

        if self.name == 'Res. Spd':
            self.player[self.name] -= 100
            pygame.time.set_timer(self.player['respawn event'], self.player[self.name])

        print(self.player[self.name])


