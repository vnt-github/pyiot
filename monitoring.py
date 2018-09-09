from client import subscribe
from config import testClient
from datetime import datetime
from redisstore import Redis
from datetime import timedelta
import utils, time

def monitor():
    subscribe()
    now = datetime.utcnow()
    print "data till now "
    print Redis.zrange(testClient['topic'], 0, utils.datetime_to_epochtime(now))

if __name__ == "__main__":
    while True:
        monitor()
        time.sleep(10)