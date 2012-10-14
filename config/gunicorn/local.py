import os
 
def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

bind = '0.0.0.0:5001'
workers = numCPUs() * 2 + 1
worker_class = 'gevent'
backlog = 2048
debug = False

from gunicorn.arbiter import Arbiter
import signal
Arbiter.SIGNALS.remove(signal.SIGWINCH)
