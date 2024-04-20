import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):  # game ist Game Klasse aus main.py
        self.game = game
        self._layer = PLAYER_EBENE  # '_' deutet eine interne Variable, die nicht verändert werden sollte von jemanden, der den Code später herunterlädt
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
        self.image = self.game.character_spritesheet.get_sprite(
            3, 2, self.width, self.height
        )  # Bild des Spielers beginnnt nicht bei (0,0) sondern (3,2) mit einer Länge und Breite von 32px
        # Hitbox des Objekts (Spieler)
        self.rect = self.image.get_rect()  # selbe Größe wie self.image
        self.rect.x = self.x
        self.rect.y = self.y

        # Variablen, die abspeicher, ob der Spieler sich bewegen soll auf Grund von gedrückten Knöpfen
        self.x_change = 0
        self.y_change = 0
        # Variable, die angibt in welche Richtung der Spieler schaut (notwendig für Animationen später)
        self.facing = "down"

    def update(self):
        # Wird jedes mal im Game aufgerufen, wenn self.all_sprites.update() verwendet wird
        # und die Spieler Klasse an der Reihe dran ist
        self.movement()
        # Übertrage die Beweging des Spielers aus movement() auf die Darstellung des Spielers auf dem Bildschirm
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        # Setze x_change, y_change zurück für den nächsten Tastendruck
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        # Liste aller Knöpfe die auf der Tastatur gedrückt wurden (oder Maustasten)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = "up"
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = "down"


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        # Die Block Ebene befindet sich unter der Ebene des Spielers
        self._layer = BLOCK_EBENE
        # Füge Block Asset zu all_sprites und blocks in Game
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Position des Blocks
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # Größe des Blocks
        self.width = TILESIZE
        self.height = TILESIZE
        # Darstellung des Blocks
        self.image = self.game.terrain_spritesheet.get_sprite(0, 32, self.width, self.height)
        # Hitbox des Objekts (Block)
        self.rect = self.image.get_rect()  # selbe Größe wie self.image
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        # Die Block Ebene befindet sich unter der Ebene des Blocks
        self._layer = GROUND_EBENE
        # Füge Block Asset zu all_sprites und blocks in Game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Position des Ground
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # Größe des Ground
        self.width = TILESIZE
        self.height = TILESIZE
        # Darstellung des Ground
        self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)
        # Hitbox des Objekts (Ground)
        self.rect = self.image.get_rect()  # selbe Größe wie self.image
        self.rect.x = self.x
        self.rect.y = self.y


class Spritesheet:
    def __init__(self, file):
        # Lade das gesamte Blatt mit allen Bildern
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):  # Schneide die einzelnen Bilder aus dem gesamten Blatt heraus
        sprite = pygame.Surface([width, height])
        # erstes Tuoel gibt an wo das Bild geladen werden soll (linke obere Ecke)
        # zweites Tupel gibt an wo welcher Bereich aus dem Blatt herausgeschnitten werden soll
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        # Die Umrandung des Objekts (welche Schwarz ist per default) durchsichtig wird
        sprite.set_colorkey(BLACK)
        # Gib den ausgeschnittenen Bereich zurück
        return sprite
