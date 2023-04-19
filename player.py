import pygame
from pygame.locals import *
from grille import Grille
from config import *

pygame.init()
pygame.mixer.init()

class Player:
    def __init__(self, grille):
        pygame.mixer.music.load("son/game-music-loop-2-144037.mp3")
        pygame.mixer.music.set_volume(0.5) # volume réglé à 50%
        pygame.mixer.music.play()

        self.gauche = pygame.image.load("img/mario_gauche.gif")
        self.droite = pygame.image.load("img/mario_droite.gif")
        self.bas = pygame.image.load("img/mario_bas.gif")
        self.haut = pygame.image.load("img/mario_haut.gif")

        self.position = self.droite

        self.grille = grille
        self.pos = self.grille.getPlayerPosition(self.grille)

        self.x = self.pos[0] // SIZE 
        self.y = self.pos[1] // SIZE
        self.id_joueur = None
        self.score = 0  # initialisation du score à 0

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score
        
    def set_id_joueur(self, id_joueur):
        self.id_joueur = id_joueur

    def drawPlayer(self, screen):
        screen.blit(self.position, (self.x * SIZE, self.y * SIZE))

    def move(self, key):
        if key == K_LEFT:
            self.position = self.gauche
            if not self.checkCollision():
                self.x -= 1
                pygame.mixer.Sound('son/move.wav').play()
        elif key == K_RIGHT:
            self.position = self.droite
            if not self.checkCollision():
                self.x += 1
                pygame.mixer.Sound('son/move.wav').play()
        elif key == K_UP:
            self.position = self.haut
            if not self.checkCollision():
                self.y -= 1
                pygame.mixer.Sound('son/move.wav').play()
        elif key == K_DOWN:
            self.position = self.bas
            if not self.checkCollision():
                self.y += 1
                pygame.mixer.Sound('son/move.wav').play()

    def checkCollision(self):
        self.hauty = self.y - 1
        self.basy = self.y + 1
        self.droitex = self.x + 1
        self.gauchex = self.x - 1

        for y in range(len(self.grille.lvtest)):
            for x in range(len(self.grille.lvtest[y])):
                if self.position == self.gauche:
                    pos_grille = self.grille.lvtest[self.y][self.gauchex]
                    if pos_grille == CAISSE or pos_grille == CAISSE_OK:
                        a = self.grille.moveCaisse(self.x, self.y, "gauche")
                        if a:
                            self.x = self.gauchex
                            son_caisse = pygame.mixer.Sound("son/son_caisse.wav")
                            son_caisse.play()
                    return pos_grille == MUR or pos_grille == CAISSE or pos_grille == CAISSE_OK
                elif self.position == self.droite:
                    pos_grille = self.grille.lvtest[self.y][self.droitex]
                    if pos_grille == CAISSE or pos_grille == CAISSE_OK:
                        a = self.grille.moveCaisse(self.x, self.y, "droite")
                        if a:
                            self.x = self.droitex
                            son_caisse = pygame.mixer.Sound("son/son_caisse.wav")
                            son_caisse.play()
                    return pos_grille == MUR or pos_grille == CAISSE or pos_grille == CAISSE_OK
                elif self.position == self.haut:
                    pos_grille = self.grille.lvtest[self.hauty][self.x]
                    if pos_grille == CAISSE or pos_grille == CAISSE_OK:
                        a = self.grille.moveCaisse(self.x, self.y, "haut")
                        if a:
                            self.y = self.hauty
                            son_caisse = pygame.mixer.Sound("son/son_caisse.wav")
                            son_caisse.play()
                    return pos_grille == MUR or pos_grille == CAISSE or pos_grille == CAISSE_OK
                elif self.position == self.bas:
                    pos_grille = self.grille.lvtest[self.basy][self.x]
                    if pos_grille == CAISSE or pos_grille == CAISSE_OK:
                        a = self.grille.moveCaisse(self.x , self.y, "bas")
                        if a:
                            self.y = self.basy
                            son_caisse = pygame.mixer.Sound("son/son_caisse.wav")
                            son_caisse.play()
                    return pos_grille == MUR or pos_grille == CAISSE or pos_grille == CAISSE_OK

def __del__(self):
    pygame.mixer.music.stop()
