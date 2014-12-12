class BruteForceScheduler(object):
    '''
    Solves scheduling problem using a brute force algorithm.
    '''

    dates = None
    shifts = None
    workers = None
    categories = None


    def __init__(self, dates, shifts, workers, categories):
        '''
        Constructor
        '''
        self.dates = dates
        self.shifts = {}
        self.workers = {}
        self.categories = categories
        
        for c in self.categories:
            self.shifts[c] = [s for s in shifts if s.category == c]
            self.workers[c] = [w for w in workers if w.category == c]

        self._validate_input()


    def generate(self):
        '''
        Does an exhaustive search of the solution space and prints first solution.
        Assumes roles are fixed - a worker of a given category cannot cover shifts of different categories.
        '''
        for c in self.categories:
            frontier = [s for s in self._get_successors(None, c)]
            while frontier:
                path = frontier.pop()
                self._apply_path(path, c)
                if all([s.is_covered() for s in self.shifts[c]]):
                    if all([w.total_hrs >= w.contract_hrs for w in self.workers[c]]):
                        break
                else:
                    for s in self._get_successors(path, c):
                        frontier.append(s)

        self._print()


    def _validate_input(self):
        '''
        Start/end dates must cover a week from Monday to Sunday.
        Sum of hours to schedule must be within the range of contract hours and max. hours.
        '''
        if len(self.dates) != 7:
            raise Exception("Schedule must cover a week period.")

        if not (self.dates[0].weekday() == 0 and self.dates[-1].weekday() == 6):
            raise Exception("Start/end dates must be Monday and Sunday respectively.")
        
        for c in self.categories:
            shift_hrs = sum([s.duration for s in self.shifts[c]])
            contract_hrs = sum([w.contract_hrs for w in self.workers[c]])
            max_hrs = sum([w.max_hrs for w in self.workers[c]])

            print("Category: {0} Contract: {1} Shifts: {2} Max: {3}".format(c, contract_hrs, shift_hrs, max_hrs))

            if not (contract_hrs <= shift_hrs <= max_hrs):
                raise Exception("Invalid shift hours ({0}) for category {1}. Must be between {2} (contract hours) and {3} (max. hours).".format(shift_hrs, c, contract_hrs, max_hrs))


    def _get_successors(self, path, category):
        ''' 
        Builds all possible paths from the current position.
        '''
        if path is None:
            path = []

        next_shift = self._next_shift(category)
        suitable_workers = [w for w in self.workers[category] if w.can_cover(shift=next_shift)]
        # Sort so that we first select worker with less hours assigned.
        suitable_workers.sort(key=lambda worker: worker.total_hrs / worker.max_hrs, reverse=True)

        successors = []
        for w in suitable_workers:
            successors.append(path + [(w, next_shift)])

        return successors


    def _next_shift(self, category):
        ''' 
        Returns next unassigned shift for the given category. 
        '''
        for s in self.shifts[category]:
            if not s.is_covered(): 
                return s

        return None


    def _apply_path(self, path, category):
        '''
        Makes necessary shift assignments/unassignments to get to the new path from the current one.
        '''
        current_path = set([(s.worker, s) for s in self.shifts[category] if s.worker is not None])
        new_path = set(path)
        undo = current_path - new_path
        do = new_path - current_path

        for w, s in undo:
            w.uncover(s)
            s.unassign()

        for w, s in do:
            w.cover(s)
            s.assign_to(w)


    def _print(self):
        '''
        Prints the schedule.
        '''
        print(" "*10, end="")
        for d in self.dates:
            print("{:>14}".format(str(d)), end="")
        print()
        print(" "*10, end="")
        for d in self.dates:
            print("="*14, end="")
        print()

        for c in self.categories:
            for w in self.workers[c]:
                print("{:>10}".format(w.name), end="")
                for d in self.dates:
                    s = w.shift_by_date(d)
                    if s is None:
                        print(" "*14, end="")
                    else:
                        print("{:>14}".format("{:%H:%M}".format(s.start_time) + "-" + "{:%H:%M}".format(s.end_time)), end="")
                print()

        print()
       