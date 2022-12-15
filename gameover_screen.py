# -*- coding: utf-8 -*-
import main_screen

import pygame
import sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Game_over")

BG = pygame.image.load("Background.png")


def get_font(size):
    return pygame.font.Font("font.ttf", size)


def gameover_menu(winner_letter):
    while True:
        winner = 'Gray' if winner_letter == 'G' else 'Red'
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        MENU_TEXT = get_font(100).render(f"{winner} win!", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        NEW_GAME_BUTTON = Button(image=pygame.image.load("randomRectangle.png"), pos=(400, 300),
                             text_input="New game", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("quitRectangle.png"), pos=(400, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [NEW_GAME_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEW_GAME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_screen.main_menu()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    gameover_menu('G')
