import scheduler, threading



s = scheduler.Scheduler()

print("Try syncConfig()")
s.syncConfig()
    

print("Try syncMeasueres()")
s.syncMeasures()