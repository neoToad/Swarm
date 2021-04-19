# Simple pygame program

# Import and initialize the pygame library
import pygame
from units_bases_lasers import Base, Unit
from upgrade_menu import show_gold, UpgradeMenu, Button

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

RED = (200, 0, 0)
BLUE = (0, 0, 128)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

respawn_speed = 1000

# Amount of time before each players units spawn
# Add units for player
P1_ADDUNIT = pygame.USEREVENT + 0
pygame.time.set_timer(P1_ADDUNIT, respawn_speed)
P2_ADDUNIT = pygame.USEREVENT + 1
pygame.time.set_timer(P2_ADDUNIT, respawn_speed)
P3_ADDUNIT = pygame.USEREVENT + 2
pygame.time.set_timer(P3_ADDUNIT, respawn_speed)
P4_ADDUNIT = pygame.USEREVENT + 3
pygame.time.set_timer(P4_ADDUNIT, respawn_speed)

#Standard gold increase
GOLD_INCREASE = pygame.USEREVENT + 4
pygame.time.set_timer(GOLD_INCREASE, 1000)

# Timer for finding the attack target
FIND_ATTACK_TARGET = pygame.USEREVENT + 5
pygame.time.set_timer(FIND_ATTACK_TARGET, 500)
# add_player_units = [['Player01', P1_ADDUNIT], ['Player02', P2_ADDUNIT], ['Player03', P3_ADDUNIT], ['Player04', P4_ADDUNIT]]

p1_units = pygame.sprite.Group()
p2_units = pygame.sprite.Group()
p3_units = pygame.sprite.Group()
p4_units = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bases = pygame.sprite.Group()
lasers = pygame.sprite.Group()

# players dict
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# upgrade_menu = UpgradeMenu(screen)
# btn_upgrade_dmg = Button(screen, 2, "Atk Dmg")
# btn_upgrade_atkspd = Button(screen,4, "Atk Spd")
# btn_upgrade_respd = Button(screen,6, "Respawn")
# btn_upgrade_spd = Button(screen,8, "Spd")
# buttons = [btn_upgrade_dmg, btn_upgrade_atkspd, btn_upgrade_respd, btn_upgrade_spd]

players_dict = {
    "Player01":
        {'color': RED,
         'base': None,
         'base loc': (SCREEN_WIDTH / 2, 100),
         'group': p1_units,
         'respawn event': P1_ADDUNIT,
         'Res. Spd': 1000,
         'Res. Spd cost': 50,
         'Spd': 1,
         'Spd cost': 50,
         'Atk Dmg': 1,
         'Atk Dmg cost': 50,

         'Atk Spd': 2000,

         'Atk Spd cost': 50,
         'gold': 0},

    "Player02":
        {'color': BLUE,
         'base': None,
         'base loc': (150, SCREEN_HEIGHT / 2),
         'group': p2_units,
         'respawn event': P2_ADDUNIT,
         "Res. Spd": 1000,
         'Spd': 1,
         'Spd Cost': 50,
         'Atk Dmg': 1,

         'Atk Spd': 2000,
         'gold': 0},
    "Player03":
        {'color': GREEN,
         'base': None,
         'base loc': (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200),
         'group': p3_units,
         'respawn event': P3_ADDUNIT,
         "Res. Spd": 1000,
         'Spd': 1,
         'Spd Cost': 50,

         'Atk Dmg': 1,

         'Atk Spd': 2000,
         'gold': 0},
    "Player04":
        {'color': WHITE,
         'base': None,
         'base loc': (SCREEN_WIDTH - 150, SCREEN_HEIGHT / 2),
         'group': p4_units,
         'respawn event': P4_ADDUNIT,
         "Res. Spd": 1000,
         'Atk Dmg': 1,
         'Atk Spd': 2000, # Lower is faster
         'Spd': 1,
         'Spd Cost': 50,
         'gold': 0}
}

upgrade_menu = UpgradeMenu(screen)
btn_upgrade_dmg = Button(screen, 2, "Atk Dmg", players_dict["Player01"])
btn_upgrade_atkspd = Button(screen,4, "Atk Spd", players_dict["Player01"])
btn_upgrade_respd = Button(screen,6, "Res. Spd", players_dict["Player01"])
btn_upgrade_spd = Button(screen,8, "Spd", players_dict["Player01"])
buttons = [btn_upgrade_dmg, btn_upgrade_atkspd, btn_upgrade_respd, btn_upgrade_spd]

# Set up the drawing window
# screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

leftclick_down_location = (0, 0)

for x in players_dict:
    players_dict[x]['base'] = Base(screen, players_dict[x], players_dict[x]['base loc'], players_dict[x]['color'], players_dict[x]['group'], players_dict[x]['respawn event'], lasers, all_sprites)
    players_dict[x]['group'].add(players_dict[x]['base'])
    bases.add(players_dict[x]['base'])
    all_sprites.add(players_dict[x]['base'])
    # print(players_dict[x])


class SelectorBox():
    def __init__(self):
        self.draw_new_selection_box = False
        self.selection_completed = False

    def draw_selection(self):
        if unit_selector.draw_new_selection_box:
            selection_box_x = current_mouse_location[0] - leftclick_down_location[0]
            selection_box_y = current_mouse_location[1] - leftclick_down_location[1]
            selection_box = pygame.Rect((leftclick_down_location), (selection_box_x, selection_box_y))
            return selection_box


def spawn_units():
    for player in players_dict:
        group = players_dict[player]['group']
        if event.type == players_dict[player]['respawn event']:
            new_enemy = Unit(screen, players_dict[player], players_dict[player]['color'], players_dict[player]['Spd'],
                             all_sprites, players_dict[player]['group'], lasers)

            group.add(new_enemy)
            all_sprites.add(new_enemy)

unit_selector = SelectorBox()

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # Randomly spawn units in their base area

        spawn_units()

        # Check for clicks
        button_type = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN: # If a mouse button is pressed

            # Check if clicked in game screen and draw the selection
            if button_type[0]:
                for unit in p1_units:
                    unit.selected = False
                leftclick_down_location = pygame.mouse.get_pos()
                unit_selector.draw_new_selection_box = True

                # Check if game menu button has been pressed
                for button in buttons:
                    if button.rect.collidepoint(leftclick_down_location):
                        button.check_for_click()

            if button_type[2]:
                rightclick_down_location = pygame.mouse.get_pos()
                for unit in p1_units:
                    try:
                        if unit.selected == True:
                            unit.set_target(rightclick_down_location)
                            unit.moving = True
                    except AttributeError:
                        pass

            # Check if game menu button has been pressed


        if event.type == pygame.MOUSEBUTTONUP:
            if not button_type[0]:
                leftclick_up_location = pygame.mouse.get_pos()
                unit_selector.draw_new_selection_box = False

            # Add gold
        if event.type == GOLD_INCREASE:
            for player in players_dict:
                players_dict[player]['gold'] += 1
                # print(f"{player} gold: {players_dict[player]['gold']}")

    current_mouse_location = pygame.mouse.get_pos()

    selection_box = unit_selector.draw_selection()

    screen.fill((0, 0, 0))

    # #Add gold
    # if event.type == GOLD_INCREASE:
    #     for player in players_dict:
    #         players_dict[player]['gold'] += 1
    #         print(f"{players_dict[player]} gold: {players_dict[player]['gold']}")

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
                        unit.kill()
                    else:
                        laser.kill()
                        unit.get_damage(laser.damage)
                        pass

    if unit_selector.draw_new_selection_box:
        pygame.draw.rect(screen, RED, selection_box, 2)
        for unit in p1_units:
            if unit not in bases:
                if selection_box.colliderect(unit):
                    pygame.draw.rect(screen, BLUE, unit, 2)
                    unit.selected = True

    # Show Selected units
    for unit in p1_units:
        # try:
        if unit not in bases:
            if unit.selected == True:
                pygame.draw.rect(screen, BLUE, unit, 2)
            unit.overlapped(bases)
        # except AttributeError:
        #     pass
    # Start earning gold

    all_sprites.update()
    # lasers.update()

    lasers.draw(screen)
    all_sprites.draw(screen)
    bases.update()
    lasers.update()
    upgrade_menu.update()
    for button in buttons:
        button.update()
    show_gold(screen, players_dict['Player01']['gold'])
    pygame.display.flip()
    clock.tick(60)
