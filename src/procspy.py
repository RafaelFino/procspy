import psutil, time, sys
from datetime import datetime
from storage import Storage
from proc import Proc
from config import Config   
from logger import Logger


day = datetime.now().strftime("%Y-%m-%d")
def check(procs: dict, last: datetime, config: Config) -> dict:   
    targets = set(procs.keys())
    storage = Storage(config.database)

    if day != datetime.now().strftime("%Y-%m-%d"):
        Logger.info(f"New day: {day} -> Reset elapsed time")
        for proc in procs.values():
            proc.reset()
        day = datetime.now().strftime("%Y-%m-%d")

    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            n = p.name()
            if n in targets:
                elapsed = (datetime.now() - last).total_seconds()
                procs[n].add(elapsed)
                storage.insert(n, elapsed)
                Logger.info(f"+ Added {n} use in {elapsed:.2f}s to {procs[n].get_elapsed():.2f}s -> Limit: {procs[n].limit:.2f}s")    

                if procs[n].is_expired():
                    Logger.info(f"--> Expired {n}: {procs[n].get_elapsed()}s/{procs[n].limit}s")
                    Logger.info(f"--> Killing {n} ({pid})")
                    p.kill()
                    Logger.success(f"--> Killed {n} ({pid})")

                targets.discard(n)
        except psutil.NoSuchProcess:
            pass
        except Exception as e:            
            Logger.warning(f"check error: {e}")    

    storage.close()        

    return procs

def loadProcs(config: Config) -> dict:
    procs = {}

    for name, item in config.targets.items():
        Logger.info(f"Get {name}: limited to {item.limit}s from config file")
        procs[name] = Proc(name, item.limit)

    storage = Storage(config.database)
    data = storage.get_elapsed()
    storage.close()

    for name, elapsed in data.items():

        if name in procs.keys():            
            procs[name].add(elapsed)
            Logger.info(f"Load {name} from database with {elapsed:.2f}s from previous session")

    for name, proc in procs.items():
        Logger.success(f"Including process for [{name}]: {proc}")
    
    return procs
   
def main(config: Config):
    procs = loadProcs(config)    
    last = datetime.now()    
    
    while True:        
        procs = check(procs, last, config)
        last = datetime.now()
        time.sleep(config.interval)        
        
if __name__ == "__main__":    
    ret = 0
    try:
        if len(sys.argv) < 2:
            raise Exception("Usage: python procspy.py <config file>")

        config = Config()
        config.load(sys.argv[1])
        Logger.init(config.log_name)    
        Logger.success(f"Config load from file: {sys.argv[1]}")
        
        main(config)
        
    except Exception as e:
        Logger.error(f"{e}")
        ret = 1
    
    finally:
        Logger.info("Exiting...")        
        sys.exit(ret)
    
