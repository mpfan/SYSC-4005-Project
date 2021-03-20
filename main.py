from model import Model
from entity import *
from snapshot import Snapshot
from event import create_inspection_finished, create_processing_finished, create_end_of_simulation, EventType

if __name__ == '__main__':
     # Initializes the initial system snapshot
    clock = 0
    w1 = Workstation(1, {1: [Component(1)]})
    w2 = Workstation(2, {1: [], 2: []})
    w3 = Workstation(3, {1: [], 3: []})
    workstations = [w1, w2, w3]
    products = []
    components = [Component(1)]
    # 2 inspectors with id 1,2
    inspectors = [Inspector(n) for n in range(1, 3)]

    # Initial events
    eos = create_end_of_simulation(1000)
    inspectionFinished1 = create_inspection_finished(
        2, Component(1), inspectors[0])
    inspectionFinished2 = create_inspection_finished(
        3, Component(2), inspectors[1])

    fel = [inspectionFinished1, inspectionFinished2, eos]

    initial_snapshot = Snapshot(clock, workstations, products, components, inspectors, fel, None)

    model = Model('RoundRobin', 1, initial_snapshot)
    model.simulate()
    snapshots = model.generate_report()
