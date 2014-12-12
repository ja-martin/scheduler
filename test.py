import cProfile
from bf_scheduler import BruteForceScheduler
from ga_scheduler import GeneticScheduler
from shift import Shift
from worker import Worker
from datetime import time
from datetime import date
from datetime import timedelta


if __name__ == '__main__':
    ####################################################################
    ################### T  E  S  T      D  A  T  A #####################
    ####################################################################
    dates = [date(2014, 7, 7) + timedelta(days=i) for i in range(7)]

    categories = (1, 2, 3)

    workers = []
    workers.append(Worker(1, 'Josh',     1, 40, 48))
    workers.append(Worker(2, 'Lina',     2, 32, 40))
    workers.append(Worker(3, 'Dagmara',  2, 32, 40))
    workers.append(Worker(4, 'Rasa',     2, 20, 28))
    workers.append(Worker(5, 'Emma',     3, 36, 44))
    workers.append(Worker(6, 'Filipe',   3, 32, 40))
    workers.append(Worker(7, 'Patrycia', 3, 32, 40))
    workers.append(Worker(8, 'Joanna',   3, 10, 18))
    workers.append(Worker(9, 'Jose',     3, 20, 28))
    
    shifts = []
    # Monday
    shifts.append(Shift(dates[0], time(13, 00), time(20, 30), 2))
    shifts.append(Shift(dates[0], time(13, 00), time(20, 30), 2))
    shifts.append(Shift(dates[0], time( 6, 00), time(14, 00), 1))
    shifts.append(Shift(dates[0], time( 8, 00), time(16, 30), 3))
    shifts.append(Shift(dates[0], time( 6, 00), time(14, 00), 3))
    shifts.append(Shift(dates[0], time( 8, 00), time(12, 30), 3))
    shifts.append(Shift(dates[0], time(13, 00), time(20, 30), 3))
    # Tuesday
    shifts.append(Shift(dates[1], time( 6, 00), time(15, 00), 1))
    shifts.append(Shift(dates[1], time(13, 30), time(20, 30), 2))
    shifts.append(Shift(dates[1], time(13, 30), time(20, 30), 2))
    shifts.append(Shift(dates[1], time( 6, 00), time(13, 00), 3))
    shifts.append(Shift(dates[1], time( 8, 00), time(16, 30), 3))
    shifts.append(Shift(dates[1], time(13, 00), time(20, 30), 3))
    # Wednesday
    shifts.append(Shift(dates[2], time( 8, 00), time(15, 30), 3))
    shifts.append(Shift(dates[2], time(14, 30), time(20, 30), 2))
    shifts.append(Shift(dates[2], time(14, 30), time(20, 30), 2))
    shifts.append(Shift(dates[2], time( 6, 00), time(15, 30), 1))
    shifts.append(Shift(dates[2], time( 6, 00), time(13, 30), 3))
    shifts.append(Shift(dates[2], time( 8, 30), time(15, 00), 3))
    shifts.append(Shift(dates[2], time(13, 00), time(20, 30), 3))
    # Thursday
    shifts.append(Shift(dates[3], time( 6, 00), time(14, 00), 1))
    shifts.append(Shift(dates[3], time( 6, 00), time(14, 30), 3))
    shifts.append(Shift(dates[3], time( 8, 00), time(16, 00), 3))
    shifts.append(Shift(dates[3], time(14, 00), time(20, 30), 3))
    shifts.append(Shift(dates[3], time(12, 00), time(20, 30), 2))
    shifts.append(Shift(dates[3], time(12, 00), time(20, 30), 2))
    # Friday
    shifts.append(Shift(dates[4], time( 6, 00), time(15, 00), 1))
    shifts.append(Shift(dates[4], time(15, 00), time(20, 30), 2))
    shifts.append(Shift(dates[4], time(15, 00), time(20, 30), 2))
    shifts.append(Shift(dates[4], time( 6, 00), time(13, 30), 3))
    shifts.append(Shift(dates[4], time(12, 00), time(20, 30), 3))
    shifts.append(Shift(dates[4], time( 8, 00), time(16, 30), 3))
    # Saturday
    shifts.append(Shift(dates[5], time(12, 00), time(20, 30), 2))
    shifts.append(Shift(dates[5], time( 8, 00), time(15, 00), 3))
    shifts.append(Shift(dates[5], time( 8, 00), time(16, 00), 2))
    shifts.append(Shift(dates[5], time(14, 00), time(20, 30), 3))
    # Sunday
    shifts.append(Shift(dates[6], time(12, 00), time(20, 30), 2))
    shifts.append(Shift(dates[6], time(12, 00), time(20, 30), 3))
    shifts.append(Shift(dates[6], time( 8, 00), time(15, 00), 2))
    shifts.append(Shift(dates[6], time( 8, 00), time(12, 00), 3))
    
    shifts.sort(key=lambda x: x.category)

    ####################################################################
    ###################  R  U  N      T  E  S  T #######################
    ####################################################################
        
    scheduler = BruteForceScheduler(dates, shifts, workers, categories)
    #scheduler.generate()
    cProfile.run('scheduler.generate()') 

    scheduler2 = GeneticScheduler(workers, shifts) 
    #scheduler2.generate()
    cProfile.run('scheduler2.generate()')     