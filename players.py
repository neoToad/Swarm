import pygame

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
P2_ADDUNIT = pygame.USEREVENT + 1
P3_ADDUNIT = pygame.USEREVENT + 2
P4_ADDUNIT = pygame.USEREVENT + 3

# Timer for finding the attack target
FIND_ATTACK_TARGET = pygame.USEREVENT + 5
pygame.time.set_timer(FIND_ATTACK_TARGET, 500)

p1_units = pygame.sprite.Group()
p2_units = pygame.sprite.Group()
p3_units = pygame.sprite.Group()
p4_units = pygame.sprite.Group()

players_dict = {
    "Player01":
        {
         'type': 'human',
         'color': RED,
         'base': None,
         'base loc': (SCREEN_WIDTH / 2, 100),
         'group': p1_units,
         'respawn event': P1_ADDUNIT,
         'Res. Spd': 1000,
         'Res. Spd cost': 50,
         'Spd': 1,
         'Spd cost': 50,
         'Atk Dmg': 200,
         'Atk Dmg cost': 50,
         'Atk Spd': 4000,
         'Atk Spd cost': 50,
         'unit health': 1,
         'laser range': 100,
         'base laser range': 200,
         'base target range': 200,
         'base cool down': 1500,
         'gold': 0,
         'score': 0,
         'reward': 0,
         'dead': False
         },

    "Player02":
        {'type': 'ai',
         'color': BLUE,
         'base': None,
         'base loc': (150, SCREEN_HEIGHT / 2),
         'group': p2_units,
         'respawn event': P2_ADDUNIT,
         'Res. Spd': 1000,
         'Res. Spd cost': 50,
         'Spd': 1,
         'Spd cost': 50,
         'Atk Dmg': 1,
         'Atk Dmg cost': 50,
         'Atk Spd': 4000,
         'Atk Spd cost': 50,
         'unit health': 1,
         'laser range': 100,
         'gold': 0,
         'score': 0,
         'reward': 0,
         'dead': False},

    "Player03":
        {'type': 'ai',
         'color': GREEN,
         'base': None,
         'base loc': (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 200),
         'group': p3_units,
         'respawn event': P3_ADDUNIT,
         'Res. Spd': 1000,
         'Res. Spd cost': 50,
         'Spd': 1,
         'Spd cost': 50,
         'Atk Dmg': 1,
         'Atk Dmg cost': 50,
         'Atk Spd': 4000,
         'Atk Spd cost': 50,
         'unit health': 1,
         'laser range': 100,
         'gold': 0,
         'score': 0,
         'reward': 0,
         'dead': False},

    "Player04":
        {'type': 'ai',
         'color': WHITE,
         'base': None,
         'base loc': (SCREEN_WIDTH - 150, SCREEN_HEIGHT / 2),
         'group': p4_units,
         'respawn event': P4_ADDUNIT,
         'Res. Spd': 1000,
         'Res. Spd cost': 50,
         'Spd': 1,
         'Spd cost': 50,
         'Atk Dmg': 1,
         'Atk Dmg cost': 50,
         'Atk Spd': 4000,
         'Atk Spd cost': 50,
         'unit health': 1,
         'laser range': 100,
         'gold': 0,
         'score': 0,
         'reward': 0,
         'dead': False},
}
