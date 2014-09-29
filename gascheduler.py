from random import choice

class GaScheduler(object):
	'''
	Solves the scheduling problem using a genetic algorithm.
	'''

	workers = None
	shifts = None # Date ordered.
	dates = None # Store the start and end indexes of the shifts list for each different date.

	def __init__(self, workers, shifts):
		self.workers = workers

		self.shifts = shifts
		self.shifts.sort(key=lambda s: s.date)

		self.dates = list()
		# Traverse the shifts list to get the column ranges for the different dates.
		current = self.shifts[0].date
		start = 0
		for i, s in enumerate(self.shifts):
			if s != current:
				self.dates.append({"start": start, "end": i})
				start = i
				current = s.date
		self.dates.append({"start": start, "end": len(self.shifts)})

		self.generate()



	def generate(self):
		'''
		'''
		population = list()

		while len(population) != 15:
			matrix = self._random_assignment()
			if self._is_valid(matrix):
				population.append(matrix)

		for matrix in population:
			for row in matrix:
				for cell in row: print cell,
				print
			print


	def _fitness(self, matrix):
		pass


	def _random_assignment(self):
		matrix = self._empty_matrix()

		for date in self.dates:
			# Generate different assignment options. Example: day with 3 shifts --> [[1,0,0], [0,1,0], [0,0,1]]
			# In this way we meet two hard constraints:  
			start, end = date["start"], date["end"]
			n = end - start
			options = [[1 if j == i else 0 for j in range(n)] for i in range(n)]

			w_index = range(len(self.workers))

			while options:
				w = choice(w_index)
				w_index.remove(w)
				matrix[w][start:end] = options.pop()

		return matrix


	def _is_valid(self, matrix):
		'''
		Check if a 
		'''
		for i in range(len(matrix)):
			worker = self.workers[i]
			shifts_lst = [self.shifts[j] for j in range(len(matrix[i])) if matrix[i][j] == 1]

			if not worker.can_cover(shifts_lst=shifts_lst):
				return False

		return True


	def _empty_matrix(self):
		''' 
		Generates a blank assignments matrix: (no. of workers) * (no. of shifts)
		'''
		return [[0 for s in self.shifts] for w in self.workers]
		
