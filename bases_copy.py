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

players_dict = {
    "Player01":
        {'color': RED, 'base': Base((SCREEN_WIDTH / 2, 100), RED), 'group': p1_units},
    "Player02":
        {'base': Base((150, SCREEN_HEIGHT / 2), BLUE), 'group': p2_units},
    "Player03":
        {'base': Base((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100), GREEN), 'group': p3_units},
    "Player04":
        {'base': Base((SCREEN_WIDTH - 150, SCREEN_HEIGHT / 2), WHITE), 'group': p4_units}
}

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

respawn_speed = 1000

leftclick_down_location = (0, 0)

p1_speed = 1

for x in players_dict:
    bases.add(players_dict[x]['base'])


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
            if event.type == add_command:
                new_enemy = Unit(screen, players_dict[player]['base'], players_dict[player]['base'].color, p1_speed, all_sprites, players_dict[player]['group'], lasers)
                group = players_dict[player]['group']
                group.add(new_enemy)
                all_sprites.add(new_enemy)
                # if player != "Player01":
                #     enemies.add(new_enemy)



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
            if button_type[1]:
                respawn_speed -= 400
                # pygame.time.set_timer(P2_ADDUNIT, 5000)
                pygame.time.set_timer(P2_ADDUNIT, 200)

        if event.type == pygame.MOUSEBUTTONUP:
            if not button_type[0]:
                leftclick_up_location = pygame.mouse.get_pos()
                unit_selector.draw_new_selection_box = False

    current_mouse_location = pygame.mouse.get_pos()

    selection_box = unit_selector.draw_selection()

    all_sprites.update()
    lasers.update()

    # hits = pygame.sprite.groupcollide(all_sprites, lasers, True, True)

    screen.fill((0, 0, 0))
    # Add units to screen
    for entity in bases:
        screen.blit(entity.surf, entity.rect)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        if event.type == FIND_ATTACK_TARGET:  # check event queue contains PLAYSOUNDEVENT
            entity.check_for_target = True
        # hits = pygame.sprite.spritecollide(entity, lasers, True)
        for entity in lasers:
            screen.blit(entity.surf, entity.rect)
        # if pygame.sprite.spritecollide(entity, all_sprites, True):
        #     entity.kill()
        # hits = pygame.sprite.groupcollide(all_sprites, lasers, True, True)

    if unit_selector.draw_new_selection_box:
        pygame.draw.rect(screen, RED, selection_box, 2)
        for unit in p1_units:
            if selection_box.colliderect(unit):
                pygame.draw.rect(screen, BLUE, unit, 2)
                unit.selected = True
    # Show Selected units
    for unit in p1_units:
        try:
            if unit.selected == True:
                pygame.draw.rect(screen, BLUE, unit, 2)
            unit.overlapped()
        except AttributeError:
            pass

    # hits = pygame.sprite.groupcollide(all_sprites, lasers, True, True)



    # Flip the display
    pygame.display.flip()
    clock.tick(60)
