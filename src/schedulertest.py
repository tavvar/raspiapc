import scheduler, threading

s = scheduler.Scheduler()

##print("Try syncConfig()")
##s.syncConfig()
##print("Try syncMeasures()")
##s.syncMeasures(1)

measureThread = threading.Thread(target=s.syncMeasuresInterval)
configThread = threading.Thread(target=s.syncConfigInterval)

configThread.start()
measureThread.start()
        

#s.syncMeasures(1)
#s.syncConfig()

