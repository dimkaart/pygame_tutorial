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

        # Variable für die Lebenspunkte
        self.hp = LifeBar(self.game, HP)

        # Variable für Anzahl an getöteten Gegnern
        self.gamepoints = Points(self.game, 0)

    def update(self):
        # Wird jedes mal im Game aufgerufen, wenn self.all_sprites.update() verwendet wird
        # und die Spieler Klasse an der Reihe dran ist
        self.movement()
        # Visualisiere die Bewegungen des Spielers
        self.animate()
        # Überprüfe ob der Spieler vom Gegner berührt wurde und somit gestorben ist
        self.collide_enemy()
        # Überprüfe ob der Spieler ein HealingItem berührt und somit seine Lebenspunkte wiederherstellt
        self.collide_healing()
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

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, dokill=False)
        if hits:
            # Spieler stirbt nur dann wenn keine Lebenspunkte mehr vorhanden sind
            if self.hp.lifebar > 1:
                self.hp = LifeBar(self.game, self.hp.lifebar - 1)
            else:
                # Lösche den Spieler aus all_sprites und somit auh aus dem Spiel
                self.kill()
                # Beende das Spiel
                self.game.playing = False

    def collide_healing(self):
        hits = pygame.sprite.spritecollide(self, self.game.items, dokill=True)
        if hits:
            HealingItem.sound_track.play()
            self.hp = LifeBar(self.game, min(100, self.hp.lifebar + hits[0].healingEffect))

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


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):  # fg: Vordergrundfarbe, bg: Hintergrundfarbe
        self.font = pygame.font.Font("Assets/Fonts/arial.ttf", fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        # Generiere ein Rechteck (Ebene) und fülle diese mit der Hintergrundfarbe self.bg
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.bg)
        # Hitbox des Knopfs
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Stelle den Inhalt (self.content) in de rSchrift self.font dar
        self.text = self.font.render(self.content, True, self.fg)
        # Postion des Textes
        self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))

        # Darstellung des Knopfes auf dem Bildschirm
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        # - pos: Position der Maus
        # - pressed: Wurde die Maus gedrückt?
        if self.rect.collidepoint(pos):  # Kollidiert der Knopf mit der Maus?
            if pressed[0]:
                return True
            return False
        return False


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_EBENE
        # Füge Attack Asset zu all_sprites und attacks in Game hinzu
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Position der Attacke
        self.x = x
        self.y = y
        # Größe/Reichweite der Attacke
        self.width = TILESIZE
        self.height = TILESIZE
        # Darstellung der Attacke
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        # Hitbos des Objekts (Attacke)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Variable, die bestimmet, welche der Animationen angezeigt werden soll
        self.animate_loop = 0

        # Lade Soundeffekte für Treffer und Fehler
        self.sound_hit = pygame.mixer.Sound("Assets/Music/Soundeffect/swordhit.wav")
        self.sound_hit.set_volume(0.75)
        self.sound_miss = pygame.mixer.Sound("Assets/Music/Soundeffect/swordmiss.wav")
        self.sound_miss.set_volume(0.05)

    def update(self):
        self.animate()
        hit = self.collide_enemies()
        if hit:
            self.sound_hit.play()
            # Wenn ein Gegner getötet wurde erhöhe den Punktestand um 1
            self.game.player.gamepoints = Points(self.game, self.game.player.gamepoints.points + 1)
        else:
            self.sound_miss.play()

    def collide_enemies(self):
        hits = pygame.sprite.spritecollide(
            self, self.game.enemies, dokill=True
        )  # Lösche den Gegner (und die Attacke), falls die Attacke diesen trifft
        if hits:
            return hits

    def animate(self):
        # Richtung in die der Spieler schaut ist gleichzeitig die Richtung in die er angreift
        direction = self.game.player.facing

        down_animate = [
            self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height),
        ]

        up_animate = [
            self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height),
        ]

        left_animate = [
            self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height),
        ]

        right_animate = [
            self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height),
        ]

        if direction == "up":
            self.image = up_animate[math.floor(self.animate_loop)]
            self.animate_loop += 0.5
            if self.animate_loop >= 5:  # Wenn die Animation vollständig durchgelaufen ist
                self.kill()  # Löscje das Asset Attacks

        if direction == "down":
            self.image = down_animate[math.floor(self.animate_loop)]
            self.animate_loop += 0.5
            if self.animate_loop >= 5:  # Wenn die Animation vollständig durchgelaufen ist
                self.kill()  # Löscje das Asset Attacks

        if direction == "left":
            self.image = left_animate[math.floor(self.animate_loop)]
            self.animate_loop += 0.5
            if self.animate_loop >= 5:  # Wenn die Animation vollständig durchgelaufen ist
                self.kill()  # Löscje das Asset Attacks

        if direction == "right":
            self.image = right_animate[math.floor(self.animate_loop)]
            self.animate_loop += 0.5
            if self.animate_loop >= 5:  # Wenn die Animation vollständig durchgelaufen ist
                self.kill()  # Löscje das Asset Attacks


class LifeBar(pygame.sprite.Sprite):
    def __init__(self, game, hp):
        self.game = game
        self._layer = PLAYER_EBENE

        # Aktueller Stand der Lebenspunkte
        self.lifebar = hp

        # Füge die Lebenspunkte Asset zu all_sprites in Game hinzu
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Position der Lebenspunkte
        self.x = 1
        self.y = 1
        print(hp)

        if hp >= 75:
            self.image = self.game.health_spritesheet.get_sprite(3, 20, 42, 7)
        elif hp >= 50:
            self.image = self.game.health_spritesheet.get_sprite(51, 20, 42, 7)
        elif hp >= 25:
            self.image = self.game.health_spritesheet.get_sprite(99, 20, 42, 7)
        elif hp > 0:
            self.image = self.game.health_spritesheet.get_sprite(146, 20, 42, 7)

        self.image = pygame.transform.scale(self.image, (75, 25))

        # Hitbox des Objekts (Life Bar)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class HealingItem(pygame.sprite.Sprite):
    # Soundeffekt
    pygame.mixer.init()
    sound_track = pygame.mixer.Sound("Assets/Music/Soundeffect/potion.wav")
    sound_track.set_volume(0.15)

    def __init__(self, game, x, y, effect):
        self.game = game
        self._layer = GROUND_EBENE
        # Füge Item Asset zu all_sprites und items in Game hinzu
        self.groups = self.game.all_sprites, self.game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Position des Items
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # Größe des Items
        self.width = TILESIZE
        self.height = TILESIZE

        # Darstellnug des Items
        if effect <= 25:
            self.image = self.game.item_spritesheet.get_sprite(0, 448, self.width, self.height)
        elif (effect > 25) and (effect <= 50):
            self.image = self.game.item_spritesheet.get_sprite(128, 608, self.width, self.height)
        self.image.set_colorkey(WHITE)
        # Hitbox des Objekts (Healing Item)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Heilungseffekt
        self.healingEffect = effect


class Points(pygame.sprite.Sprite):
    def __init__(self, game, points=0):
        self.game = game
        self._layer = PLAYER_EBENE

        # Aktueller Stand der Punkte
        self.points = points

        # Füge Punkte Asset zu all_spirtes in Game hinzu
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Position der Punkte
        self.x = WIN_BREITE - 3 * TILESIZE
        self.y = 0
        # Größe des Punktestands
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.item_spritesheet.get_sprite(224, 382, self.width, self.height)
        self.image.set_colorkey(WHITE)

        # Hitbos des Objekts (Punkte)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
