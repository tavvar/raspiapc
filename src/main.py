#!/bin/python
import scheduler, threading


if __name__=='__main__': 
    s = scheduler.Scheduler()

    measureThread = threading.Thread(target=s.syncMeasuresInterval)
    configThread = threading.Thread(target=s.syncConfigInterval)

    configThread.start()
    measureThread.start()
        


