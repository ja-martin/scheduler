from datetime import date, time, timedelta
from gascheduler import GaScheduler
from worker import Worker
from shift import Shift

if __name__ == '__main__':

    workers_lst = []
    #workers_lst.append(Worker(1, 'Josh', 1, [], 40, 48))
    #workers_lst.append(Worker(2, 'Lina', 2, [], 32, 40))
    #workers_lst.append(Worker(3, 'Dagmara', 2, [], 32, 40))
    #workers_lst.append(Worker(4, 'Rasa', 2, [], 20, 28))
    workers_lst.append(Worker(5, 'Emma', 3, [], 36, 48))
    workers_lst.append(Worker(6, 'Filipe', 3, [], 32, 40))
    workers_lst.append(Worker(7, 'Patrycia', 3, [], 32, 40))
    workers_lst.append(Worker(8, 'Joanna', 3, [], 10, 18))
    workers_lst.append(Worker(9, 'Jose', 3, [], 20, 28))
    
    #for w in workers_lst: print(w.partner_id, w.name, w.category, w.contract_hrs, sep='\t')
    
    start_date = date(2014, 7, 7) 
    week = [start_date + timedelta(days=i) for i in range(7)]
    
    shifts_lst = []
    
    #shifts_lst.append(Shift(week[0], time(13, 0),time(20, 30), 2))
    #shifts_lst.append(Shift(week[0], time(13, 0),time(20, 30), 2))
    #shifts_lst.append(Shift(week[0], time(6, 0), time(14, 00), 1))
    shifts_lst.append(Shift(week[0], time(8, 00),time(16, 30), 3))
    shifts_lst.append(Shift(week[0], time(6, 0), time(14, 00), 3))
    shifts_lst.append(Shift(week[0], time(8, 0), time(12, 30), 3))
    shifts_lst.append(Shift(week[0], time(13, 0),time(20, 30), 3))
    
    #shifts_lst.append(Shift(week[1], time(6, 0),  time(15, 00), 1))
    #shifts_lst.append(Shift(week[1], time(13, 30),time(20, 30), 2))
    #shifts_lst.append(Shift(week[1], time(13, 30),time(20, 30), 2))
    shifts_lst.append(Shift(week[1], time(6, 0),  time(13, 00), 3))
    shifts_lst.append(Shift(week[1], time(8, 0),  time(16, 30), 3))
    shifts_lst.append(Shift(week[1], time(13, 0), time(20, 30), 3))
    
    shifts_lst.append(Shift(week[2], time(8, 0),  time(15, 30), 3))
    #shifts_lst.append(Shift(week[2], time(14, 30),time(20, 30), 2))
    #shifts_lst.append(Shift(week[2], time(14, 30),time(20, 30), 2))
    #shifts_lst.append(Shift(week[2], time(6, 0),  time(15, 30), 1))
    shifts_lst.append(Shift(week[2], time(6, 0),  time(13, 30), 3))
    shifts_lst.append(Shift(week[2], time(8, 30), time(15, 00), 3))
    shifts_lst.append(Shift(week[2], time(13, 00),time(20, 30), 3))
    
    #shifts_lst.append(Shift(week[3], time(6, 0), time(14, 0), 1))
    shifts_lst.append(Shift(week[3], time(6, 0), time(14, 30), 3))
    shifts_lst.append(Shift(week[3], time(8, 0), time(16, 0), 3))
    shifts_lst.append(Shift(week[3], time(14, 0),time(20, 30), 3))
    #shifts_lst.append(Shift(week[3], time(12, 0),time(20, 30), 2))
    #shifts_lst.append(Shift(week[3], time(12, 0),time(20, 30), 2))
    
    #shifts_lst.append(Shift(week[4], time(6, 0), time(15, 00), 1))
    #shifts_lst.append(Shift(week[4], time(15, 0),time(20, 30), 2))
    #shifts_lst.append(Shift(week[4], time(15, 0),time(20, 30), 2))
    shifts_lst.append(Shift(week[4], time(6, 0), time(13, 30), 3))
    shifts_lst.append(Shift(week[4], time(12, 0),time(20, 30), 3))
    shifts_lst.append(Shift(week[4], time(8, 0), time(16, 30), 3))
    
    #shifts_lst.append(Shift(week[5], time(12, 0), time(20, 30), 2))
    shifts_lst.append(Shift(week[5], time(8, 0), time(15, 00), 3))
    #shifts_lst.append(Shift(week[5], time(8, 0), time(16, 00), 2))
    shifts_lst.append(Shift(week[5], time(14, 0), time(20, 30), 3))
    
    #shifts_lst.append(Shift(week[6], time(12, 0), time(20, 30), 2))
    shifts_lst.append(Shift(week[6], time(12, 0), time(20, 30), 3))
    #shifts_lst.append(Shift(week[6], time(8, 0), time(15, 00), 2))
    shifts_lst.append(Shift(week[6], time(8, 0), time(12, 00), 3))

    sch = GaScheduler(workers_lst, shifts_lst)