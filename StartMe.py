import numpy as np 
from enum import Enum
from math import inf
import sys
import copy
import random

import time
""" *****************************************************************
								Constants
***************************************************************** """

DIM_MIN = 5
DIM_MAX = 15

GAME_ETAPES = ["BASIC", "S", "K", "KS", "KT", "KTS"]

#L_REWARDS = [[-1 for i in range(len(L_STATES[0]))] for j in range (len(L_STATES))]

D_SHORTS = {"O" : 0, "." :1, "E" : 2, "W" : 3, "R" : 4, "C" : 5, "S" : 6, "K" : 7, "P" : 8, "-" : 9, "T" : 10, "F" : 11}

NB_STATES = 12
NB_ETAPES = 7

M_REWARDS = np.full((NB_ETAPES, NB_STATES), -1)

R_W = 10000
R_L = -R_W/5#TODO : trouver le facteur d'une manière "automatique"
R_F = -10
R_IMPOSSIBLE = -10000

P_E = 0.7

class State(Enum):
	START = 0
	BLANK = 1
	ENEMY = 2
	WALL = 3
	TRAP = 4
	CRACKS = 5
	SWORD = 6
	KEY = 7
	PORTAIL = 8
	MOVING = 9
	TREASURE = 10
	FRIGO = 11

class Etape(Enum):
	BASIC = 0
	S = 1
	K = 2
	KS = 3
	KT = 4
	KTS = 5
	FINAL = 6


def init_rewards():
	for etape in range(NB_ETAPES):
		for state in range(NB_STATES):
			if state == State.START.value :
				if etape == Etape.KT.value or etape == Etape.KTS.value :
					M_REWARDS[etape][state] += R_W
			elif state == State.ENEMY.value :
				if etape == Etape.BASIC.value or etape == Etape.K.value or etape == Etape.KT.value :
					M_REWARDS[etape][state] += (1- P_E) * R_L
			#elif state == State.TRAP.value :
			#	if etape == Etape.KT.value or etape == Etape.KTS.value : 
			#		M_REWARDS[etape][state] += 0.1 * R_L + 0.3 * R_W
			#	else :
			#		M_REWARDS[etape][state] += 0.1 * R_L # Le reste dépend de l'état (distance vers le start)
			elif state == State.FRIGO.value :
				M_REWARDS[etape][state] += R_F
			elif state == State.WALL.value :
				M_REWARDS[etape][state] = R_IMPOSSIBLE
			elif state == State.TREASURE.value :
				if etape < Etape.K.value :
					M_REWARDS[etape][state] = R_IMPOSSIBLE
			
				#elif etape < Etape.KT.value :
				#	M_REWARDS[etape][state] += R_W
			#elif state == State.KEY.value :
				#if etape < Etape.K.value :
				#	M_REWARDS[etape][state] += R_W
			elif state == State.CRACKS.value :
				M_REWARDS[etape][state] = R_L 
	#for state in range(NB_STATES):
	#	M_REWARDS[-1][state] = 0



init_rewards()
#print(M_REWARDS)

class DungeonMatrix():
	def __init__(self, file_name):
		self.game_etape = "BASIC"
		self.enemies = []
	
		if type(file_name) == int :
			self.random_instance(file_name)
		else :
			self.read_instance(file_name)



	def random_instance(self, n):
		self.matrix = np.ones((n, n))


		#self.matrix[random.randrange(n)][random.randrange(n)] = D_SHORTS["O"]
		self.matrix[n-1][n-1] = D_SHORTS["O"]
		point = [random.randrange(n), random.randrange(n)]
		
		while self.matrix[point[0]][point[1]] != 1 :
			point = [random.randrange(n), random.randrange(n)]
		
		self.matrix[0][0] = D_SHORTS["T"]
		
		point = [random.randrange(n), random.randrange(n)]
		while self.matrix[point[0]][point[1]] != 1 :
			point = [random.randrange(n), random.randrange(n)]
		self.matrix[point[0]][point[1]] = D_SHORTS["K"]
		point = [random.randrange(n), random.randrange(n)]
		while self.matrix[point[0]][point[1]] != 1 :
			point = [random.randrange(n), random.randrange(n)]
		self.matrix[point[0]][point[1]] = D_SHORTS["S"]


		for i in range(n):
			for j in range(n):
				if self.matrix[i][j] == 1:
					p = random.random()
					if p < 0.2:
						p = random.random()
						if p < 0.2 : 
							self.matrix[i][j] = D_SHORTS["C"]
						else:
							self.matrix[i][j] = D_SHORTS["W"]
					else:
						p = random.random()
						if p < 0.15:
							self.matrix[i][j] = D_SHORTS["E"]
							self.enemies.append((i, j))
						elif p < 0.5 :
							l = [D_SHORTS["E"], D_SHORTS["R"], D_SHORTS["-"], D_SHORTS["P"], D_SHORTS["F"]]
							k = random.randrange(5) #!!!! 5
							self.matrix[i][j] = l[k]
							if D_SHORTS["E"] == l[k]:
								self.enemies.append((i, j))


		#print(self.matrix, self.enemies)

	def read_instance(self, file_name):
		#TODO : read from file
		file = open(file_name, "r")
		line = file.readline()
		line_split = line.split(":")
		self.nb_lines = int(line_split[-1].rstrip())

		line = file.readline()
		line_split = line.split(":")
		self.nb_columns = int(line_split[-1].rstrip())

		self.matrix = np.zeros((self.nb_lines, self.nb_columns))

		for i in range(self.nb_lines) :
			line = file.readline()
			line_split = line.split(" ")
			for j in range(self.nb_columns) :
				c = line_split[j].rstrip()
				self.matrix[i][j] = D_SHORTS[c]
				if c == "E" :
					self.enemies.append((i, j))

		file.close()
		print(self.matrix)

	def trouve_min(self, Q, d):
		mini = np.inf
		sommet = -1
		for s in Q:
			if d[s[0]][s[1]] < mini:
				mini = d[s[0]][s[1]]
				sommet = s
		if sommet == -1:
			return random.choice(Q)
		return sommet

	def maj_dist(self, s1, s2, d):
		if d[s2[0]][s2[1]] > d[s1[0]][s1[1]] + 1:
			d[s2[0]][s2[1]] = d[s1[0]][s1[1]] + 1


	def is_realisable(self):
		reponse = 0
		Q = []
		n = len(self.matrix)
		d = [[np.inf for i in range(n)] for j in range(n)]
		d[n - 1][n - 1] = 0
		for i in range(n):
			for j in range(n):
				if self.matrix[i][j] != D_SHORTS["W"] and self.matrix[i][j] != D_SHORTS["C"]:
					Q.append((i, j))
		while Q != []:
			s1 = self.trouve_min(Q, d)
			Q.remove(s1)
			if s1[0] > 0:
				s2 = (s1[0] - 1, s1[1])
				self.maj_dist(s1, s2, d)
			if s1[0] < (n - 1):
				s2 = (s1[0] + 1, s1[1])
				self.maj_dist(s1, s2, d)
			if s1[1] > 0:
				s2 = (s1[0], s1[1] - 1)
				self.maj_dist(s1, s2, d)
			if s1[1] < (n - 1):
				s2 = (s1[0], s1[1] + 1)
				self.maj_dist(s1, s2, d)
		for i in range(n):
			for j in range(n):
				if self.matrix[i][j] == D_SHORTS["K"]:
					reponse = (d[i][j] < np.inf)
		reponse = (reponse and (d[n - 1][n - 1] < np.inf))
		print(reponse)


#dg = DungeonMatrix(5)
#print(dg.matrix, dg.is_realisable())

""" *****************************************************************
						Basic Framework - Graphics
***************************************************************** """

#TODO Marion

""" *****************************************************************
								MDP Model	
***************************************************************** """

class Dir(Enum):
	NULL = [0,0]
	NORD = [-1,0]
	EST = [0,1]
	SOUTH = [1,0]
	WEST = [0,-1]
	

class MDP():
	def __init__(self, matrix):
		self.matrix = matrix
		self.states = []

		for etape in range(NB_ETAPES):
			l = []
			for line in range(len(self.matrix)):
				for column in range(len(self.matrix[0])):
					l += [(etape, line, column)]
			self.states += l

		self.values_old = [np.zeros((len(matrix), len(matrix[0]))) for i in range(NB_ETAPES)]
		self.values_new = [np.zeros((len(matrix), len(matrix[0]))) for i in range(NB_ETAPES)]
		self.dec = [np.full((len(matrix), len(matrix[0])), 0) for i in range(NB_ETAPES)]
		self.dec_old = [np.full((len(matrix), len(matrix[0])), 0) for i in range(NB_ETAPES)]

	def is_in_matrix(self, i, j):
		if i < 0 or j < 0 :
			return False
		elif i >= len(self.matrix) or j >= len(self.matrix[0]) :
			return False
		return True

	def is_accessible(self, i, j, etape):
		if self.matrix[i][j] == State.WALL.value :
			return False
		if self.matrix[i][j] == State.TREASURE.value and etape < Etape.K.value :
			return False
		return True

	def hasSword(self, etape):
		if etape == Etape.S.value or etape == Etape.KS.value or etape == Etape.KTS.value :
			return True
		else :
			return False

	def hasKey(self, etape):
		if etape > Etape.S.value :
			return True
		else :
			return False

	def hasTreasure(self,etape) :
		if etape == Etape.KT.value or etape == Etape.KTS.value :
			return True
		else :
			return False

	def get_neighborhood(self, etape, line, column, forbidden):
		res = []
		#print("f : ",forbidden)
		for a in Dir:
			#print((line+a.value[0], column+a.value[1], etape))

			if (a.value[0] != 0 or a.value[1] !=0)  and ((line+a.value[0], column+a.value[1]) not in forbidden) and self.is_in_matrix(line+a.value[0], column+a.value[1]) and self.is_accessible(line+a.value[0], column+a.value[1], etape) :
				#print("1")
				res+= [(line+a.value[0], column+a.value[1])]
		return res

	def state_evaluation(self, etape, line, column, state) :
		if state == State.BLANK.value : 
			rew = -1
			sum_vt = self.values_old[etape][line][column]
			return rew + sum_vt

		if state == State.FRIGO.value : 
			rew = -1 + R_F
			sum_vt = self.values_old[etape][line][column]
			return rew + sum_vt

		if state == State.ENEMY.value :
			if  self.hasSword(etape):
				rew = -1
				sum_vt = self.values_old[etape][line][column]
				return rew + sum_vt
			else :
				rew = - 1 + (1 - P_E)*R_L
				sum_vt = P_E * self.values_old[etape][line][column] + (1 - P_E)*self.values_old[Etape.FINAL.value][-1][-1]
				return rew + sum_vt

		if state == State.TRAP.value :
			#print("\t 1")
			if etape == Etape.KT.value or etape == Etape.KTS.value :
				#print("\t \t 2")
				rew = -1 + 0.1 * R_L + 0.3 * R_W
				sum_vt = 0.1 * self.values_old[Etape.FINAL.value][-1][-1] + 0.3 * self.values_old[Etape.FINAL.value][-1][-1] + 0.6 * self.values_old[etape][line][column]
				#print("\t \t ",rew, sum_vt)
				return rew + sum_vt
			#elif etape == Etape.Basic.value :
			#	rew = R_L
				#sum_vt =  0.1 * self.values_old[Etape.BASIC.value][-1][-1] + 0.3 * self.values_old[etape][-1][-1] + 0.6 * self.values_old[etape][line][column]
			else :
				rew = -1 + 0.1 * R_L - 0.3 * (len(self.matrix) - 1 - line + len(self.matrix[0]) - 1 -column) #TODO : seulement heuristique de la longueur du chemin !!! 
				#if etape == Etape.BASIC.value : 
					#print("rw : ",rew, line, column)
				sum_vt =  0.1 * self.values_old[Etape.FINAL.value][-1][-1] + 0.3 * self.values_old[etape][-1][-1] + 0.6 * self.values_old[etape][line][column]
				return rew + sum_vt

		if state == State.CRACKS.value : 
			rew = -1 + R_L
			sum_vt = self.values_old[Etape.FINAL.value][line][column]
			return rew + sum_vt

		if state == State.SWORD.value :
			rew = -1 
			new_etape = etape 
			
			if not self.hasSword(etape) :
				if etape == Etape.BASIC.value :
					new_etape = Etape.S.value
				elif etape == Etape.K.value :
					new_etape = Etape.KS.value
				elif etape == Etape.KT.value :
					new_etape = Etape.KTS.value
		
			sum_vt = self.values_old[new_etape][line][column]			
			return rew + sum_vt

		if state == State.KEY.value :
			rew = -1
			new_etape = etape
			if not self.hasKey(etape): 
				if etape == Etape.BASIC.value :
					new_etape = Etape.K.value
				elif etape == Etape.S.value :
					new_etape = Etape.KS.value

			sum_vt = self.values_old[new_etape][line][column]
			return rew + sum_vt

		if state == State.TREASURE.value : 
			rew = -1 
			new_etape = etape
			if etape == Etape.K.value :
					new_etape = Etape.KT.value
			elif etape == Etape.KS.value :
				new_etape = Etape.KTS.value
			sum_vt = self.values_old[new_etape][line][column]
			return rew + sum_vt

		if state == State.START.value :
			rew = -1 
			new_etape = etape
			if self.hasTreasure(etape):
				new_etape = Etape.FINAL.value
				rew = R_W
			sum_vt = self.values_old[new_etape][line][column]
			return rew + sum_vt

		if state == State.PORTAIL.value :
			nb_cells = 0
			v = 0
			for l in range(len(self.matrix)):
				for c in range(len(self.matrix[0])):
					#
					if self.matrix[l][c] != State.PORTAIL.value and self.matrix[l][c] != State.MOVING.value and self.is_accessible(l, c, etape):
						nb_cells += 1
						v += self.state_evaluation(etape,l,c,self.matrix[l][c])
						#v += self.values_old[etape][l][c]

			return -1 + v/nb_cells


		if state == State.MOVING.value :
			v = 0
			forbidden = []
			to_explore = []
			#print(etape, line, column)
			neighborhood = self.get_neighborhood(etape,line,column, forbidden)
			total = neighborhood
			i = 0

			#v += 1/len(neighborhood)*
			fac = 0
			#print("******** START **********\n")
			while len(neighborhood) > 0 :
				#print("n :", neighborhood)
				fac = 0
				for nei in neighborhood:
					if self.matrix[nei[0]][nei[1]] != State.MOVING.value :
						#print(len(neighborhood))
						#print(neighborhood)
						#print(self.matrix[nei[0]][nei[1]])
						#print(self.state_evaluation(etape,line,column, self.matrix[nei[0]][nei[1]]))
						v += self.state_evaluation(etape,line,column, self.matrix[nei[0]][nei[1]])
						fac += 1
						#v += self.values_old[etape][line][column]
					#	forbidden += [nei]
					#else :
					#	if self.matrix[nei[0]][nei[1]] == State.MOVING.value :
					#		to_explore += [nei]
				
				forbidden += [(line, column)]
				#print(forbidden)
				neighborhood = [] 
				#for e in to_explore :
				#	neighborhood += self.get_neighborhood(etape, line, column, forbidden)

				neighborhood = list(set(neighborhood))
				total += neighborhood
				i += 1
			
			#print(total)
			#print("************* END ************** \n")
			#print(v)
			if fac != 0 :
				return - 1 + v/fac 
			return -1 + v
			#return self.state_evaluation(etape, line, column, State.BLANK.value)
			

	def Q_as(self, s, a):

		#print("*** Q_as ***")
		#print("\t s = ", s, "a = ", a)
		if (not self.is_in_matrix(s[1] + a[0], s[2] + a[1])) :
			#print("\t \t not in matrix ! ")
			#print(self.matrix[s[1]][s[2]])
			#print(M_REWARDS[s[0]][int(self.matrix[s[1]][s[2]])])
			#print(s[0], s[1], s[2])
			#print(self.values)
			#print(self.values[s[0]][s[1]][s[2]])
			return R_IMPOSSIBLE + self.values_old[s[0]][s[1]][s[2]]
		elif (not self.is_accessible(s[1] + a[0], s[2] + a[1], s[0])) :
			return -1*(len(self.matrix) + len(self.matrix[0])  - s[1] - s[2]) + self.values_old[Etape.BASIC.value][len(self.matrix) - 1][len(self.matrix[0])-1]
			#return M_REWARDS[s[0]][int(self.matrix[s[1]][s[2]])] + self.values[s[0]][s[1]][s[2]]
		elif a == [0,0]:
			if s[0] == Etape.FINAL.value :
				return 0
			else :
				return self.state_evaluation(s[0], s[1], s[2], self.matrix[s[1]][s[2]])
		else :
			# A revoir ! Passage entre les etapes
			new_line = s[1] + a[0]
			new_column = s[2] + a[1]
			#print("lc :", new_line, new_column)
			new_etape = s[0]
			
			return self.state_evaluation(new_etape, new_line, new_column, self.matrix[new_line][new_column])

			


	def calcul_error_value(self) :
		er = 0

		for etape in range(NB_ETAPES):
			for i in range(len(self.matrix)):
				for j in range(len(self.matrix[0])):
					d = self.values_old[etape][i][j] - self.values_new[etape][i][j]
					#print("\t ",d)
					if abs(d) > er :
						#print("eij :",etape, i, j)
						#print(self.values_old[etape][i][j])
						#print(self.values_new[etape][i][j])
						er = abs(d)
		return er

	def calcul_error_d(self):
		er = 0

		for etape in range(NB_ETAPES):
			for i in range(len(self.matrix)):
				for j in range(len(self.matrix[0])):
					d = self.dec[etape][i][j] - self.dec_old[etape][i][j]
					er += abs(d)
		#print("er policy it : ",er)
		return er

	def value_iteration(self, epsilon):
		
		er = epsilon+1
		nb_it = 0
		while er > epsilon and nb_it < 1000 :
			#print("*** NEW ITERATION *** \n")
			#print(self.values_old)
			for s in self.states:
				#print("state : ", s)
				#print("matrix :",self.matrix[s[1]][s[2]])
				
				Q = []
				#if self.matrix [s[1]][s[2]] == State.WALL.value :
				#	Q = [R_IMPOSSIBLE]
				#elif s[0] == Etape.BASIC.value and self.matrix [s[1]][s[2]] == State.TREASURE.value :
				#	Q = [R_IMPOSSIBLE]
				#else :
				for a in Dir :
					#print(a)
					#if a.value != [0,0] or s[0] == NB_ETAPES - 1 :
					Q += [self.Q_as(s, a.value)]
			
				#print("\t ",Q)
				self.values_new[s[0]][s[1]][s[2]] = np.asarray(Q).max()
				self.dec[s[0]][s[1]][s[2]] = np.asarray(Q).argmax()
			#print(self.values_old)
			#print(self.values_new)
			#print(self.dec)
			#er = er - 0.01
			er = self.calcul_error_value()
			#print(self.calcul_error_value())
			self.values_old = copy.deepcopy(self.values_new)
			nb_it += 1

			if nb_it % 100 == 0 :
				print(nb_it)
				print(er)


		#print("**************** VALUES ************************* \n")
		#print(self.values_old)
		#print(self.values_new)
		#print(self.dec)
		#print("*************************************************** \n")
		#print("nb_it = ", nb_it)

		#return nb_it
		return self.dec

	def policy_iteration(self):
		er = 1
		nb_it = 0
		while er != 0 and nb_it < 1000:
			for s in self.states :
				#print(etape, line, column)
				#print(self.states[etape][line][column], self.dec_old[etape][line][column])
				dt = []
				if self.dec_old[s[0]][s[1]][s[2]] == 0 :
					dt = Dir.NULL.value
				elif self.dec_old[s[0]][s[1]][s[2]] == 1 :
					dt = Dir.NORD.value
				elif self.dec_old[s[0]][s[1]][s[2]] == 2 :
					dt = Dir.EST.value
				elif self.dec_old[s[0]][s[1]][s[2]] == 3 :
					dt = Dir.SOUTH.value
				elif self.dec_old[s[0]][s[1]][s[2]] == 4 :
					dt = Dir.WEST.value

				self.values_old[s[0]][s[1]][s[2]] = self.Q_as(s, dt)
				Q = []
				for a in Dir :
					Q += [self.Q_as(s, a.value)]
					self.dec[s[0]][s[1]][s[2]] = np.asarray(Q).argmax()

			er = self.calcul_error_d()
			self.dec_old = copy.deepcopy(self.dec)
			nb_it += 1

			if nb_it % 100 == 0 :
				print(nb_it)
				print(er)

		#print(self.values_old)
		#print(self.values_new)
		#print(self.dec)
		#print("nb_it :", nb_it)
		#return nb_it
		return self.dec
#dg = DungeonMatrix("instance_subject.txt")

#mdp = MDP(dg.matrix)
#m_decision = mdp.value_iteration(0.01)
#m_decision = mdp.policy_iteration()
""" *****************************************************************
						Reinforcement learning
***************************************************************** """


class QLearning():
	def __init__(self, matrix):
		self.matrix = matrix
		self.states = []

		for etape in range(NB_ETAPES):
			l = []
			for line in range(len(self.matrix)):
				for column in range(len(self.matrix[0])):
					l += [(etape, line, column)]
			self.states += l

		self.values_old = [np.zeros((len(matrix), len(matrix[0]),5)) for i in range(NB_ETAPES)]
		#self.values_new = [np.zeros((len(matrix), len(matrix[0]))) for i in range(NB_ETAPES)]
		self.dec = [np.full((len(matrix), len(matrix[0])), 0) for i in range(NB_ETAPES)]
		#self.dec_old = [np.full((len(matrix), len(matrix[0])), 0) for i in range(NB_ETAPES)]

	def is_in_matrix(self, i, j):
		#print("\t in : ", i,j)
		if i < 0 or j < 0 :
			#print("\t \t not in\n")
			return False
		elif i >= len(self.matrix) or j >= len(self.matrix[0]) :
			#print("\t \t not in\n")
			return False
		#print("\t \t in\n")
		return True

	def is_accessible(self, i, j, etape):
		#print("\t acc :", i,j,etape)
		if self.matrix[i][j] == State.WALL.value :
			#print("\t \t not acc\n")
			return False
		if self.matrix[i][j] == State.TREASURE.value and etape < Etape.K.value :
			#print("\t \t not acc\n")
			return False
		#print("\t \t acc\n")
		return True

	def hasSword(self, etape):
		if etape == Etape.S.value or etape == Etape.KS.value or etape == Etape.KTS.value :
			return True
		else :
			return False

	def hasKey(self, etape):
		if etape > Etape.S.value :
			return True
		else :
			return False

	def hasTreasure(self,etape) :
		if etape == Etape.KT.value or etape == Etape.KTS.value :
			return True
		else :
			return False

	def get_neighborhood(self, etape, line, column, forbidden):
		res = []
		#print("f : ",forbidden)
		for a in Dir:
			#print((line+a.value[0], column+a.value[1], etape))

			if (a.value[0] != 0 or a.value[1] !=0)  and ((line+a.value[0], column+a.value[1]) not in forbidden) and self.is_in_matrix(line+a.value[0], column+a.value[1]) and self.is_accessible(line+a.value[0], column+a.value[1], etape) :
				#print("1")
				res+= [(line+a.value[0], column+a.value[1])]
		return res

	def get_r_sp(self, etape, line, column, state) :
		#print("\t",etape, line, column, state)
		if state == State.BLANK.value :
			return (-1,(etape,line,column))

		if state == State.FRIGO.value :
			return (-1 + R_F,(etape,line,column))


		if state == State.ENEMY.value : 
			if self.hasSword(etape):
				return (-1,(etape, line, column))
			else :
				p = random.random()
				if p <= P_E :
					return(-1, (etape, line, column))
				else :
					return (-1 + R_L, (Etape.BASIC.value, len(self.matrix) -1, len(self.matrix[0]) - 1))

				
		if state == State.TRAP.value :
			if self.hasTreasure(etape) :
				p = random.random()
				if p <= 0.1 :
					return (-1 + R_L, (Etape.BASIC.value, len(self.matrix) -1, len(self.matrix[0]) - 1))
				elif p <= 0.1 + 0.3 :
					return (-1 + R_W, (Etape.FINAL.value, len(self.matrix) -1, len(self.matrix[0]) -1))
				else :
					return (-1, (etape, line, column)) 
			
			else :
				p = random.random()
				if p <= 0.1 :
					return (-1 + R_L, (Etape.BASIC.value, len(self.matrix) -1, len(self.matrix[0]) - 1))
				elif p <= 0.1 + 0.3 :
					return (-1 - (len(self.matrix) - 1 - line + len(self.matrix[0]) - 1 -column), (etape, len(self.matrix) -1, len(self.matrix[0]) -1))
				else :
					return (-1, (etape, line, column)) 

		if state == State.CRACKS.value :
			return (-1 + R_L, (Etape.BASIC.value, len(self.matrix) -1 , len(self.matrix[0]) - 1))	

		if state == State.SWORD.value :
			new_etape = etape 
			
			if not self.hasSword(etape) :
				if etape == Etape.BASIC.value :
					new_etape = Etape.S.value
				elif etape == Etape.K.value :
					new_etape = Etape.KS.value
				elif etape == Etape.KT.value :
					new_etape = Etape.KTS.value
			return (-1, (new_etape, line, column))

		if state == State.KEY.value :
			new_etape = etape
			if not self.hasKey(etape): 
				if etape == Etape.BASIC.value :
					new_etape = Etape.K.value
				elif etape == Etape.S.value :
					new_etape = Etape.KS.value

			return (-1, (new_etape, line, column))

		if state == State.TREASURE.value :
			new_etape = etape
			if etape == Etape.K.value :
					new_etape = Etape.KT.value
			elif etape == Etape.KS.value :
				new_etape = Etape.KTS.value

			return (-1, (new_etape, line, column))

		if state == State.START.value :
			new_etape = etape
			if self.hasTreasure(etape):
				new_etape = Etape.FINAL.value

			return (-1, (new_etape, line, column))	

		if state == State.MOVING.value :

			sp = state
			l = line
			c = column 

			l_nei = []
			for a in Dir:		
				if self.is_in_matrix(l + a.value[0], c + a.value[1]) and self.is_accessible(l + a.value[0], c + a.value[1], etape):
					l_nei += [[l + a.value[0], c + a.value[1]]]
			index = random.randrange(0, len(l_nei))
			new_state = l_nei[index]
			l = new_state[0]
			c = new_state[1]
			sp = self.matrix[l][c]

			return self.get_r_sp(etape, l, c, sp)
		
		if state == State.PORTAIL.value :
			sp = state
			l = line
			c = column

			l_nei = []
			for il in range(len(self.matrix)):
				for ic in range(len(self.matrix[0])):
					if self.is_accessible(il, ic, etape):
						l_nei += [[il, ic]]
			index = random.randrange(0, len(l_nei))
			#print(l_nei)
			return self.get_r_sp(etape, l_nei[index][0], l_nei[index][1], self.matrix[l_nei[index][0]][l_nei[index][1]])
		
	def index_to_dir(self, index) :
		if index == 0 :
			return Dir.NULL.value
		if index == 1 :
			return Dir.NORD.value
		if index == 2 :
			return Dir.EST.value
		if index == 3 :
			return Dir.SOUTH.value
		if index == 4 :
			return Dir.WEST.value

	def q_learning(self):

		for etape in range(NB_ETAPES -1 ):
			for line in range(len(self.matrix)):
				for column in range(len(self.matrix[0])):
					for a in range(5):
						dir = self.index_to_dir(a)
						#print("state elca: ", etape, line, column, dir)
						if not self.is_in_matrix(line + dir[0], column + dir[1]) or not self.is_accessible(line + dir[0], column + dir[1], etape):
							self.values_old[etape][line][column][a] = R_IMPOSSIBLE
						elif dir == [0,0] :
							self.values_old[etape][line][column][a] = R_IMPOSSIBLE

		#print(self.values_old)
		#return
		nb_periods = 10
		cpt = 0
		#print(self.values_old)
		while cpt < nb_periods :
			cpt += 1
			state = (Etape.BASIC.value, len(self.matrix) -1, len(self.matrix[0]) -1)
			cpt2 = 0
			#print("final state :")
			while state != (Etape.FINAL.value, len(self.matrix) -1, len(self.matrix[0])-1) and cpt2 < 1000000 :
				#print("final state :", (Etape.FINAL.value, len(self.matrix) -1, len(self.matrix[0])-1))
				#print("act state :", state)
				cpt2 += 1

				#print("state : ",state)
				a_best = 0
				same = [a_best]
				for a in range(5):
					#print(self.values_old[state[0]][state[1]][state[2]][a])
					if self.values_old[state[0]][state[1]][state[2]][a] > self.values_old[state[0]][state[1]][state[2]][a_best]:
						a_best = a
						same = [a_best]
					elif self.values_old[state[0]][state[1]][state[2]][a] == self.values_old[state[0]][state[1]][state[2]][a_best]:
						same += [a]

				ind = random.randrange(0, len(same))
				a_best = same[ind]
				#print(a_best)
					#print("\t ",self.values_old[state[0]][state[1]][state[2]][a])
				"""
				for a in Dir :
					#print(a)
					if a.value == [0,0] and state[0] != Etape.FINAL.value :
						l_a += [R_IMPOSSIBLE]
					elif self.is_in_matrix(state[1] + a.value[0], state[2] + a.value[1]):
						l_a += [self.values_old[state[0]][state[1]][state[2]]]
					else :
						l_a += [R_IMPOSSIBLE]
				"""
				#a_best = np.asarray(l_a).max()
				#print("\t a_best : ", a_best)
				#print("\t : ",self.dec[state[0]][state[1]][state[2]])
				#print("\t : ",self.dec[state[0]][state[1]][state[2]])
				self.dec[state[0]][state[1]][state[2]] =  a_best
				a_dir = [0,0]
				#print("\t : ",self.dec[state[0]][state[1]][state[2]])
				if a_best == 0 :
					a_dir = Dir.NULL.value
				if a_best == 1 :
					a_dir = Dir.NORD.value
				if a_best == 2 :
					a_dir = Dir.EST.value
				if a_best == 3 :
					a_dir = Dir.SOUTH.value
				if a_best == 4 :
					a_dir = Dir.WEST.value

				if self.is_in_matrix(state[1] + a_dir[0], state[2] + a_dir[1]) and self.is_accessible(state[1] + a_dir[0], state[2] + a_dir[1], state[0]): 
					r_sp = self.get_r_sp(state[0], state[1] + a_dir[0], state[2] + a_dir[1], self.matrix[state[1]+ a_dir[0]][state[2] + a_dir[1]])
					#print("r_sp : ",r_sp)
					r = r_sp[0]
					sp = r_sp[1]
				
					ap_best = 0
					for a in range(5):
						if self.values_old[state[0]][state[1]][state[2]][a] >= self.values_old[state[0]][state[1]][state[2]][ap_best]:
							ap_best = a
							#print("\t ",self.values_old[state[0]][state[1]][state[2]][a])

				
					self.values_old[state[0]][state[1]][state[2]][a_best] = self.values_old[state[0]][state[1]][state[2]][a_best] + 1/(cpt+1)*(r + self.values_old[sp[0]][sp[1]][sp[2]][ap_best] - self.values_old[state[0]][state[1]][state[2]][a_best])
					state = sp
					#print(self.values_old)
				else : 
					self.values_old[state[0]][state[1]][state[2]][a_best] = self.values_old[state[0]][state[1]][state[2]][a_best] + 1/(cpt+1)*(R_IMPOSSIBLE) 
				
				if cpt2 % 100000 == 0:
					print("\t ", cpt2)
			print("nb_it : ", cpt2)
		#print(self.dec)
		return self.dec
		#return cpt2
		#print(self.dec)
				#print(sp)
		#print(self.values_old[1])


#random.random()

#QL = QLearning(dg.matrix)
#QL.q_learning()
"""
f = open("tests_vi.txt", "w")
f.write("--------------- VALUE ITER ---------------------------------- \n" )

for i in range(5,15):
	f = open("tests_vi.txt", "a")
	f.write("taille : "+str(i)+"\n")
	for j in range(20):
		start = time. time()
		dg = DungeonMatrix(i)
		print(dg.matrix)
		m = MDP(dg.matrix)
		f.write(str(m.value_iteration(1)))
		f.write("\n")
		end = time. time()
		f.write(str(end - start)+"\n")
	f.close()

f.write("--------------- POLICY ITER ---------------------------------- \n" )


f = open("tests_pi.txt", "w")
for i in range(5,15):
	f = open("tests_pi.txt", "a")
	f.write("taille : "+str(i)+"\n")
	for j in range(100):
		start = time. time()
		dg = DungeonMatrix(i)
		print(dg.matrix)
		m = MDP(dg.matrix)
		f.write(str(m.policy_iteration()))
		f.write("\n")
		end = time. time()
		f.write(str(end - start)+"\n")
	f.close()	


f = open("tests_ql.txt", "w")

f.write("--------------- QL ---------------------------------- \n" )

for i in range(5,15):
	f = open("tests_ql.txt", "a")
	f.write("taille : "+str(i)+"\n")
	for j in range(10):
		start = time. time()
		dg = DungeonMatrix(i)
		print(dg.matrix)
		m = QLearning(dg.matrix)
		f.write(str(m.q_learning()))
		f.write("\n")
		end = time. time()
		f.write(str(end - start)+"\n")
	f.close()
"""
""" *****************************************************************
								Bonus
***************************************************************** """