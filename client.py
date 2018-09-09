import json, time, random
import utils
from datetime import datetime
import paho.mqtt.client as mqttClient
from config import config, testClient
from redisstore import Redis


Connected = False
broker_config = config["mqttBroker"]

def on_connect_cb(client, userdata, flags, rc):
    global Connected
    print "on_connect_cb rc", rc
    if rc == 0:
        Connected = True
    else:
        print("connection failed")


def on_subscribe_cb(client, userdata, mid, granted_qos):
    print "on_subscribe_cb", client, userdata, mid, granted_qos

def on_message_cb(client, userdata, message):
    print "message topic", message.topic
    print "message payload", message.payload
    print "message qos", message.qos
    print "message retain", message.retain
    Redis.zadd(message.topic, utils.datetime_to_epochtime(), message.payload)

client = mqttClient.Client(transport="websockets")
client.on_connect = on_connect_cb
client.on_message = on_message_cb

def connect_client():
    client.connect(str(broker_config["host"]), port=broker_config["port"])
    client.loop_start()
    while not Connected:
        print 'retrying client connection every: ', broker_config["retryDelay"], 'seconds'
        time.sleep(broker_config["retryDelay"])


def publish(message, qos=1):
    while not Connected:
        connect_client()
    return_code, message_id = client.publish(testClient["topic"], message, qos)
    return (return_code, message_id)

def subscribe():
    while not Connected:
        connect_client()
    client.subscribe(testClient["topic"])
    # client.loop_forever()

if __name__ == "__main__":
    print publish('sensor_data', 1)
    # print subscribe()
    print "this is the mqtt handler"