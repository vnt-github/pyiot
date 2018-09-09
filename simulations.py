import random, json
import simulation_fns
import utils
from config import config, testClient
from client import subscribe

def simulate():

    simulation_fn_name = testClient.get("simulation_fn")
    if not simulation_fn_name:
        return 'please provide simulation_fn'

    simulation_fn = getattr(simulation_fns, simulation_fn_name, False)

    if not simulation_fn:
        return 'simulation_fn not found'

    simulation_args = testClient.get('simulation_args', [])

    if testClient.get("flow_fn", False):
        flow_fn = getattr(utils, testClient["flow_fn"], False)
        if not flow_fn:
            return 'flow_fn not found'
        flow_args = testClient.get("flow_args", None)
        @flow_fn(*flow_args)
        def fn():
            simulation_fn(*simulation_args)
        fn()
    else:
        simulation_fn(*simulation_args)
        return 'simulation done'

print simulate()
