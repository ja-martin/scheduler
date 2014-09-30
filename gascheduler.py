from random import choice

class GaScheduler(object):
	'''
	Solves the scheduling problem using a genetic algorithm.
	'''

	workers = None
	shifts = None # Date ordered.
	dates = None # Store the start and end indexes of the shifts list for each different date.
	generations = None
	population_length = None


	def __init__(self, workers, shifts, generations=10, population_length=15):
		self.workers = workers

		self.shifts = shifts
		self.shifts.sort(key=lambda s: s.date)

		self.dates = self._calculate_dates()

		self.generations = generations
		self.population_length = population_length

		self.generate()



	def generate(self):
		'''
		'''
		population = list()

		while len(population) != 15:
			matrix = self._random_assignment()
			print(len(population))
			if self._is_valid(matrix):
				population.append((matrix, self._days_off_fitness(matrix)))

		for matrix, fitness in population:
			for row in matrix:
				for cell in row: print cell,
				print
			print("Fitness: ", fitness)


	def _calculate_dates(self):
		dates = list()
		# Traverse the shifts list to get the column ranges for the different dates.
		# TODO: check itertools.groupby
		last_date = self.shifts[0].date
		start = 0
		for i, s in enumerate(self.shifts):
			if s.date != last_date:
				dates.append({"start": start, "end": i})
				start = i
				last_date = s.date
		dates.append({"start": start, "end": len(self.shifts)})

		return dates


	def _fitness(self, matrix):
		# max days off in a row per worker, 
		pass


	def _days_off_fitness(self, matrix):
		'''
		Calculates a fitness score for a given assignment matrix based on the quality of its days off sequences.
		Per each worker: score = max. consecutive days off / no. days off. The returned value is the average score of all workers.
		'''
		worker_score = [0] * len(matrix)

		for i, w in enumerate(matrix):
			no_days_off = w.count(0)

			if no_days_off == 0:
				worker_score[i] = 1
				continue

			last = 1 
			longest = start = end = 0
			for j, s in enumerate(w):
				if s == 0:
					if last == 0:
						end += 1
					elif last == 1:
						start, end = j, j+1
						last = 0
					if j == len(w)-1: # Last day is day off
						if end-start > longest: longest = end-start
				elif s == 1:
					if last == 0:
						if end-start > longest: longest = end-start
						last = 1
					elif last == 1:
						pass

			worker_score[i] = float(longest) / no_days_off

		return sum(worker_score) / len(worker_score)



	def _preference_fitness(self, matrix):
		pass


	def _random_assignment(self):
		matrix = self._empty_matrix()

		for date in self.dates:
			# Generate different assignment options. Example: day with 3 shifts --> [[1,0,0], [0,1,0], [0,0,1]]
			# In this way we meet two hard constraints:  
			start, end = date["start"], date["end"]
			n = end-start
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
		for i, w in enumerate(matrix):
			worker = self.workers[i]
			shifts_lst = [self.shifts[j] for j, s in enumerate(w) if s == 1]

			if not worker.can_cover(shifts_lst=shifts_lst):
				return False

		return True


	def _empty_matrix(self):
		''' 
		Generates a blank assignments matrix: (no. of workers) * (no. of shifts)
		'''
		return [[0 for s in self.shifts] for w in self.workers]

	def _print_matrix(self, matrix):
		for row in matrix:
			for cell in row: print cell,
			print
		
