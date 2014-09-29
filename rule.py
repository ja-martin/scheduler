'''
Created on 4 Jul 2014

@author: Jose
'''

class Rule(object):
    '''
    classdocs
    '''


    def __init__(self, worker, date, start_time, end_time):
        '''
        Constructor
        '''
        self.worker = worker
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        
    def affects(self, shift):
        pass
        