import math
import random

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
        # Variable, die bestimmt, welches der animationen angezeigt werden soll
        self.animation_loop = 1

    def update(self):
        # Wird jedes mal im Game aufgerufen, wenn self.all_sprites.update() verwendet wird
        # und die Spieler Klasse an der Reihe dran ist
        self.movement()
        # Visualisiere die Bewegungen des Spielers
        self.animate()
        # Übertrage die Beweging des Spielers aus movement() auf die Darstellung des Spielers auf dem Bildschirm (in x-Richtung)
        self.rect.x += self.x_change
        # Überprüfe ob der Spieler mit der Wand in x-Richtung kollidiert
        self.collide_blocks("x")
        # Übertrage die Beweging des Spielers aus movement() auf die Darstellung des Spielers auf dem Bildschirm (in y-Richtung)
        self.rect.y += self.y_change
        # Überprüfe ob der Spieler mit der Wand in y-Richtung kollidiert
        self.collide_blocks("y")
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

    def collide_blocks(self, direction):
        if direction == "x":
            # - spritecollide(A, B) überprüft ob die Rechtecke vom Sprite A mit der Gruppe von Sprites B
            # z.B. Player und Liste der Wände oder Player und Liste aller Feinde sich überlappen
            # - dokill besagt ob sämtliche Sprites, die kollidieren gelöscht werden sollen
            hits = pygame.sprite.spritecollide(
                self, self.game.blocks, dokill=False
            )  # Rückgabe ist Liste aller Objekte mit denen der Spieler kollidiert
            if hits:
                if self.x_change > 0:
                    # Fall 1: Bewegung nach rechts
                    # Der Spieler soll an die Position "Wand - Breite des Spielers (nach links)" versetzt werden,
                    # wobei man zunächst beide Rechtecke übereinander darstellt (hits[0].rect.left) um eine feste Startposition zu haben
                    # von der der Spieler wegbewegt wird um keine Kollision mehr zu haben
                    self.rect.x = hits[0].rect.left - self.rect.width
                elif self.x_change < 0:
                    # Fall 2: Bewegung nach links
                    # Der Spieler soll an die Position "REchte obere Ecke der Wand = Linke obere Ecke des Spielers" versetzt werden
                    self.rect.x = hits[0].rect.right
        elif direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, dokill=False)
            if hits:
                if self.y_change > 0:
                    # Fall 3: Bewegung nach unten
                    self.rect.y = hits[0].rect.top - self.rect.height
                elif self.y_change < 0:
                    # Fall 4: Bewegung nach oben
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        down_animations = [
            self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height),
        ]

        up_animations = [
            self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height),
        ]

        left_animations = [
            self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height),
        ]

        right_animations = [
            self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height),
        ]

        if self.facing == "down":
            if self.y_change == 0:
                # Fall 1: Schauen nach unten aber bewegen uns nicht
                self.image = down_animations[0]
            else:  # y_change != 0
                # Fall 2: Schauen nach unten und bewegen uns
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        elif self.facing == "up":
            if self.y_change == 0:
                # Fall 1: Schauen nach unten aber bewegen uns nicht
                self.image = up_animations[0]
            else:  # y_change != 0
                # Fall 2: Schauen nach unten und bewegen uns
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        elif self.facing == "left":
            if self.x_change == 0:
                # Fall 1: Schauen nach unten aber bewegen uns nicht
                self.image = left_animations[0]
            else:  # y_change != 0
                # Fall 2: Schauen nach unten und bewegen uns
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        elif self.facing == "right":
            if self.x_change == 0:
                # Fall 1: Schauen nach unten aber bewegen uns nicht
                self.image = right_animations[0]
            else:  # y_change != 0
                # Fall 2: Schauen nach unten und bewegen uns
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_EBENE
        # Füge Gegner Asset zu all_sprites und enemies in Game hinzu
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Position des Gegners
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # Größe des Gegners
        self.width = TILESIZE
        self.height = TILESIZE

        # Darstellung des Gegners
        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)

        # Hitbox des Objekts (Gegner)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Variable, die abspeicherm ob der Gegner sich bewegt
        self.x_change = 0
        self.y_change = 0

        # In welche Richtung schaut der Gegner (notwendig für Animation)
        self.facing = random.choice(["down", "up", "left", "right"])
        # Variable, die bestimmt, welche der Animationen angezeigt werden soll
        self.animation_loop = 1
        # Variable, die bestimmt, ob der Gegner sich überhaupt bewegen soll
        self.movement_loop = 0
        # Zufällige Laufweite des Gegners zwischen 7px und 30px
        self.max_travel = random.randint(7, 30)

    def update(self):
        self.movement()
        self.animate()
        # Übertrage die Bewegung des Gegners, falls welche besteht (aus movement()) auf die Darstellung des Gegners auf dem Bildschirm (x-Richtung)
        self.rect.x += self.x_change
        self.collide_blocks("x")
        # Übertrage die Bewegung des Gegners, falls welche besteht (aus movement()) auf die Darstellung des Gegners auf dem Bildschirm (y-Richtung)
        self.rect.y += self.y_change
        self.collide_blocks("y")

        # Setze x_change, y_change zurück für die nächste Iteration
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            # Wenn wir self.max_travel Frames nach links bewegt haben, ändere die Bewegungsrichtung nach rechts
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"

        if self.facing == "up":
            self.y_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "down"
        if self.facing == "down":
            self.y_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "up"

    def animate(self):
        down_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height),
        ]

        up_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height),
        ]

        left_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height),
        ]

        right_animations = [
            self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height),
        ]

        if self.facing == "down":
            if self.y_change == 0:
                # Fall 1: Schauen nach unten aber bewegen uns nicht
                self.image = down_animations[0]
            else:  # y_change != 0
                # Fall 2: Schauen nach unten und bewegen uns
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        elif self.facing == "up":
            if self.y_change == 0:
                # Fall 1: Schauen nach unten aber bewegen uns nicht
                self.image = up_animations[0]
            else:  # y_change != 0
                # Fall 2: Schauen nach unten und bewegen uns
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        elif self.facing == "left":
            if self.x_change == 0:
                # Fall 1: Schauen nach unten aber bewegen uns nicht
                self.image = left_animations[0]
            else:  # y_change != 0
                # Fall 2: Schauen nach unten und bewegen uns
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        elif self.facing == "right":
            if self.x_change == 0:
                # Fall 1: Schauen nach unten aber bewegen uns nicht
                self.image = right_animations[0]
            else:  # y_change != 0
                # Fall 2: Schauen nach unten und bewegen uns
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def collide_blocks(self, direction):
        if direction == "x":
            # - spritecollide(A, B) überprüft ob die Rechtecke vom Sprite A mit der Gruppe von Sprites B
            # z.B. Player und Liste der Wände oder Player und Liste aller Feinde sich überlappen
            # - dokill besagt ob sämtliche Sprites, die kollidieren gelöscht werden sollen
            hits = pygame.sprite.spritecollide(
                self, self.game.blocks, dokill=False
            )  # Rückgabe ist Liste aller Objekte mit denen der Spieler kollidiert
            if hits:
                if self.x_change > 0:
                    # Fall 1: Bewegung nach rechts
                    # Der Spieler soll an die Position "Wand - Breite des Spielers (nach links)" versetzt werden,
                    # wobei man zunächst beide Rechtecke übereinander darstellt (hits[0].rect.left) um eine feste Startposition zu haben
                    # von der der Spieler wegbewegt wird um keine Kollision mehr zu haben
                    self.rect.x = hits[0].rect.left - self.rect.width
                elif self.x_change < 0:
                    # Fall 2: Bewegung nach links
                    # Der Spieler soll an die Position "REchte obere Ecke der Wand = Linke obere Ecke des Spielers" versetzt werden
                    self.rect.x = hits[0].rect.right
        elif direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, dokill=False)
            if hits:
                if self.y_change > 0:
                    # Fall 3: Bewegung nach unten
                    self.rect.y = hits[0].rect.top - self.rect.height
                elif self.y_change < 0:
                    # Fall 4: Bewegung nach oben
                    self.rect.y = hits[0].rect.bottom
