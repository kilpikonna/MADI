from StartMe import *
import pygame
from pygame.locals import *
import time
import random


pygame.init()

fenetre = pygame.display.set_mode((800, 800))

sol = pygame.image.load("sol.jpg").convert()
mur = pygame.image.load("mur.jpg").convert()
platform = pygame.image.load("platform.jpg").convert()
monster = pygame.transform.scale(pygame.image.load("monster.png").convert_alpha(), (100, 100))
perso = pygame.transform.scale(pygame.image.load("perso.png").convert_alpha(), (60, 100))
portail = pygame.transform.scale(pygame.image.load("portail.png").convert_alpha(), (100, 100))
porte = pygame.transform.scale(pygame.image.load("porte.png").convert_alpha(), (100, 100))
sword = pygame.transform.scale(pygame.image.load("sword.png").convert_alpha(), (100, 100))
tresor = pygame.transform.scale(pygame.image.load("tresor.png").convert_alpha(), (100, 100))
cle = pygame.transform.scale(pygame.image.load("cle.png").convert_alpha(), (100, 100))
crack = pygame.transform.scale(pygame.image.load("crack.png").convert_alpha(), (100, 100))
glace = pygame.transform.scale(pygame.image.load("glace.png").convert_alpha(), (100, 100))
start = pygame.transform.scale(pygame.image.load("depart.png").convert_alpha(), (100, 100))


def affiche(fen, lvl, per):
	for i in range(len(lvl.matrix)):
		for j in range(len(lvl.matrix)):
			fen.blit(sol, (j * 100, i * 100))
			if D_SHORTS["O"] == lvl.matrix[i][j]:
				fen.blit(start, (j * 100, i * 100))
			if D_SHORTS["E"] == lvl.matrix[i][j] and (i, j) in lvl.enemies :
				fen.blit(monster, (j * 100, i * 100))
			if D_SHORTS["W"] == lvl.matrix[i][j]:
				fen.blit(mur, (j * 100, i * 100))
			if D_SHORTS["R"] == lvl.matrix[i][j]:
				fen.blit(porte, (j * 100, i * 100))
			if D_SHORTS["C"] == lvl.matrix[i][j]:
				fen.blit(crack, (j * 100, i * 100))
			if D_SHORTS["S"] == lvl.matrix[i][j] and not(per.havesword):
				fen.blit(sword, (j * 100, i * 100))
			if D_SHORTS["K"] == lvl.matrix[i][j] and not(per.havekey):
				fen.blit(cle, (j * 100, i * 100))
			if D_SHORTS["P"] == lvl.matrix[i][j]:
				fen.blit(portail, (j * 100, i * 100))
			if D_SHORTS["-"] == lvl.matrix[i][j]:
				fen.blit(platform, (j * 100, i * 100))
			if D_SHORTS["T"] == lvl.matrix[i][j] and not(per.havetreasure):
				fen.blit(tresor, (j * 100, i * 100))
			if D_SHORTS["F"] == lvl.matrix[i][j]:
				fen.blit(glace, (j * 100, i * 100))
			fen.blit(perso, (per.x * 100, per.y * 100))
	return

class Perso():
	def __init__(self, lvl):
		self.havesword = 0
		self.havekey = 0
		self.havetreasure = 0
		self.dead = 0
		for i in range(len(lvl)):
			for j in range(len(lvl)):
				if lvl[i][j] == D_SHORTS["O"]:
					self.x = j
					self.y = i

	def deplace(self, dir, lvl):
		if dir == 1 and self.y > 0:
			if lvl.matrix[self.y - 1][self.x] != D_SHORTS["W"]:
				self.y -= 1
		if dir == 3 and self.y < len(lvl.matrix) - 1:
			if lvl.matrix[self.y + 1][self.x] != D_SHORTS["W"]:
				self.y += 1
		if dir == 2 and self.x < len(lvl.matrix) - 1:
			if lvl.matrix[self.y][self.x + 1] != D_SHORTS["W"]:
				self.x += 1
		if dir == 4 and self.x > 0:
			if lvl.matrix[self.y][self.x - 1] != D_SHORTS["W"]:
				self.x -= 1
		if lvl.matrix[self.y][self.x] == D_SHORTS["S"]:
			self.havesword = 1
		if lvl.matrix[self.y][self.x] == D_SHORTS["K"]:
			self.havekey = 1
		if lvl.matrix[self.y][self.x] == D_SHORTS["T"] and self.havekey:
			self.havetreasure = 1
		if lvl.matrix[self.y][self.x] == D_SHORTS["F"]:
			time.sleep(2)
		if lvl.matrix[self.y][self.x] == D_SHORTS["E"] and (self.y, self.x) in lvl.enemies:
			p = random.random()
			if p < 0.7 or self.havesword:
				lvl.enemies.remove((self.y, self.x))
			else:
				self.dead = 1
		if lvl.matrix[self.y][self.x] == D_SHORTS["C"]:
			self.dead = 1
		if lvl.matrix[self.y][self.x] == D_SHORTS["P"]:
			r_x = random.randrange(len(lvl.matrix))
			r_y = random.randrange(len(lvl.matrix))
			while lvl.matrix[r_y][r_x] == D_SHORTS["W"]:
				r_x = random.randrange(len(lvl.matrix))
				r_y = random.randrange(len(lvl.matrix))
			self.x = r_x
			self.y = r_y
			self.deplace(0, lvl)
		if lvl.matrix[self.y][self.x] == D_SHORTS["-"]:
			l = []
			if self.y > 0 and lvl.matrix[self.y - 1][self.x] != D_SHORTS["W"]:
				l.append(1)
			if self.x > 0 and lvl.matrix[self.y][self.x - 1] != D_SHORTS["W"]:
				l.append(4)
			if self.y < len(lvl.matrix) - 1 and lvl.matrix[self.y + 1][self.x] != D_SHORTS["W"]:
				l.append(3)
			if self.x < len(lvl.matrix) - 1 and lvl.matrix[self.y][self.x + 1] != D_SHORTS["W"]:
				l.append(2)
			if l != []:
				self.deplace(random.choice(l), lvl)
		if lvl.matrix[self.y][self.x] == D_SHORTS["R"]:
			p = random.random()
			if p < 0.1:
				self.dead = 1
			if p < 0.4 and p >= 0.1:
				for i in range(len(lvl.matrix)):
					for j in range(len(lvl.matrix)):
						if lvl.matrix[i][j] == D_SHORTS["O"]:
							self.x = j
							self.y = i










continuer = 1

while continuer:
	continuer_accueil_1 = 1
	continuer_accueil_2 = 1
	continuer_jeu = 1
	fini = 1
	mode = 0
	while continuer_accueil_1:
		background = pygame.Surface(fenetre.get_size())
		background = background.convert()
		background.fill((0, 0, 0))
		fenetre.blit(background, (0, 0))

		# Affichage d'un texte
		font = pygame.font.Font(None, 36)
		text = font.render("Veuillez choisir un niveau :", 1, (250, 250, 250))
		fenetre.blit(text, (0, 0))

		font = pygame.font.Font(None, 36)
		text = font.render("Appuyer sur F1 pour l'instance du sujet", 1, (250, 250, 250))
		fenetre.blit(text, (0, 50))

		font = pygame.font.Font(None, 36)
		text = font.render("Appuyer sur F2 pour l'instance test", 1, (250, 250, 250))
		fenetre.blit(text, (0, 100))

		font = pygame.font.Font(None, 36)
		text = font.render("Appuyer sur F3 pour un niveau aleatoire", 1, (250, 250, 250))
		fenetre.blit(text, (0, 150))

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
				continuer_accueil_1 = 0
				continuer_accueil_2 = 0
				continuer_jeu = 0
				fini = 0
			if event.type == KEYDOWN:
				if event.key == K_F1 :
					dg = DungeonMatrix("instance_subject.txt")
					personnage = Perso(dg.matrix)
					continuer_accueil_1 = 0
				if event.key == K_F2 :
					dg = DungeonMatrix("instance_test.txt")
					personnage = Perso(dg.matrix)
					continuer_accueil_1 = 0
				if event.key == K_F3:
					dg = DungeonMatrix(7)
					personnage = Perso(dg.matrix)
					continuer_accueil_1 = 0

	while continuer_accueil_2:
		background = pygame.Surface(fenetre.get_size())
		background = background.convert()
		background.fill((0, 0, 0))
		fenetre.blit(background, (0, 0))

		# Affichage d'un texte
		font = pygame.font.Font(None, 36)
		text = font.render("Veuillez choisir un mode de jeu :", 1, (250, 250, 250))
		fenetre.blit(text, (0, 0))

		font = pygame.font.Font(None, 36)
		text = font.render("Appuyer sur F1 pour le mode manuel", 1, (250, 250, 250))
		fenetre.blit(text, (0, 50))

		font = pygame.font.Font(None, 36)
		text = font.render("Appuyer sur F2 pour l'itération de la valeur", 1, (250, 250, 250))
		fenetre.blit(text, (0, 100))

		font = pygame.font.Font(None, 36)
		text = font.render("Appuyer sur F3 pour l'itération de la politique", 1, (250, 250, 250))
		fenetre.blit(text, (0, 150))

		font = pygame.font.Font(None, 36)
		text = font.render("Appuyer sur F4 pour le Q-learning", 1, (250, 250, 250))
		fenetre.blit(text, (0, 200))

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
				continuer_accueil_1 = 0
				continuer_accueil_2 = 0
				continuer_jeu = 0
				fini = 0
			if event.type == KEYDOWN:
				if event.key == K_F1 :
					mode = 1
					continuer_accueil_2 = 0
				if event.key == K_F2 :
					mode = 2
					mdp = MDP(dg.matrix)
					strat = mdp.value_iteration(0.01)
					continuer_accueil_2 = 0
				if event.key == K_F3:
					mode = 3
					mdp = MDP(dg.matrix)
					strat = mdp.policy_iteration()
					continuer_accueil_2 = 0
				if event.key == K_F4:
					mode = 4
					strat = QLearning(dg.matrix)
					strat.q_learning()
					continuer_accueil_2 = 0

	background = pygame.Surface(fenetre.get_size())
	background = background.convert()
	background.fill((0, 0, 0))
	fenetre.blit(background, (0, 0))
	affiche(fenetre, dg, personnage)
	pygame.display.flip()

	while continuer_jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer_jeu = 0
				continuer = 0
				fini = 0
			if mode == 1:
				if event.type == KEYDOWN:
					if event.key == K_UP:
						personnage.deplace(1, dg)
					if event.key == K_DOWN:
						personnage.deplace(3, dg)
					if event.key == K_RIGHT:
						personnage.deplace(2, dg)
					if event.key == K_LEFT:
						personnage.deplace(4, dg)
		if mode > 1:
			if not(personnage.havesword) and not(personnage.havetreasure) and not(personnage.havekey):
				personnage.deplace(strat[0][personnage.y][personnage.x], dg)
				time.sleep(1)
			if personnage.havesword and not(personnage.havetreasure) and not(personnage.havekey):
				personnage.deplace(strat[1][personnage.y][personnage.x], dg)
				time.sleep(1)
			if not(personnage.havesword) and not(personnage.havetreasure) and personnage.havekey:
				personnage.deplace(strat[2][personnage.y][personnage.x], dg)
				time.sleep(1)
			if personnage.havesword and not(personnage.havetreasure) and personnage.havekey:
				personnage.deplace(strat[3][personnage.y][personnage.x], dg)
				time.sleep(1)
			if not(personnage.havesword) and personnage.havetreasure and personnage.havekey:
				personnage.deplace(strat[4][personnage.y][personnage.x], dg)
				time.sleep(1)
			if personnage.havesword and personnage.havetreasure and personnage.havekey:
				personnage.deplace(strat[5][personnage.y][personnage.x], dg)
				time.sleep(1)
		affiche(fenetre, dg, personnage)
		pygame.display.flip()

		if personnage.dead:
			continuer_jeu = 0
		if personnage.havetreasure and D_SHORTS["O"] == dg.matrix[personnage.y][personnage.x]:
			continuer_jeu = 0

	while fini:
		if personnage.dead:
			background = pygame.Surface(fenetre.get_size())
			background = background.convert()
			background.fill((0, 0, 0))
			fenetre.blit(background, (0, 0))
			font = pygame.font.Font(None, 36)
			text = font.render("Perdu", 1, (250, 250, 250))
			fenetre.blit(text, (0, 0))
			font = pygame.font.Font(None, 36)
			text = font.render("Appuyer sur espace pour continuer", 1, (250, 250, 250))
			fenetre.blit(text, (0, 50))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == QUIT:
					fini = 0
					continuer = 0
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						fini = 0

		if personnage.havetreasure and D_SHORTS["O"] == dg.matrix[personnage.y][personnage.x]:
			background = pygame.Surface(fenetre.get_size())
			background = background.convert()
			background.fill((0, 0, 0))
			fenetre.blit(background, (0, 0))
			font = pygame.font.Font(None, 36)
			text = font.render("Gagne", 1, (250, 250, 250))
			fenetre.blit(text, (0, 0))
			font = pygame.font.Font(None, 36)
			text = font.render("Appuyer sur espace pour continuer", 1, (250, 250, 250))
			fenetre.blit(text, (0, 50))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == QUIT:
					fini = 0
					continuer = 0
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						fini = 0

