run pip install -r requirements.txt

# for client simulations run 
```sh
$ python simulations.py
```

descriptions
client.py: mqtt client handler for the device to be simulated
config.json: all the configurations
redisstore.py: redis handler

testClient.json: client specific configurations
    topic: the topic which a client should publish to
    simulation_fn: the function which should be used to generate the pseudo data values
    simulation_args: the arguments for simulation_fn
    flow_fn: the fuction which defines the behaviour of the device/sensor
    flow_args: flow_fn's arguments

simulation_fns.py: this file should contain the functions to be used to generate the data value for various devices/sensors


simulations.py: this initializes the device/sensor and executes acc to flow_fn(if present else single run)

#for monitoring run 
```sh
$ python monitoring.py.py
```
monitoring.py: subscribes to the cilent topic and fetches the data from db/store to perform any desired operations