from random import choice


class Solution(object):
	'''
	Represents a feasible assignment matrix and its fitness value.
	'''

	matrix = None
	fitness = None

	def __init__(self, matrix, fitness):
		self.matrix = matrix
		self.fitness = fitness


class GeneticScheduler(object):
	'''
	Solves scheduling problem using a genetic algorithm.
	'''

	workers = None
	shifts = None
	dates = None # Stores the start and end indexes of the shifts list for each different date.
	generations = None
	population_length = None
	solution = None
	crossovers = 0
	crossovers_valid = 0
	crossovers_not_valid = 0


	def __init__(self, workers, shifts, generations=50, population_length=16):
		'''
		Constructor
		'''
		self.workers = workers

		self.shifts = shifts
		self.shifts.sort(key=lambda s: s.date)

		self.dates = self._calculate_dates()

		self.generations = generations
		self.population_length = population_length


	def generate(self):
		'''
		Creates an initial population of valid matrixes and produces a number of descendant generations
		mixing individual solutions, keeping in the proccess those with best fitness value. Finally,
		selects best solution.
		'''
		# Randomly creates an initial population of valid assignments.
		population = list()
		while len(population) != self.population_length:
			matrix = self._random_assignment()
			if self._is_valid(matrix):
				population.append(Solution(matrix, self._fitness(matrix))) 

		# Produces new generations of children, keeping for the next generation the solutions with best fitness value. 
		for gen in range(self.generations):
			children = self._generate_children(population)
			population = sorted((population + children), reverse=True, key=lambda sol: sol.fitness)[:self.population_length]

		self.solution = max(population, key=lambda sol: sol.fitness)

		self._print_solution()
		print("Fitness value: ", self.solution.fitness)


	def _generate_children(self, population):
		'''
		Generates valid children from the current population, randomly selecting parents
		and applying crossover over them until we obtain a number of valid children equal
		to half the population.
		'''
		children = list()
		while len(children) < self.population_length/2:
			parents = [choice(population) for _ in range(4)]
			parents.sort(reverse=True, key=lambda sol: sol.fitness)

			child_matrix = self._crossover(*[sol.matrix for sol in parents[:2]])

			if self._is_valid(child_matrix):
				children.append(Solution(child_matrix, self._fitness(child_matrix)))

		return children


	def _crossover(self, m1, m2):
		'''
		Creates a new matrix from m1 and m2, randomly selecting a joining date (column).
		'''
		self.crossovers += 1
		crossover_pnt = choice(self.dates)["start"]

		child_matrix = list()
		for i, _ in enumerate(m1):
			child_matrix.append(m1[i][:crossover_pnt] + m2[i][crossover_pnt:])

		return child_matrix


	def _calculate_dates(self):
		'''
		Builds a list with the column ranges for the different dates. This data eases
		the construction of random assignment matrixes (_random_assignment function.)
		'''
		# TODO: check itertools.groupby
		dates = list()
		last_date = self.shifts[0].date
		start = 0
		for i, s in enumerate(self.shifts):
			if s.date != last_date:
				dates.append({"start": start, "end": i, "date": last_date})
				start = i
				last_date = s.date

		dates.append({"start": start, "end": len(self.shifts), "date": last_date})

		return dates


	def _fitness(self, matrix):
		'''
		Returns a score of the quality of the solution.
		'''
		# TODO: add more scenarios to evaluate: closing and opening next day, weekends, preference matrix. 
		return self._days_off_fitness(matrix)


	def _days_off_fitness(self, matrix):
		'''
		Calculates a fitness score for the matrix based on the quality of its days off sequences.
		Per worker: score = max. consecutive days off / no. days off. The returned value is the average.
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


	def _random_assignment(self):
		'''
		Generates random assignments of the shifts. This method produces a matrix where:
		- All shifts are assigned.
		- Every worker has 1 or 0 shifts assigned per day.
		- Assignments fulfil the category condition.
		But the matrix needs yet to be validated (no. of hours assigned per worker).
		'''
		matrix = self._empty_matrix()

		for date in self.dates:
			# Generate different assignment options. Example: day with 3 shifts --> [[1,0,0], [0,1,0], [0,0,1]] 
			start, end = date["start"], date["end"]
			n = end-start
			options = [[1 if j == i else 0 for j in range(n)] for i in range(n)]

			w_index = list(range(len(self.workers)))

			while options:
				option = options.pop()
				shift = self.shifts[start+option.index(1)]

				while True:
					i = choice(w_index)
					worker = self.workers[i]
					if worker.category == shift.category:
						break

				w_index.remove(i)
				matrix[i][start:end] = option

		return matrix


	def _is_valid(self, matrix):
		'''
		Check if the matrix is valid (feasible).
		'''
		for i, w in enumerate(matrix):
			worker = self.workers[i]
			shifts_lst = [self.shifts[j] for j, s in enumerate(w) if s == 1]

			if not worker.can_cover(shifts_lst=shifts_lst):
				return False

		return True


	def _empty_matrix(self):
		''' 
		Returns a blank matrix (no. of workers * no. of shifts)
		'''
		return [[0 for s in self.shifts] for w in self.workers]
	

	def _print_solution(self):
		'''
		'''
		# Print dates
		print(" "*10, end="")
		for date in self.dates:
			print("{:>14}".format(str(date["date"])), end="")
		print()
		print(" "*10, end="")
		for date in self.dates:
			print("="*14, end="")
		print()

		# Print workers and shifts
		for i, w in enumerate(self.workers):
			print("{:>10}".format(w.name), end="")
			for date in self.dates:
				day_off = True
				for j in range(date["start"], date["end"]):
					if self.solution.matrix[i][j] == 1:
						day_off = False
						s = self.shifts[j]
						print("{:>14}".format("{:%H:%M}".format(s.start_time) + "-" + "{:%H:%M}".format(s.end_time)), end="")
				if day_off:
					print(" "*14, end="")
			print()


	def _preference_fitness(self, matrix):
		'''
		'''
		pass # TODO