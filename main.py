import sys

import pygame
from settings import *
from sprites import *

pygame.mixer.init()
# Lade sounds vor, damit diese sofort nach Knopfdruck gespielt werden
pygame.mixer.pre_init(44100, -16, 2, 512)


class Game:
    def __init__(self):
        pygame.init()
        # Bildschirmauflösung
        self.screen = pygame.display.set_mode((WIN_BREITE, WIN_HOEHE))
        # Bildschirmwiederholung
        self.clock = pygame.time.Clock()
        # Schrifttext
        self.font = pygame.font.Font("Assets/Fonts/arial.ttf", 64)
        # Status des Spiels (wird später zum stoppen des Spiels benötigt)
        self.running = True
        # Spielname
        self.game_title = pygame.display.set_caption(GAME_TITLE)
        # Spielicon
        icon = pygame.image.load(ICON_NAME)
        self.game_icon = pygame.display.set_icon(icon)
        # Lade sämtliche Spritesheets (Character, Gegner, Wiesen, Heiltränke, etc.)
        self.character_spritesheet = Spritesheet("Assets/Images/character.png")
        self.terrain_spritesheet = Spritesheet("Assets/Images/Outdoor.png")
        self.enemy_spritesheet = Spritesheet("Assets/Images/enemy.png")
        self.attack_spritesheet = Spritesheet("Assets/Images/attack.png")
        self.health_spritesheet = Spritesheet("Assets/Images/health.png")
        self.item_spritesheet = Spritesheet("Assets/Images/items.png")

        # Lade Hintergrund für Startbildschirm
        self.intro_background = pygame.image.load("Assets/Images/introbackground.png")
        # Lade Hintergrund für Endbildschirm
        self.gameover_background = pygame.image.load("Assets/Images/gameover.png")

        self.timestamp_enemy = pygame.time.get_ticks()
        self.timestamp_healing = pygame.time.get_ticks()

        self.font_points = pygame.font.Font("Assets/Fonts/arial.ttf", 32)

        self.volume = VOLUME

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                elif column == "E":
                    Enemy(self, j, i)
                elif column == "P":
                    self.player = Player(self, j, i)
                elif column == "1":
                    HealingItem(self, j, i, 25)
                elif column == "2":
                    HealingItem(self, j, i, 50)

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

        ## Spieler hinzufügen
        # self.player = Player(self, 1, 2)  # self ist das Game Objekt
        # Ganzes Spielfeld zeichnen statt nur Spieler
        self.createTilemap()

    def events(self):
        # Game Loop Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT überprüft ob das Spiel mittels "x" beendet wurde
                self.playing = False
                self.running = False

            # Attacke mit Leertaste
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Attacke mit der Maus
                    # if event.type == pygame.MOUSEBUTTONDOWN:
                    #    if event.button == 1:
                    # Position der Attacke is abhängig von der Position des Spielers und der Richtung in die er schaut
                    # --> self.player muss in der Funktion createTilemap definiert werden
                    if self.player.facing == "up":
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                        # Animation findet über dem Spieler statt
                        # '-' weger der Weise wie das Spielfeld definiert wird mit (0,0) in der oberen linken Ecke jeweils
                    if self.player.facing == "down":
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == "left":
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == "right":
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

            timeStamp_enemy = pygame.time.get_ticks()
            if timeStamp_enemy - self.timestamp_enemy >= ENEMY_RESPAWN_TIME:  # 500 Millisekunden sind 0,5 Seknuden
                self.random_enemy_generator()
                self.timestamp_enemy = timeStamp_enemy  # Starte den Timer für Enemy neu

            timeStamp_healing = pygame.time.get_ticks()
            if timeStamp_healing - self.timestamp_healing >= HEALINGITEM_RESPAWN_TIME:
                self.random_healingItem_generator()
                self.timestamp_healing = timeStamp_healing  # Starte den Time für Healing Items neu

    def random_enemy_generator(self):
        x_position = random.randint(2, (WIN_BREITE // TILESIZE) - 2)
        y_position = random.randint(2, (WIN_HOEHE // TILESIZE) - 2)

        Enemy(self, x_position, y_position)

    def random_healingItem_generator(self):
        x_position = random.randint(2, (WIN_BREITE // TILESIZE) - 2)
        y_position = random.randint(2, (WIN_HOEHE // TILESIZE) - 2)

        rand = random.random()

        if rand < 0.66:
            HealingItem(self, x_position, y_position, 25)
        else:
            HealingItem(self, x_position, y_position, 50)

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

        # Stelle den aktuellen Punktestand dar
        score_text = self.font_points.render(f"{self.player.gamepoints.points}", True, WHITE)
        self.screen.blit(score_text, (WIN_BREITE - 2 * TILESIZE, 0))

        # Update den Bildschirm
        pygame.display.update()

    def main(self):
        pygame.mixer.music.load("Assets/Music/Track/game_music.wav")
        pygame.mixer.music.set_volume(self.volume - 50)
        pygame.mixer.music.play(-1)  # -1 spielt die Musik unendlich Mal weiter (x>=0: Musik wird x Mal wiedergegeben)

        # Game Loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def intro_screen(self):
        # Variable die angibt ob der Startbildschirm weiterhin angezeigt werden soll
        intro = True

        # Definiere den Title des Spiels
        title = self.font.render(GAME_TITLE, True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        # Definiere einen Knopf mittels unserer Button Klasse
        play_button = Button(10, 100, 200, 100, WHITE, BLACK, "Play", 64)

        # Lade Musik fpr Startbildschirm
        pygame.mixer.music.load("Assets/Music/Track/intro_music.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

        # Überprüfen ob das Spiel mittels "X" in der rechten oberen Ecke geschlossen wurde
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            # Erfahre die Position der Maus
            mouse_pos = pygame.mouse.get_pos()
            # Erfahre welcher Knopf der Maus gedrückt wurde
            # 0: linke Taste ; 1: rechte Taste ; 2: mittlere Taste
            mouse_pressed = pygame.mouse.get_pressed()
            # Überprüfe ob der Play Knopf gedrückt wurde, wenn ja beende den Startbildschirm
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            # Projeziiere alle Elemente übereinander in ein Bild
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)

            pygame.display.update()

    def game_over(self):
        # Definiere den Text, welcher angezeigt wird wenn man verliert
        text = self.font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIN_BREITE // 2, WIN_HOEHE // 2))

        # Definiere einen Knopf Restart, um das Spiel neu zu starten
        restart_button = Button(10, 100, 250, 150, WHITE, BLACK, "Restart", 64)
        # Definiere einen Knopf Punkte, um den Spielstand wiederzugeben
        points_button = Button(800, 100, 350, 150, WHITE, BLACK, f"Punkte: {self.player.gamepoints.points}", 48)

        # Fadeout für die Spielmusik
        pygame.mixer.music.fadeout(1000)
        # Lade Musik für Endbildschirm
        pygame.mixer.music.load("Assets/Music/Track/gameover_INITIAL.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(0)

        # Lösche alle Elemente auf derm Bildschirm um nur den Endbildschirm anzeigen zu lassen
        for sprite in self.all_sprites:
            sprite.kill()

        # Event Loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Efahre die Position der Maus
                mouse_pos = pygame.mouse.get_pos()
                # Erfahre welecher Knopf auf dre Maus gedrückt wurde
                mouse_pressed = pygame.mouse.get_pressed()

                # Überprüfe ob der Restart Knopf gedrückt wurde, wenn ja Starte das Spiel neu
                if restart_button.is_pressed(mouse_pos, mouse_pressed):
                    self.new()
                    self.main()
                    self.game_over()

                # Projeziere alle Elemente übereineader in ein Bild
                self.screen.blit(self.gameover_background, (0, 0))
                self.screen.blit(text, text_rect)
                self.screen.blit(restart_button.image, restart_button.rect)
                self.screen.blit(points_button.image, points_button.rect)
                self.clock.tick(FPS)

                pygame.display.update()


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
