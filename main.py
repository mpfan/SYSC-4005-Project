from model import Model
from entity import *
from snapshot import Snapshot
from event import create_inspection_finished, create_processing_finished, create_end_of_simulation, EventType
import random 

# System modules
import copy

if __name__ == '__main__':
    inspector1_blocked_time = []
    inspector2_blocked_time = []
    total_products_created = []
    # Initializes the initial system snapshot
    clock = 0
    w1 = Workstation(1, {1: []})
    w2 = Workstation(2, {1: [], 2: []})
    w3 = Workstation(3, {1: [], 3: []})
    workstations = [w1, w2, w3]
    products = []
    components = []
    # 2 inspectors with id 1,2
    inspectors = [Inspector(n) for n in range(1, 3)]

    i1 = []
    i2 = []

    for n in range(10):
        # Initial events
        eos = create_end_of_simulation(1000)
        inspectionFinished1 = create_inspection_finished(
            2, Component(1), inspectors[0])
        inspectionFinished2 = create_inspection_finished(
            3, Component(2), inspectors[1])
        inspectionFinished3 = create_inspection_finished(
            4, Component(3), inspectors[1])
        # inspectionFinished3 = create_inspection_finished(
        #     3, Component(3), inspectors[1])

        inspectors[0].set_busy(True)
        inspectors[1].set_busy(True)

        fel = [inspectionFinished1, inspectionFinished2, inspectionFinished3, eos]

        initial_snapshot = Snapshot(clock, workstations, products, components, inspectors, fel, None)

        buf_size = {1: [], 2: [], 3: []}
        i_block = {1: [], 2: []}

        model = Model('ShortestQueue', n, copy.deepcopy(initial_snapshot))
        model.simulate()
        model.generate_report()

        i1.append(model.get_inspector1_blocked_time(None))
        i2.append(model.get_inspector2_blocked_time(None))

    print({"i1": i1, "i2": i2})