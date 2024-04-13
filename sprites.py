import pygame
from pygame.sprite import Group
from settings import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y): # game ist Game Klasse aus main.py
        self.game = game
        self._layer = PLAYER_EBENE # '_' deutet eine interne Variable, die nicht verändert werden sollte von jemanden, der den Code später herunterlädt
        # Füge Spieler Asset zu all_spirtes in Game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Position des Spielers
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # Größe des Spielers
        self.width = TILESIZE
        self.height = TILESIZE
        # Darstellung des Spielers (Part 1: Rechteck, Part 2: Bild)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        # Hitbox des Objekts (Spieler)
        self.rect = self.image.get_rect() # selbe Größe wie self.image
        self.rect.x = self.x
        self.rect.y = self.y