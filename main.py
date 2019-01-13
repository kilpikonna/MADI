from StartMe import *
import pygame
from pygame.locals import *
import time
import random
import copy


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

sol_1 = pygame.image.load("sol_1.jpg").convert()
mur_1 = pygame.image.load("mur_1.jpg").convert()
platform_1 = pygame.image.load("platform.jpg").convert()
monster_1 = pygame.transform.scale(pygame.image.load("monster_1.png").convert_alpha(), (100, 100))
portail_1 = pygame.transform.scale(pygame.image.load("portail.png").convert_alpha(), (100, 100))
porte_1 = pygame.transform.scale(pygame.image.load("porte_1.png").convert_alpha(), (100, 100))
sword_1 = pygame.transform.scale(pygame.image.load("sword_1.png").convert_alpha(), (100, 100))
tresor_1 = pygame.transform.scale(pygame.image.load("tresor_1.png").convert_alpha(), (100, 100))
cle_1 = pygame.transform.scale(pygame.image.load("cle_1.png").convert_alpha(), (100, 100))
crack_1 = pygame.transform.scale(pygame.image.load("crack_1.png").convert_alpha(), (100, 100))
glace_1 = pygame.transform.scale(pygame.image.load("glace_1.png").convert_alpha(), (100, 100))
start_1 = pygame.transform.scale(pygame.image.load("depart_1.png").convert_alpha(), (100, 100))

sol_2 = pygame.image.load("sol_2.jpg").convert()
mur_2 = pygame.image.load("mur_2.jpg").convert()
platform_2 = pygame.image.load("platform.jpg").convert()
monster_2 = pygame.transform.scale(pygame.image.load("monster_2.png").convert_alpha(), (100, 100))
portail_2 = pygame.transform.scale(pygame.image.load("portail.png").convert_alpha(), (100, 100))
porte_2 = pygame.transform.scale(pygame.image.load("porte_2.png").convert_alpha(), (100, 100))
sword_2 = pygame.transform.scale(pygame.image.load("sword_2.png").convert_alpha(), (100, 100))
tresor_2 = pygame.transform.scale(pygame.image.load("tresor_2.png").convert_alpha(), (100, 100))
cle_2 = pygame.transform.scale(pygame.image.load("cle_2.png").convert_alpha(), (100, 100))
crack_2 = pygame.transform.scale(pygame.image.load("crack_2.png").convert_alpha(), (100, 100))
glace_2 = pygame.transform.scale(pygame.image.load("glace_2.png").convert_alpha(), (100, 100))
start_2 = pygame.transform.scale(pygame.image.load("depart_2.png").convert_alpha(), (100, 100))

sol_3 = pygame.image.load("sol_3.jpg").convert()
mur_3 = pygame.image.load("mur_3.jpg").convert()
platform_3 = pygame.image.load("platform.jpg").convert()
monster_3 = pygame.transform.scale(pygame.image.load("monster_3.png").convert_alpha(), (100, 100))
portail_3 = pygame.transform.scale(pygame.image.load("portail.png").convert_alpha(), (100, 100))
porte_3 = pygame.transform.scale(pygame.image.load("porte_3.png").convert_alpha(), (100, 100))
sword_3 = pygame.transform.scale(pygame.image.load("sword_3.png").convert_alpha(), (100, 100))
tresor_3 = pygame.transform.scale(pygame.image.load("tresor_3.png").convert_alpha(), (100, 100))
cle_3 = pygame.transform.scale(pygame.image.load("cle_3.png").convert_alpha(), (100, 100))
crack_3 = pygame.transform.scale(pygame.image.load("crack_3.png").convert_alpha(), (100, 100))
glace_3 = pygame.transform.scale(pygame.image.load("glace_3.png").convert_alpha(), (100, 100))
start_3 = pygame.transform.scale(pygame.image.load("depart_3.png").convert_alpha(), (100, 100))

sol_4 = pygame.image.load("sol_4.jpg").convert()
mur_4 = pygame.image.load("mur_4.jpg").convert()
platform_4 = pygame.image.load("platform.jpg").convert()
monster_4 = pygame.transform.scale(pygame.image.load("monster_4.png").convert_alpha(), (100, 100))
portail_4 = pygame.transform.scale(pygame.image.load("portail.png").convert_alpha(), (100, 100))
porte_4 = pygame.transform.scale(pygame.image.load("porte_4.png").convert_alpha(), (100, 100))
sword_4 = pygame.transform.scale(pygame.image.load("sword_4.png").convert_alpha(), (100, 100))
tresor_4 = pygame.transform.scale(pygame.image.load("tresor_4.png").convert_alpha(), (100, 100))
cle_4 = pygame.transform.scale(pygame.image.load("cle_4.png").convert_alpha(), (100, 100))
crack_4 = pygame.transform.scale(pygame.image.load("crack_4.png").convert_alpha(), (100, 100))
glace_4 = pygame.transform.scale(pygame.image.load("glace_4.png").convert_alpha(), (100, 100))
start_4 = pygame.transform.scale(pygame.image.load("depart_4.png").convert_alpha(), (100, 100))

l_sol = [sol, sol_1, sol_2, sol_3, sol_4]
l_mur = [mur, mur_1, mur_2, mur_3, mur_4]
l_platform = [platform, platform_1, platform_2, platform_3, platform_4]
l_monster = [monster, monster_1, monster_2, monster_3, monster_4]
l_portail = [portail, portail_1, portail_2, portail_3, portail_4]
l_porte = [porte, porte_1, porte_2, porte_3, porte_4]
l_sword = [sword, sword_1, sword_2, sword_3, sword_4]
l_tresor = [tresor, tresor_1, tresor_2, tresor_3, tresor_4]
l_cle = [cle, cle_1, cle_2, cle_3, cle_4]
l_crack = [crack, crack_1, crack_2, crack_3, crack_4]
l_glace = [glace, glace_1, glace_2, glace_3, glace_4]
l_start = [start, start_1, start_2, start_3, start_4]



def affiche_strat(fen, lvl, dec):
	print(dec)
	for i in range(len(lvl.matrix)):
		for j in range(len(lvl.matrix)):
			fen.blit(sol, (j * 100, i * 100))
			if D_SHORTS["O"] == lvl.matrix[i][j]:
				fen.blit(l_start[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["."] == lvl.matrix[i][j]:
				fen.blit(l_sol[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["E"] == lvl.matrix[i][j]:
				fen.blit(l_monster[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["W"] == lvl.matrix[i][j]:
				fen.blit(l_mur[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["R"] == lvl.matrix[i][j]:
				fen.blit(l_porte[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["C"] == lvl.matrix[i][j]:
				fen.blit(l_crack[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["S"] == lvl.matrix[i][j] :
				fen.blit(l_sword[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["K"] == lvl.matrix[i][j] :
				fen.blit(l_cle[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["P"] == lvl.matrix[i][j]:
				fen.blit(l_portail[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["-"] == lvl.matrix[i][j]:
				fen.blit(l_platform[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["T"] == lvl.matrix[i][j] :
				fen.blit(l_tresor[dec[i][j]], (j * 100, i * 100))
			if D_SHORTS["F"] == lvl.matrix[i][j]:
				fen.blit(glace, (j * 100, i * 100))
			#fen.blit(perso, (per.x * 100, per.y * 100))
	return

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
			#½if lvl.matrix[self.y - 1][self.x] != D_SHORTS["W"]:
			self.y -= 1
		if dir == 3 and self.y < len(lvl.matrix) - 1:
			#if lvl.matrix[self.y + 1][self.x] != D_SHORTS["W"]:
			self.y += 1
		if dir == 2 and self.x < len(lvl.matrix) - 1:
			#if lvl.matrix[self.y][self.x + 1] != D_SHORTS["W"]:
			self.x += 1
		if dir == 4 and self.x > 0:
			#if lvl.matrix[self.y][self.x - 1] != D_SHORTS["W"]:
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
		if lvl.matrix[self.y][self.x] == D_SHORTS["W"]:
			for i in range(len(lvl.matrix)):
					for j in range(len(lvl.matrix)):
						if lvl.matrix[i][j] == D_SHORTS["O"]:
							self.x = j
							self.y = i









dg = None 
dg_old = None
continuer = 1
nouveau_essaie = 0
strat = None
mode = 0
affiche_strategy = 0
etape = 0

while continuer:
	print(nouveau_essaie)
	if nouveau_essaie == 0 :
		print("nouveau game")
		continuer_accueil_1 = 1
		continuer_accueil_2 = 1
		continuer_jeu = 1
		fini = 1
		mode = 0
	else :
		print("nouveau essaie")
		continuer_accueil_1 = 0
		continuer_accueil_2 = 0
		continuer_jeu = 1
		fini = 1
		#mode = 0

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
					dg_old = DungeonMatrix("instance_subject.txt")
					personnage = Perso(dg.matrix)
					continuer_accueil_1 = 0
				if event.key == K_F2 :
					dg = DungeonMatrix("instance_test.txt")
					dg_old = DungeonMatrix("instance_test.txt")
					personnage = Perso(dg.matrix)
					continuer_accueil_1 = 0
				if event.key == K_F3:
					dg = DungeonMatrix(8)
					dg_old = copy.deepcopy(dg)
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
					ql = QLearning(dg.matrix)
					strat = ql.q_learning()
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
				dplc = strat[0][personnage.y][personnage.x]
			if personnage.havesword and not(personnage.havetreasure) and not(personnage.havekey):
				dplc = strat[1][personnage.y][personnage.x]
			if not(personnage.havesword) and not(personnage.havetreasure) and personnage.havekey:
				dplc = strat[2][personnage.y][personnage.x]
			if personnage.havesword and not(personnage.havetreasure) and personnage.havekey:
				dplc = strat[3][personnage.y][personnage.x]
			if not(personnage.havesword) and personnage.havetreasure and personnage.havekey:
				dplc = strat[4][personnage.y][personnage.x]
			if personnage.havesword and personnage.havetreasure and personnage.havekey:
				dplc = strat[5][personnage.y][personnage.x]
			personnage.deplace(dplc, dg)
		affiche(fenetre, dg, personnage)
		pygame.display.flip()

		if mode > 1:
			time.sleep(0.3)

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
			text2 = font.render("Appuyer sur F1 pour revenir à la fenêtre d'accueil", 1, (250, 250, 250))
			text3 = font.render("Appuyer sur F2 pour sauvegarder la strategie sur le disque", 1, (250, 250, 250))
			fenetre.blit(text, (0, 50))
			fenetre.blit(text2, (0, 100))
			fenetre.blit(text3, (0, 150))
			pygame.display.flip()
			for event in pygame.event.get():
				print("new event")
				if event.type == QUIT:
					nouveau_essaie = 0
					print(nouveau_essaie)
					fini = 0
					continuer = 0
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						nouveau_essaie = 1
						print(nouveau_essaie)
						background = pygame.Surface(fenetre.get_size())
						background = background.convert()
						background.fill((0, 0, 0))
						fenetre.blit(background, (0, 0))
						dg = copy.deepcopy(dg_old)
						personnage = Perso(dg.matrix)
						affiche(fenetre, dg, personnage)
						pygame.display.flip()
						fini = 0
					if event.key == K_F1 :
						nouveau_essaie = 0
						fini = 0
						continuer = 1
						continuer_accueil_1 = 1
					if event.key == K_F2:
						fini = 0
						#print("AS")
						app = ["BASIC", "S", "K", "KS", "KT", "KTS"]
						affiche_strat(fenetre, dg, strat[0])
						#pygame.display.flip()
						etape = 0
						pygame.image.save(fenetre, "strategy_BASIC.jpeg")
						while etape < 5 :
							etape += 1

							affiche_strat(fenetre, dg, strat[etape])
							#pygame.display.flip()
							pygame.image.save(fenetre, "strategy_"+app[etape]+".jpeg")
							nouveau_essaie = 0
							print(nouveau_essaie)
							fini = 0
							continuer = 0
							affiche_strategy = 0



		if personnage.havetreasure and D_SHORTS["O"] == dg.matrix[personnage.y][personnage.x]:
			background = pygame.Surface(fenetre.get_size())
			background = background.convert()
			background.fill((0, 0, 0))
			fenetre.blit(background, (0, 0))
			font = pygame.font.Font(None, 36)
			text = font.render("Gagne", 1, (250, 250, 250))
			fenetre.blit(text, (0, 0))
			font = pygame.font.Font(None, 36)
			text = font.render("Appuyer sur espace pour nouvelle partie", 1, (250, 250, 250))
			text2 = font.render("Appuyer sur F1 pour revenir à la fenêtre d'accueil", 1, (250, 250, 250))
			text3 = font.render("Appuyer sur F2 pour sauvegarder la strategie sur le disque", 1, (250, 250, 250))
			fenetre.blit(text, (0, 50))
			fenetre.blit(text2, (0, 100))
			fenetre.blit(text3, (0, 150))
			pygame.display.flip()
			for event in pygame.event.get():
				print("new event")
				if event.type == QUIT:
					nouveau_essaie = 0
					print(nouveau_essaie)
					fini = 0
					continuer = 0
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						nouveau_essaie = 1
						print(nouveau_essaie)
						background = pygame.Surface(fenetre.get_size())
						background = background.convert()
						background.fill((0, 0, 0))
						fenetre.blit(background, (0, 0))
						dg = copy.deepcopy(dg_old)
						personnage = Perso(dg.matrix)
						affiche(fenetre, dg, personnage)
						pygame.display.flip()
						fini = 0
					if event.key == K_F1 :
						nouveau_essaie = 0
						fini = 0
						continuer = 1
						continuer_accueil_1 = 1
					if event.key == K_F2:
						fini = 0
						#print("AS")
						app = ["BASIC", "S", "K", "KS", "KT", "KTS"]
						affiche_strat(fenetre, dg, strat[0])
						#pygame.display.flip()
						etape = 0
						pygame.image.save(fenetre, "strategy_BASIC.jpeg")
						while etape < 5 :
							etape += 1

							affiche_strat(fenetre, dg, strat[etape])
							#pygame.display.flip()
							pygame.image.save(fenetre, "strategy_"+app[etape]+".jpeg")
							nouveau_essaie = 0
							print(nouveau_essaie)
							fini = 0
							continuer = 0
							affiche_strategy = 0



