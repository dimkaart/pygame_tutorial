# HD Auflösung
WIN_BREITE = 1280
WIN_HOEHE = 960

# Bildschirmwiederholungsrate
FPS = 60

# Spielname
GAME_TITLE = "Bestes RPG aller Zeiten"

# Spielicon (from https://itch.io/game-assets/free/tag-icons)
ICON_NAME = "Assets/Images/game_icon.png"

# Darstellung von Assets übereinander im Spiel (nach Ebenen)
PLAYER_EBENE = 3
BLOCK_EBENE = 2
GROUND_EBENE = 1

# Geschwindigkeit mit der sich der Spieler auf dem Feld bewegt
PLAYER_SPEED = 4

# Kachelgröße
TILESIZE = 32

# Farben (R,G,B)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# 40 x 30 Quadrate á 32px (Breite x Höhe) stellen das "Spielfeld" dar (1280x960)
# 'B' = Wand (Block)
# '.' = Leere Feld/Gras
# 'P' = Spieler (Player)
# '1' = Health +25
# '2' = Health +50
# 'E' = Gegner (Enemy)
tilemap = [
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
    "B......................................B",
    "B......................................B",
    "B..P...................................B",
    "B.............................BBB......B",
    "B......................................B",
    "B......BBBB............................B",
    "B.........B............................B",
    "B.........BBBB.........................B",
    "B......................................B",
    "B......................................B",
    "B......................................B",
    "B......................................B",
    "B......................BBBB............B",
    "B......................BBBB............B",
    "B.........................B............B",
    "B.........................B............B",
    "B.........................BBBBB........B",
    "B......................................B",
    "B......................................B",
    "B......................................B",
    "B..............................BBB.....B",
    "B...........................BBB........B",
    "B........................BBB...........B",
    "B........BBBB.........BBB..............B",
    "B............BBBB......................B",
    "B................BBBB...B..............B",
    "B...................B...B..............B",
    "B...................B...B..............B",
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
]
