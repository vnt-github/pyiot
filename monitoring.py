import utils, time, json, smtplib
from client import subscribe
from config import testClient, config
from datetime import datetime
from redisstore import Redis
from datetime import timedelta

monitoring = config["monitoring"]

def toRaiseAlert(values):
    print values
    if not values:
        return False
    avg = sum(values)/len(values)
    print "avg", avg
    return avg > testClient["threshold"]

def raiseAlert(emailAddresses):
    # sender = "pyiot@mailinator.com"
    # receivers = emailAddresses
    # message = """
    # warning! sensort is operating in threshold range
    # """
    # try:
    #     smtpObj = smtplib.SMTP('localhost')
    #     smtpObj.sendmail(sender, receivers, message)         
    #     print "Successfully sent email"
    # except Exception as err:
    #     print "Error: unable to send email", err

    # NOTE: need to configure an actual smtp server
    print "raising alert"
    return True

def monitor(range=timedelta(seconds=300)):
    subscribe()
    now = datetime.utcnow()
    previous = now - range
    print "data till now ", previous, now 
    stored_values = Redis.zrangebyscore(testClient['topic'], utils.datetime_to_epochtime(previous), utils.datetime_to_epochtime(now))

    parsed_values = [json.loads(value) for (value, score) in stored_values ]

    values = [each["value"] for each in parsed_values]

    raiseAlert = toRaiseAlert(values)
    if raiseAlert:
        raiseAlert(monitoring["emailAddresses"])
    return raiseAlert

if __name__ == "__main__":
    while True:
        monitor(timedelta(seconds=int(monitoring.get("rangeInSeconds", "500"))))
        time.sleep(int(monitoring.get("checkIntervalInSeconds", "10")))