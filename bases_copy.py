# Simple pygame program

# Import and initialize the pygame library
import pygame
from units_bases_lasers import Base, Unit

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

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
pygame.time.set_timer(P2_ADDUNIT, 1000)
P3_ADDUNIT = pygame.USEREVENT + 2
pygame.time.set_timer(P3_ADDUNIT, 1000)
P4_ADDUNIT = pygame.USEREVENT + 3
pygame.time.set_timer(P4_ADDUNIT, 1000)

# Timer for finding the attack target
FIND_ATTACK_TARGET = pygame.USEREVENT + 5
pygame.time.set_timer(FIND_ATTACK_TARGET, 500)
add_player_units = [['Player01', P1_ADDUNIT], ['Player02', P2_ADDUNIT], ['Player03', P3_ADDUNIT], ['Player04', P4_ADDUNIT]]

p1_units = pygame.sprite.Group()
p2_units = pygame.sprite.Group()
p3_units = pygame.sprite.Group()
p4_units = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bases = pygame.sprite.Group()
lasers = pygame.sprite.Group()

# players dict
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

players_dict = {
    "Player01":
        {'color': RED, 'base': Base(screen, (SCREEN_WIDTH / 2, 100), RED), 'group': p1_units},
    "Player02":
        {'base': Base(screen, (150, SCREEN_HEIGHT / 2), BLUE), 'group': p2_units},
    "Player03":
        {'base': Base(screen, (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100), GREEN), 'group': p3_units},
    "Player04":
        {'base': Base(screen, (SCREEN_WIDTH - 150, SCREEN_HEIGHT / 2), WHITE), 'group': p4_units}
}

# Set up the drawing window
# screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

respawn_speed = 1000

leftclick_down_location = (0, 0)

p1_speed = 1

for x in players_dict:
    players_dict[x]['group'].add(players_dict[x]['base'])
    bases.add(players_dict[x]['base'])
    all_sprites.add(players_dict[x]['base'])


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


unit_selector = SelectorBox()

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # Randomly spawn units in their base area

        for player, add_command in add_player_units:
            # print(add_command)
            group = players_dict[player]['group']
            if event.type == add_command:
                new_enemy = Unit(screen, players_dict[player]['base'], players_dict[player]['base'].color, p1_speed, all_sprites, players_dict[player]['group'], lasers)

                group.add(new_enemy)
                all_sprites.add(new_enemy)



            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    for x in bases:
                        x.get_health(50)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    for x in bases:
                        x.get_damage(1)

            # bases.add(players_dict[player]['base'])

        # Check for clicks
        button_type = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN: # If a mouse button is pressed
            if button_type[0]:
                for unit in p1_units:
                    unit.selected = False
                leftclick_down_location = pygame.mouse.get_pos()
                unit_selector.draw_new_selection_box = True
            if button_type[2]:
                rightclick_down_location = pygame.mouse.get_pos()
                for unit in p1_units:
                    try:
                        if unit.selected == True:
                            unit.set_target(rightclick_down_location)
                            unit.moving = True
                    except AttributeError:
                        pass
            # if button_type[1]:
            #     respawn_speed -= 400
            #     pygame.time.set_timer(P2_ADDUNIT, 200)

        if event.type == pygame.MOUSEBUTTONUP:
            if not button_type[0]:
                leftclick_up_location = pygame.mouse.get_pos()
                unit_selector.draw_new_selection_box = False

    current_mouse_location = pygame.mouse.get_pos()

    selection_box = unit_selector.draw_selection()

    screen.fill((0, 0, 0))

    # Draw units and check for collisions
    for unit in all_sprites:
        # screen.blit(unit.image, unit.rect)
        if event.type == FIND_ATTACK_TARGET:  # check event queue contains PLAYSOUNDEVENT
            unit.check_for_target = True
        for laser in lasers:
            screen.blit(laser.image, laser.rect)
            if unit not in laser.player_group:
                if pygame.sprite.collide_rect(laser, unit):
                    if unit not in bases:
                        laser.kill()
                        unit.kill()
                    else:
                        laser.kill()
                        print('planet hit')
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
    all_sprites.update()
    lasers.update()
    bases.update()

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
