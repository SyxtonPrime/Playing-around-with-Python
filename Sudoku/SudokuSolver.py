import numpy as np
import copy
from collections import Counter

class Sudoku:

	def __init__(self, puzzle, poss, acc):

	# Both of these should by numpy arrays.
	# Puzzle should be a 9 by 9 grid of integers 0 - 9
	# where 0 corresponds to unknown and Poss should 
	# contain lists of possibilities.
		self.puzzle = puzzle
		self.poss 	= poss
		self.acc 	= acc

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return np.array_equal(self.puzzle, other.puzzle) and self.poss == other.poss
		else:
			return False

	def row(self, i):
		return self.puzzle[i]

	def column(self, i):
		return self.puzzle[:,i]

	def box(self, i, j):
		return self.puzzle[i:i+3,j:j+3]

# Taks list of 81 characters and produce a sudoku puzzle
# in the Sudoku class.
def CreateSudoku(lst):
	acc 	= lst.count('.')
	grid	= [lst[9*i:9*i+9].replace('.', '0') for i in range(9)]
	puzzle  = np.zeros((9, 9), dtype = int)
	poss 	= [[0 for _ in range(9)] for _ in range(9)]
	for i in range(0, 9):
		for j in range(0, 9):
			num = int(grid[i][j])
			if num == 0:
				puzzle[i, j] = 0
				poss[i][j] = [k for k in range(1, 10)]
			else:
				puzzle[i, j] = num
				poss[i][j] = [num]

	return Sudoku(puzzle = puzzle, poss = poss, acc = acc)

def easysudoku():
	return '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def hardsudoku():
	return '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

def EliminatePossibilities(sudoku):
	for i in range(9):
		for j in range(9):
			possibilities = sudoku.poss[i][j]
			if len(possibilities) != 1:
				solved = False
				newposs = []
				for k in possibilities:
					if 	(k not in sudoku.row(i)) and (k not in sudoku.column(j)) and (k not in sudoku.box(i - i%3, j - j%3)):
						newposs.append(k)
				if len(newposs) == 1:
					sudoku.puzzle[i, j] = newposs[0]
					sudoku.acc -= 1
				elif len(newposs) == 0:
					return False
				sudoku.poss[i][j] = newposs
	return True

def lstCheck(lst):
	unplacedVals = [i for i in range(1, 10) if [i] not in lst]
	occurances = Counter([item for sublist in lst for item in sublist])
	return [i for i in unplacedVals if occurances[i] == 1]

def ForcedPlacements(sudoku):
	for i in range(9):
		row = sudoku.poss[i]
		valuesToBePlaced = lstCheck(row)
		for val in valuesToBePlaced:
			for j in range(9):
				if val in row[j]:
					sudoku.puzzle[i, j] = val
					sudoku.poss[i][j] = [val]
					sudoku.acc 	-= 1

		column = [j[i] for j in sudoku.poss]
		valuesToBePlaced = lstCheck(column)
		for val in valuesToBePlaced:
			for j in range(9):
				if val in column[j]:
					sudoku.puzzle[j, i] = val
					sudoku.poss[j][i] = [val]
					sudoku.acc 	-= 1

		box = [x for z in [y[3*(i%3): 3*(i%3) + 3] for y in sudoku.poss[i - i%3: i - i%3 + 3]] for x in z]
		valuesToBePlaced = lstCheck(box)
		for val in valuesToBePlaced:
			for j in range(3):
				for k in range(3):
					if val in box[3*j + k]:
						sudoku.puzzle[i - i%3 + j, 3*(i%3) + k] = val
						sudoku.poss[i - i%3 + j][3*(i%3) + k] = [val]
						sudoku.acc 	-= 1


def	Solve(sudoku):
	while sudoku.acc != 0:
		oldacc = sudoku.acc
		if EliminatePossibilities(sudoku):
			ForcedPlacements(sudoku)
		else:
			return False

		if oldacc == sudoku.acc:
			lengthArray = np.array([[len(x) if len(x) > 1 else 10 for x in row] for row in sudoku.poss])
			fewestOptions = lengthArray.min()
			guessPosition = np.where(lengthArray == fewestOptions)

			trial = copy.deepcopy(sudoku)
			options = sudoku.poss[guessPosition[0][0]][guessPosition[1][0]]

			for option in options:
				trial.poss[guessPosition[0][0]][guessPosition[1][0]] = [option]
				trial.puzzle[guessPosition[0][0]][guessPosition[1][0]] = option
				trial.acc -= 1
				attempt = Solve(trial)
				if attempt:
					return attempt
				else:
					trial = copy.deepcopy(sudoku)
			return False

	return sudoku

def IsValidSolution(sudoku):
	for i in range(9):
		row = sudoku.row(i)
		for j in range(1, 10):
			if j not in row:
				print('Row ', i, ' failed due to ', k)
				return False
		
		column = sudoku.column(i)
		for j in range(1, 10):
			if j not in column:
				print('Column ', i, ' failed due to ', k)
				return False

	for i in range(3):
		for j in range(3):
			box = sudoku.box(3*i, 3*j)
			for k in range(1, 10):
				if k not in box:
					print('Box ', i, ' ', j, ' failed due to ', k)
					return False
	return True