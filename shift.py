class Shift(object):
    '''
    classdocs
    '''
    _break_limit = 6
    _break_duration = 0.5

    def __init__(self, date, start_time, end_time, category):
        '''
        Constructor
        '''
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.category = category
        self.duration = self._calculate_duration()
        
        self.worker = None
        

    def is_covered(self):
        '''
        '''
        return self.worker is not None
    

    def assign_to(self, worker):
        '''
        '''
        self.worker = worker
        

    def unassign(self):
        '''
        '''
        self.worker = None
        

    def _calculate_duration(self):
        '''
        '''
        d = (self.end_time.hour - self.start_time.hour) + (self.end_time.minute - self.start_time.minute)/60
        return d if d < self.__class__._break_limit else d - self.__class__._break_duration
        