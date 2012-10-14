import os
 
def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

workers = numCPUs() * 2 + 1
worker_class = 'gevent'
backlog = 1024
debug = True
