'''
Created on 4 Jul 2014

@author: Jose
'''
from __future__ import print_function
import cProfile
from schedule import Schedule
from schedule_iter import Schedule_iter
from shift import Shift
from worker import Worker
from rule import Rule
from datetime import time
from datetime import date
from datetime import timedelta
import datetime

category_dict = {1: 'SM', 2: 'SSV', 3: 'BAR'}
categories = (1, 2, 3)


if __name__ == '__main__':

    workers_lst = []
    workers_lst.append(Worker(1, 'Josh', 1, [], 40, 48))
    workers_lst.append(Worker(2, 'Lina', 2, [], 32, 40))
    workers_lst.append(Worker(3, 'Dagmara', 2, [], 32, 40))
    workers_lst.append(Worker(4, 'Rasa', 2, [], 20, 28))
    workers_lst.append(Worker(5, 'Emma', 3, [], 36, 48))
    workers_lst.append(Worker(6, 'Filipe', 3, [], 32, 40))
    workers_lst.append(Worker(7, 'Patrycia', 3, [], 32, 40))
    workers_lst.append(Worker(8, 'Joanna', 3, [], 10, 18))
    workers_lst.append(Worker(9, 'Jose', 3, [], 20, 28))
    
    #for w in workers_lst: print(w.partner_id, w.name, w.category, w.contract_hrs, sep='\t')
    
    start_date = date(2014, 7, 7) 
    week = [start_date + timedelta(days=i) for i in range(7)]
    
    shifts_lst = []
    
    shifts_lst.append(Shift(week[0], time(13, 0),time(20, 30), 2))
    shifts_lst.append(Shift(week[0], time(13, 0),time(20, 30), 2))
    shifts_lst.append(Shift(week[0], time(6, 0), time(14, 00), 1))
    shifts_lst.append(Shift(week[0], time(8, 00),time(16, 30), 3))
    shifts_lst.append(Shift(week[0], time(6, 0), time(14, 00), 3))
    shifts_lst.append(Shift(week[0], time(8, 0), time(12, 30), 3))
    shifts_lst.append(Shift(week[0], time(13, 0),time(20, 30), 3))
    
    shifts_lst.append(Shift(week[1], time(6, 0),  time(15, 00), 1))
    shifts_lst.append(Shift(week[1], time(13, 30),time(20, 30), 2))
    shifts_lst.append(Shift(week[1], time(13, 30),time(20, 30), 2))
    shifts_lst.append(Shift(week[1], time(6, 0),  time(13, 00), 3))
    shifts_lst.append(Shift(week[1], time(8, 0),  time(16, 30), 3))
    shifts_lst.append(Shift(week[1], time(13, 0), time(20, 30), 3))
    
    shifts_lst.append(Shift(week[2], time(8, 0),  time(15, 30), 3))
    shifts_lst.append(Shift(week[2], time(14, 30),time(20, 30), 2))
    shifts_lst.append(Shift(week[2], time(14, 30),time(20, 30), 2))
    shifts_lst.append(Shift(week[2], time(6, 0),  time(15, 30), 1))
    shifts_lst.append(Shift(week[2], time(6, 0),  time(13, 30), 3))
    shifts_lst.append(Shift(week[2], time(8, 30), time(15, 00), 3))
    shifts_lst.append(Shift(week[2], time(13, 00),time(20, 30), 3))
    
    shifts_lst.append(Shift(week[3], time(6, 0), time(14, 0), 1))
    shifts_lst.append(Shift(week[3], time(6, 0), time(14, 30), 3))
    shifts_lst.append(Shift(week[3], time(8, 0), time(16, 0), 3))
    shifts_lst.append(Shift(week[3], time(14, 0),time(20, 30), 3))
    shifts_lst.append(Shift(week[3], time(12, 0),time(20, 30), 2))
    shifts_lst.append(Shift(week[3], time(12, 0),time(20, 30), 2))
    
    shifts_lst.append(Shift(week[4], time(6, 0), time(15, 00), 1))
    shifts_lst.append(Shift(week[4], time(15, 0),time(20, 30), 2))
    shifts_lst.append(Shift(week[4], time(15, 0),time(20, 30), 2))
    shifts_lst.append(Shift(week[4], time(6, 0), time(13, 30), 3))
    shifts_lst.append(Shift(week[4], time(12, 0),time(20, 30), 3))
    shifts_lst.append(Shift(week[4], time(8, 0), time(16, 30), 3))
    
    shifts_lst.append(Shift(week[5], time(12, 0), time(20, 30), 2))
    shifts_lst.append(Shift(week[5], time(8, 0), time(15, 00), 3))
    shifts_lst.append(Shift(week[5], time(8, 0), time(16, 00), 2))
    shifts_lst.append(Shift(week[5], time(14, 0), time(20, 30), 3))
    
    shifts_lst.append(Shift(week[6], time(12, 0), time(20, 30), 2))
    shifts_lst.append(Shift(week[6], time(12, 0), time(20, 30), 3))
    shifts_lst.append(Shift(week[6], time(8, 0), time(15, 00), 2))
    shifts_lst.append(Shift(week[6], time(8, 0), time(12, 00), 3))
    
    shifts_lst.sort(key = lambda x: x.category)

    for c in categories:
        print("Category ", c, ": ", sum([s.duration() for s in shifts_lst if s.category == c]), " total hours")
        print("Workers: ", sum([w.contract_hrs for w in workers_lst if w.category == c]), " contract hours")
        print("and ", sum([w.max_hrs for w in workers_lst if w.category == c]), " max hours")
    
    #for s in shifts_lst:
    #    print(s.date, s.start_time, s.end_time, category_dict[s.category], sep='\t')
        
    sch = Schedule(week[0], week[6], shifts_lst, workers_lst)
    cProfile.run('sch.generate()')
    #cProfile.run('sch.generate2()')
    #sch.generate2()
    
    