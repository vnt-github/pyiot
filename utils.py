import threading
import random
from datetime import datetime

def setIterations(iterations=1):
    print("iterations", iterations)
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            times = iterations
            while times:
                times-=1
                f(*args, **kwargs)
        return wrapped_f
    return wrap

def setInterval(interval=0):
    print("interval:", interval)
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            e = threading.Event()
            while not e.wait(interval):
                f(*args, **kwargs)
        return wrapped_f
    return wrap
    

def datetime_to_epochtime(arg_time=None):
    if not arg_time:
        arg_time = datetime.utcnow()

    if isinstance(arg_time, datetime):
        time_list = list(arg_time.timetuple())
        arg_time = datetime(*time_list[:6])
        return int(round((arg_time - datetime(1970,1,1,0,0,0)).total_seconds()*1000))
    else:
        return None

if __name__ == "__main__":
    # @setIterations(1)
    @setInterval(1)
    def printD(*args, **kwargs):
        print args, kwargs
    printD(1,2,3, a=1, b=3)