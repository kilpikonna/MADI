import numpy as np 
from enum import Enum
from math import inf
import sys
import copy

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
R_L = -R_W
R_F = -5 
R_IMPOSSIBLE = -1000000

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
			elif state == State.TRAP.value :
				if etape == Etape.KT.value or etape == Etape.KTS.value : 
					M_REWARDS[etape][state] += 0.1 * R_L + 0.3 * R_W
				else :
					M_REWARDS[etape][state] += 0.1 * R_L # Le reste dépend de l'état (distance vers le start)
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
			#	if etape < Etape.K.value :
			#		M_REWARDS[etape][state] += R_W
			elif state == State.CRACKS.value :
				M_REWARDS[etape][state] = R_L 





init_rewards()
print(M_REWARDS)

class DungeonMatrix():
	def __init__(self, file_name = "empty"):
		self.game_etape = "BASIC"
	
		if file_name == "empty" :
			self.random_instance()
		else :
			self.read_instance(file_name)

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
				self.matrix[i][j] = D_SHORTS[line_split[j].rstrip()]

		file.close()
		print(self.matrix)


dg = DungeonMatrix("instance_test.txt")

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
		self.dec = [np.full((len(matrix), len(matrix[0])), -1) for i in range(NB_ETAPES)]

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

	def Q_as(self, s, a):
		if a == [0,0]:
			return 0
		#print("*** Q_as ***")
		#print("\t s = ", s, "a = ", a)
		if (not self.is_in_matrix(s[1] + a[0], s[2] + a[1])) or (not self.is_accessible(s[1] + a[0], s[2] + a[1], s[0])) :
			#print("\t \t not in matrix ! ")
			#print(self.matrix[s[1]][s[2]])
			#print(M_REWARDS[s[0]][int(self.matrix[s[1]][s[2]])])
			#print(s[0], s[1], s[2])
			#print(self.values)
			#print(self.values[s[0]][s[1]][s[2]])
			return R_IMPOSSIBLE + self.values_old[s[0]][s[1]][s[2]]
			#return M_REWARDS[s[0]][int(self.matrix[s[1]][s[2]])] + self.values[s[0]][s[1]][s[2]]
		else :
			# A revoir ! Passage entre les etapes
			new_line = s[1] + a[0]
			new_column = s[2] + a[1]
			#print("lc :", new_line, new_column)
			new_etape = s[0]

			if self.matrix[new_line][new_column] == State.SWORD.value :
				if s[0] == Etape.BASIC.value :
					new_etape = Etape.S.value
				elif s[0] == Etape.K.value :
					new_etape = Etape.KS.value
				elif s[0] == Etape.KT.value :
					new_etape = Etape.KTS.value

			elif self.matrix[new_line][new_column] == State.KEY.value :
				if s[0] == Etape.BASIC.value :
					new_etape = Etape.K.value
				elif s[0] == Etape.S.value :
					new_etape = Etape.KS.value
			
			elif self.matrix[new_line][new_column] == State.TREASURE.value :
				if s[0] == Etape.K.value :
					new_etape = Etape.KT.value
				elif s[0] == Etape.KS.value :
					new_etape = Etape.KTS.value

			elif self.matrix[new_line][new_column] == State.START.value:
				if s[0] == Etape.KT.value :
					new_etape = Etape.FINAL.value
				elif s[0] == Etape.KTS.value :
					new_etape = Etape.FINAL.value

			return M_REWARDS[s[0]][int(self.matrix[new_line][new_column])] + self.values_old[new_etape][new_line][new_column]

	def calcul_error(self) :
		er = 0

		for etape in range(NB_ETAPES):
			for i in range(len(self.matrix)):
				for j in range(len(self.matrix[0])):
					d = self.values_old[etape][i][j] - self.values_new[etape][i][j]
					#print("\t ",d)
					if abs(d) > er :
						print("eij :",etape, i, j)
						print(self.values_old[etape][i][j])
						print(self.values_new[etape][i][j])
						er = abs(d)
		return er


	def value_iteration(self, epsilon):
		
		er = epsilon+1

		while er > epsilon :
			print("*** NEW ITERATION *** \n")
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
					Q += [self.Q_as(s, a.value)]
			
				#print(Q)
				self.values_new[s[0]][s[1]][s[2]] = np.asarray(Q).max()
				self.dec[s[0]][s[1]][s[2]] = np.asarray(Q).argmax()
			#print(self.values_old)
			#print(self.values_new)
			er = er - 0.01
			print(self.calcul_error())
			self.values_old = copy.deepcopy(self.values_new)

		print("**************** VALUES ************************* \n")
		print(self.values_old)
		print(self.values_new)
		print(self.dec)
		print("*************************************************** \n")

mdp = MDP(dg.matrix)
mdp.value_iteration(1)
""" *****************************************************************
						Reinforcement learning
***************************************************************** """

""" *****************************************************************
								Bonus
***************************************************************** """