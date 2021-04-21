import pygame
from players import players_dict
from upgrade_menu import show_gold, UpgradeMenu, Button
from Base import Base
from units_lasers import Unit
from ai_commands import AI

pygame.init()

players = players_dict

all_sprites = pygame.sprite.Group()
bases = pygame.sprite.Group()
lasers = pygame.sprite.Group()

pygame.time.set_timer(players['Player01']['respawn event'], players['Player01']['Res. Spd'])
pygame.time.set_timer(players['Player02']['respawn event'], players['Player02']['Res. Spd'])
pygame.time.set_timer(players['Player03']['respawn event'], players['Player03']['Res. Spd'])
pygame.time.set_timer(players['Player04']['respawn event'], players['Player04']['Res. Spd'])

#Standard gold increase
GOLD_INCREASE = pygame.USEREVENT + 4
pygame.time.set_timer(GOLD_INCREASE, 1000)

FIND_ATTACK_TARGET = pygame.USEREVENT + 5
pygame.time.set_timer(FIND_ATTACK_TARGET, 500)

class SwarmGame:
    def __init__(self, SCREEN_WIDTH = 1400, SCREEN_HEIGHT = 900):
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT

        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()

        self.leftclick_down_location = (0, 0)

        self.upgrade_menu = UpgradeMenu(self.screen)
        self.btn_upgrade_dmg = Button(self.screen, 2, "Atk Dmg", players_dict["Player01"])
        self.btn_upgrade_atkspd = Button(self.screen, 4, "Atk Spd", players_dict["Player01"])
        self.btn_upgrade_respd = Button(self.screen, 6, "Res. Spd", players_dict["Player01"])
        self.btn_upgrade_spd = Button(self.screen, 8, "Spd", players_dict["Player01"])
        self.buttons = [self.btn_upgrade_dmg, self.btn_upgrade_atkspd, self.btn_upgrade_respd, self.btn_upgrade_spd]

        self.draw_new_selection_box = False
        self.selection_completed = False

        self.running = True

        self.create_bases()

        # unit_selector = SelectorBox()
        # ai = AI(p1_units, p2_units, p3_units, p4_units, bases)

    def create_bases(self):
        for x in players:
            players[x]['base'] = Base(self.screen, players_dict[x], all_sprites, lasers, bases)
            players[x]['group'].add(players_dict[x]['base'])
            bases.add(players[x]['base'])
            all_sprites.add(players[x]['base'])
            # print(players_dict[x])


    def draw_selection(self):
        if self.draw_new_selection_box:
            selection_box_x = self.current_mouse_location[0] - self.leftclick_down_location[0]
            selection_box_y = self.current_mouse_location[1] - self.leftclick_down_location[1]
            selection_box = pygame.Rect(self.leftclick_down_location, (selection_box_x, selection_box_y))
            return selection_box

    def spawn_units(self, e_type):
        for player in players:
            group = players[player]['group']
            if e_type == players[player]['respawn event']:
                new_unit = Unit(self.screen, players[player], all_sprites, lasers, bases)
                group.add(new_unit)
                all_sprites.add(new_unit)

    def deselect_units(self):
        for unit in players['Player01']['group']:
            unit.selected = False

    def send_selected_to_clk(self):
        for unit in players['Player01']['group']:
            try:
                if unit.selected == True:
                    unit.set_target(self.rightclick_down_location)
                    unit.moving = True
            except AttributeError:
                pass

    def check_btn_clicks(self):
        for button in self.buttons:
            if button.rect.collidepoint(self.leftclick_down_location):
                button.check_for_click()

    # Run until the user asks to quit
    def run_game(self):
        while self.running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Randomly spawn units in their base area

                self.spawn_units(event.type)

                # Check for clicks
                button_type = pygame.mouse.get_pressed()
                if event.type == pygame.MOUSEBUTTONDOWN:  # If a mouse button is pressed

                    # Check if clicked in game screen and draw the selection
                    if button_type[0]:
                        self.deselect_units()
                        self.leftclick_down_location = pygame.mouse.get_pos()
                        self.draw_new_selection_box = True
                        print(self.leftclick_down_location)

                        # Check if game menu button has been pressed
                        self.check_btn_clicks()

                    if button_type[2]:
                        self.rightclick_down_location = pygame.mouse.get_pos()
                        self.send_selected_to_clk()

                    # Check if game menu button has been pressed

                if event.type == pygame.MOUSEBUTTONUP:
                    if not button_type[0]:
                        selfleftclick_up_location = pygame.mouse.get_pos()
                        self.draw_new_selection_box = False

                    # Add gold
                if event.type == GOLD_INCREASE:
                    for player in players:
                        players[player]['gold'] += 1
                        # print(f"{player} gold: {players_dict[player]['gold']}")

            self.current_mouse_location = pygame.mouse.get_pos()

            self.selection_box = self.draw_selection()

            self.screen.fill((0, 0, 0))

            # Draw units and check for collisions
            for unit in all_sprites:
                # screen.blit(unit.image, unit.rect)
                if event.type == FIND_ATTACK_TARGET:  # check event queue
                    unit.check_for_target = True
                for laser in lasers:
                    # screen.blit(laser.image, laser.rect)
                    if unit not in laser.player_group:
                        if pygame.sprite.collide_rect(laser, unit):
                            if unit not in bases:
                                laser.kill()
                                laser.player['gold'] += 1
                                laser.player['score'] += 2
                                unit.kill()
                            else:
                                laser.kill()
                                unit.get_damage(laser.damage)
                                laser.player['score'] += 1
                                if unit.dead == True:
                                    laser.player['score'] += 100
                                    unit.player['score'] += -100
                                    pygame.time.set_timer(unit.respawn_event, 0)
                            # print(laser.player['score'])

            if self.draw_new_selection_box:
                pygame.draw.rect(self.screen, (200, 0, 0), self.selection_box, 2)
                for unit in players['Player01']['group']:
                    if unit not in bases:
                        if self.selection_box.colliderect(unit):
                            pygame.draw.rect(self.screen, (0, 0, 128), unit, 2)
                            unit.selected = True

            # Show Selected units
            for unit in players['Player01']['group']:
                # try:
                if unit not in bases:
                    if unit.selected == True:
                        pygame.draw.rect(self.screen, (0, 0, 128), unit, 2)

            all_sprites.update()
            lasers.draw(self.screen)
            all_sprites.draw(self.screen)
            bases.update()
            lasers.update()
            self.upgrade_menu.update()
            for button in self.buttons:
                button.update()
            show_gold(self.screen, players_dict['Player01']['gold'])
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = SwarmGame()
    game.run_game()