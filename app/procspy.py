import psutil, os, time, datetime, sqlite3

procs = {}
target = {"chrome", "spotify", "firefox", "steam"}
for pid in psutil.pids():
    p = psutil.Process(pid)
    create = p.create_time()
    n = p.name()
    if n in target:
        if (n not in procs) or (create < procs[n]):
            procs[n] = create
                    
for name, create in procs.items():
    elapsed = (datetime.datetime.now() - datetime.datetime.fromtimestamp(create)).total_seconds()
    print(f"{name} : {elapsed}")
