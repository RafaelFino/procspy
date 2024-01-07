import psutil, time
from datetime import datetime
from storage import Storage
from proc import Proc
from config import Config   
from logger import Logger

def check(procs: dict, last: datetime) -> dict:   
    targets = set(procs.keys())

    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            n = p.name()
            if n in targets:
                elapsed = (datetime.now() - last).total_seconds()
                procs[n].add(elapsed)
                storage.insert(n, elapsed)
                Logger.debug(f"+ Added {n}: {elapsed:.2f}s to {procs[n].get_elapsed():.2f}s -> Limit: {procs[n].limit:.2f}s")    

                if procs[n].is_expired():
                    Logger.warning(f"--> Expired {n}: {procs[n].get_elapsed()}s")
                    Logger.info(f"--> Killing {n} ({pid})")
                    p.kill()
                    Logger.success(f"--> Killed {n} ({pid})")

                targets.discard(n)
        except psutil.NoSuchProcess:
            pass
        except Exception as e:            
            Logger.warning(f"check error: {e}")

    return procs

def load(config: Config) -> dict:
    procs = {}

    for name, item in config.targets.items():
        Logger.info(f"Get {name}: {item.limit}s from config file")
        procs[name] = Proc(name, item.limit)
        
    for name, elapsed in storage.get_elapsed().items():
        Logger.info(f"Get {name}: {elapsed:.2f}s from database")

        if name in procs.keys():            
            procs[name].add(elapsed)
            Logger.info(f"Added {name}: {elapsed:.2f}s to {procs[name].get_elapsed():.2f}s")

    for name, proc in procs.items():
        Logger.info(f"{name}: {proc}")
    
    return procs
   
def main(config: Config, storage: Storage):        
    procs = load(config)    
    last = datetime.now()
    
    while True:        
        procs = check(procs, last)
        last = datetime.now()
        time.sleep(config.interval)        
        
if __name__ == "__main__":
    Logger.init("procspy.log")
    config = Config()
    config.load("config.json")
    storage = Storage(config.database)
    main(config, storage)
