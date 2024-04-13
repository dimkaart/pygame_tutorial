import sys

import pygame
from settings import *
from sprites import *


class Game:
    def __init__(self):
        pygame.init()
        # Bildschirmauflösung
        self.screen = pygame.display.set_mode((WIN_BREITE, WIN_HOEHE))
        # Bildschirmwiederholung
        self.clock = pygame.time.Clock()
        # Schrifttext
        self.font = pygame.font.Font("Assets/Fonts/arial.ttf")
        # Status des Spiels (wird später zum stoppen des Spiels benötigt)
        self.running = True
        # Spielname
        self.game_title = pygame.display.set_caption(GAME_TITLE)
        # Spielicon
        icon = pygame.image.load(ICON_NAME)
        self.game_icon = pygame.display.set_icon(icon)

    def new(self):
        # Ist der spieler noch aktiv/lebendig
        self.playing = True
        # Container welcher sämtliche Gruppen (Spieler, Gegner, Wände, etc.) enthält
        self.all_sprites = pygame.sprite.LayeredUpdates()
        # Container für Wände
        self.blocks = pygame.sprite.LayeredUpdates()
        # Container für Gegner
        self.enemies = pygame.sprite.LayeredUpdates()
        # Container für Angriffsanimation
        self.attacks = pygame.sprite.LayeredUpdates()
        # Container für Tränke, Kisten, Waffen
        self.items = pygame.sprite.LayeredUpdates()
        # Spieler hinzufügen
        self.player = Player(self, 1, 2)  # self ist das Game Objekt

    def events(self):
        # Game Loop Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT überprüft ob das Spiel mittels "x" beendet wurde
                self.playing = False
                self.running = False

    def update(self):
        # Game Loop Updates

        # Jedes Element in der Liste all_sprites überprüft ob dessen Klasse (z.B. Player, Enemy, Wall, ...)
        # eine Funktion update() besitzt und falls ja wird diese aufgerufen
        self.all_sprites.update()

    def draw(self):
        # Game Loop Draw
        # Zeichne einen schwarzen Bildschirm
        self.screen.fill(BLACK)
        # Jedes Element in der list all_sprites überprüft ob dessen Klasse (z.B. Player, Enemy, Wall, ...)
        # ein Objekt "image" und "rect" besitzt und falls ja  wird dieses wiedergegeben
        self.all_sprites.draw(self.screen)
        # Update den Bildschirm mit 60 FPS
        self.clock.tick(FPS)
        # Update den Bildschirm
        pygame.display.update()

    def main(self):
        # Game Loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def intro_screen(self):
        pass

    def game_over(self):
        pass


# Generiere ein Elment der Klasse Game
g = Game()
# Gebe den Startbildschirm wieder
g.intro_screen()
# Generiere alle Spielelemente (z.B. Player, Enemy, Wall, ...)
g.new()

# Spieliteration
while g.running:
    g.main()
    # Überprüfe ob die Bediengung für Game Over erfüllt wurde
    g.game_over()

# Beende das Spiel wenn Paramter/Variable running=False
pygame.quit()
sys.exit()
