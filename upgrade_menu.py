import pygame
pygame.init()
font = pygame.font.SysFont('comicsans', 30)


def show_gold(screen, gold_amount):
    text = font.render("Gold: " + str(gold_amount), 1, (255, 255, 255))
    screen.blit(text, (10, 10))