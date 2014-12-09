class Worker(object):
    '''
    classdocs
    '''
    partner_id = None
    name = None
    category = None
    contract_hrs = None
    max_hrs = None
    shifts_lst = None
    total_hrs = None


    def __init__(self, partner_id, name, category, contract_hrs, max_hrs):
        '''
        Constructor
        '''
        self.partner_id = partner_id
        self.name = name
        self.category = category
        self.contract_hrs = contract_hrs
        self.max_hrs = max_hrs
        
        self.shifts_lst = []
        self.total_hrs = 0


    def can_cover(self, shift=None, shifts_lst=None):
        '''
        Checks if the given shift or group of shifts can be assigned to this worker.
        Checks: duration, category and not having two shifts on the same day (for a group of shifts).
        '''
        if shifts_lst:
            return self.contract_hrs <= sum([s.duration for s in shifts_lst]) <= self.max_hrs \
                   and len(set([s.date for s in shifts_lst])) == len(shifts_lst) \
                   and all([s.category == self.category for s in shifts_lst])
        elif shift:
            return shift.category == self.category and not self._work_on(shift.date) \
                   and self.total_hrs + shift.duration <= self.max_hrs


    def cover(self, shift):
        '''
        '''
        self.shifts_lst.append(shift)
        self.total_hrs += shift.duration
    

    def uncover(self, shift):
        '''
        '''
        self.shifts_lst.remove(shift)
        self.total_hrs -= shift.duration
    

    def shift_by_date(self, date):
        '''
        '''
        for s in self.shifts_lst:
            if s.date == date:
                return s

        return None


    def _work_on(self, date):
        '''
        '''
        for s in self.shifts_lst:
            if s.date == date: 
                return True

        return False