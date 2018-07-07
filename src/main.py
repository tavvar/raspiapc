#!/bin/python
import scheduler, threading


if __name__=='__main__': 
    s = scheduler.Scheduler(interval=10)

    measureThread = threading.Thread(target=s.syncMeasuresInterval)
    configThread = threading.Thread(target=s.syncConfigInterval)

    configThread.start()
    measureThread.start()
        


