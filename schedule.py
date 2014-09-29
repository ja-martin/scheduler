'''
Created on 4 Jul 2014

@author: Jose
'''

categories = (1, 2, 3)

class Schedule(object):
    '''
    classdocs
    '''


    def __init__(self, start_date, end_date, shifts_lst, workers_lst):
        '''
        Constructor
        '''
        self.start_date = start_date
        self.end_date = end_date
        self.shifts_lst = {}
        self.workers_lst = {}
        for c in categories:
            self.shifts_lst[c] = [s for s in shifts_lst if s.category == c]
            self.workers_lst[c] = [w for w in workers_lst if w.category == c]
        self._validations()

    def _validations(self):
        if not (self.start_date.weekday() == 0 and self.end_date.weekday() == 6):
            raise Exception("Start date and end date must be Monday and Sunday respectively.")
        if (self.end_date - self.start_date).days != 6:
            raise Exception("Start date and end date must cover a week.")
        
        for c in categories:
            shift_hrs = sum([s.duration() for s in self.shifts_lst[c]])
            contract_hrs = sum([w.contract_hrs for w in self.workers_lst[c]])
            max_hrs = sum([w.max_hrs for w in self.workers_lst[c]])
            if not (contract_hrs <= shift_hrs <= max_hrs):
                raise Exception("Shifts hours for category " + str(c) + " (" + str(shift_hrs) + ') not in between contract hours (' \
                                + str(contract_hrs) + ') and max hours (' + str(max_hrs) + ').')
                
        print('Validations OK.')
        
    def generate(self):
        for c in categories:
            frontier = [s for s in self._successors(None, c)]
            while frontier:
                path = frontier.pop()
                self._apply_path(path, c)
                if all([s.is_covered() for s in self.shifts_lst[c]]):
                    if all([w.total_hrs >= w.contract_hrs for w in self.workers_lst[c]]):
                        break
                else:
                    for s in self._successors(path, c):
                        frontier.append(s)
        self.show()
    
    def _successors(self, path, category):
        ''' Returns the list of new possible paths from the current position, adding all
        suitable assignment tuples (w, s), being w and s the indexes of worker and shift in the lists. '''
        if path is None:
            path = []
        next_shift = self._next_shift(category)
        suitable_workers = [w for w in self.workers_lst[category] if w.can_cover(shift=next_shift)]
        suitable_workers.sort(key=lambda worker: worker.total_hrs / worker.max_hrs, reverse=True)
        successors = []
        for w in suitable_workers:
            successors.append(path + [(w, next_shift)])
        return successors
    
    def _next_shift(self, category):
        ''' Returns the next unassigned shift of the list for the given category. '''
        for s in self.shifts_lst[category]:
            if not s.is_covered(): return s
        return None
    
    def _apply_path(self, path, category):
        current_path = set([(s.worker, s) for s in self.shifts_lst[category] if s.worker is not None])
        new_path = set(path)
        undo = current_path - new_path
        do = new_path - current_path
        for w, s in undo:
            w.uncover(s)
            s.unassign()
        for w, s in do:
            w.cover(s)
            s.assign_to(w)

    def show(self):
        print('SCHEDULE:', self.start_date, " TO ", self.end_date)
        for c in categories:
            for w in self.workers_lst[c]:
                print(w.name)
                for s in self.shifts_lst[c]:
                    if s.worker is w:
                        print(s.date, s.start_time, s.end_time)
        
    '''        
    def bridge_problem(here):
        "Find the fastest (least elapsed time) path to the goal in the bridge problem."
        here = frozenset(here) | frozenset(['light'])
        explored = set() # set of states we have visited
        # State will be a (peoplelight_here, peoplelight_there, time_elapsed)
        # E.g. ({1, 2, 5, 10, 'light'}, {}, 0)
        frontier = [ [(here, frozenset(), 0)] ] # ordered list of paths we have blazed
        while frontier:
            path = frontier.pop(0)
            here1, there1, t1 = state1 = path[-1]
            if not here1 or here1 == set(['light']):  ## Check for solution when we pull best path off frontier
                return path
            for (state, action) in bsuccessors(state1).items():
                if state not in explored:
                    here, there, t = state
                    explored.add(state)
                    path2 = path + [action, state]
                    # Don't check for solution when we extend a path
                    frontier.append(path2)
                    frontier.sort(key=elapsed_time)
                    return Fail

    def generate(self):
        # Each node of the tree is a tuple of 2 elements: first, a list of workers total hours and shifts assigned.
        # Second, a list of worker assigned for each shift.
        initial_state = ([(0, []) for _ in self.workers_lst], 
                        [None for _ in self.shifts_lst])
        frontier = [ initial_state ]
        while frontier:
            current_state = workers_lst, shifts_lst = frontier.pop()
            if not None in shifts_lst:
                condition = [workers_lst[i][0] >= self.workers_lst[i].contract_hrs for i in range(len(workers_lst))]
                print(current_state)
                print(condition)
                if all(condition): 
                    return current_state
            else:
                for s in self._successors(current_state):
                    frontier.append(s)
        return False
    
    def generate2(self):
        initial_state = (self.workers_lst, self.shifts_lst)
        frontier = [ initial_state ]
        while frontier:
            current_state = workers_lst, shifts_lst = frontier.pop()
            if all([s.is_covered() for s in shifts_lst]):
                if all([w.total_hrs >= w.contract_hrs for w in workers_lst]):
                    return current_state
            else:
                for su in self._successors2(current_state):
                    frontier.append(su)
        return None
    
    def _successors(self, state):
        w_lst, s_lst = state
        i = s_lst.index(None)
        shift = self.shifts_lst[i]
        category = shift.category
        duration = shift.end_time.hour - shift.start_time.hour + (shift.end_time.minute - shift.end_time.minute) / 60
        
        successors = []
        for j in range(len(w_lst)):
            worker = self.workers_lst[j]
            if worker.category == category and w_lst[j][0] + duration <= worker.max_hrs and not self.work_same_day(shift, w_lst, j):
                new_w_lst = list(w_lst)
                new_s_lst = list(s_lst)
                #print(new_w_lst)
                assignments = list(new_w_lst[j][1])
                assignments.append(i)
                new_w_lst[j] = (new_w_lst[j][0] + duration, assignments)
                #new_w_lst[j][0] += duration
                #new_w_lst[j][1].append(i)
                new_s_lst[i] = j
                successors.append((new_w_lst, new_s_lst))
        return successors
    
    def _successors2(self, state):
        workers_lst, shifts_lst = state
        next_shift = self._next_shift(shifts_lst)
        suitable_workers = [w for w in workers_lst if w.can_cover(next_shift)]
        successors = []
        
        for w in suitable_workers:
            pass 

    def work_same_day(self, shift, w_lst, j):
        date = shift.date
        assigned = w_lst[j][1]
        return date in [self.shifts_lst[i].date for i in assigned]

    def _next_shift(self, shifts_lst):
        for s in shifts_lst:
            if not s.is_covered(): return s
        return None'''        