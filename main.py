import sys
import pygame
from pygame.locals import *
import pymysql
from grille import Grille
from player import Player
from config import *

# initialisation de Pygame
pygame.init()

# création de la fenêtre
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption(TITRE)

# chargement de l'image de fond
background = pygame.image.load("img/back.png")

# création de la grille et du joueur
_grille = Grille("lvl/lv1")
_grille.drawMap(screen)
_player = Player(_grille)
_player.drawPlayer(screen)

# affichage de la fenêtre
pygame.display.flip()

# connexion à la base de données
conn = pymysql.connect(host="localhost", user="root",
                    password="", database="sokoban")
c = conn.cursor()

# création de la table des scores si elle n'existe pas déjà
c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTO_INCREMENT, id_joueur TEXT, niveau INTEGER, score INTEGER)")

# boucle principale du jeu
continuer = True
while not _grille.is_fini():
    for event in pygame.event.get():
        if event.type == QUIT:
            # sauvegarde du score dans la base de données avant de quitter
            _grille.set_niveau(1)  # définir le niveau atteint
            _player.set_id_joueur("joueur1")  # définir l'identifiant du joueur
            query = "INSERT INTO scores (id_joueur, niveau, score) VALUES (%s, %s, %s)"
            params = (_player.id_joueur, _grille.niveau, _player.score)
            c.execute(query, params)
            conn.commit()
            sys.exit()
        if event.type == KEYDOWN:
            _player.move(event.key)
            if event.key == K_r:
                # régénération de la grille et du joueur
                _grille.genMap("lvl/lv1")
                _grille.drawMap(screen)
                _player = Player(_grille)
                _player.drawPlayer(screen)

    # affichage de l'image de fond, de la grille et du joueur
    screen.blit(background, (0, 0))
    _grille.drawMap(screen)
    _player.drawPlayer(screen)

    # actualisation de la fenêtre
    pygame.display.flip()

# sauvegarde du score dans la base de données à la fin du niveau
_grille.set_niveau(1)  # définir le niveau atteint
_player.set_id_joueur("joueur1")  # définir l'identifiant du joueur
query = "INSERT INTO scores (id_joueur, niveau, score) VALUES (%s, %s, %s)"
params = (_player.id_joueur, _grille.niveau, _player.score)
c.execute(query, params)

# affichage des scores des joueurs
query = "SELECT id_joueur, niveau, score FROM scores ORDER BY score DESC"
c.execute(query)
scores = c.fetchall()
conn.commit()
conn.close()

print("Classement :")
for score in scores:
    print(
        "- Joueur {}, niveau {}, score {}".format(score[0], score[1], score[2]))
