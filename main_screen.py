# -*- coding: utf-8 -*-
import random

import checkers

import pygame
import sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")

BG = pygame.image.load("Background.png")


def get_font(size):
    return pygame.font.Font("font.ttf", size)


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        MENU_TEXT = get_font(100).render("Who will go first?", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        GRAY_BUTTON = Button(image=pygame.image.load("grayRectangle.png"), pos=(400, 250),
                             text_input="Gray", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        RED_BUTTON = Button(image=pygame.image.load("redRectangle.png"), pos=(400, 400),
                            text_input="Red", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        RANDOM_BUTTON = Button(image=pygame.image.load("randomRectangle.png"), pos=(400, 550),
                               text_input="Random", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("quitRectangle.png"), pos=(400, 700),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [GRAY_BUTTON, RED_BUTTON, RANDOM_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GRAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    checkers.checkers(800, 8, 'G')
                if RED_BUTTON.checkForInput(MENU_MOUSE_POS):
                    checkers.checkers(800, 8, 'R')
                if RANDOM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    checkers.checkers(800, 8, random.choice(('R', 'G')))
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
