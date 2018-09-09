import random
import json
from client import publish
from uuid import uuid4
def randomInRange(low=22, high=28):
    value = random.randint(low, high)
    msg = {
        "id": uuid4().hex,
        "value": value
    }
    rc, msgId = publish(json.dumps(msg))
    print "publish results rc:", rc, "msgId:", msgId