from entity import *
from snapshot import Snapshot
from policy import RoundRobin
from event import create_inspection_finished, create_processing_finished, EventType
from generator import get_service_time, get_processing_time

'''
This file contains the class definition for the model
'''

class Model:
    def __init__(self):
        # Initializes the initial system snapshot
        clock = 0
        workstations = [Workstation(n) for n in range(1, 4)] # 3 workstations with id 1,2,3
        products = []
        components = []
        inspectors = [Inspector(n) for n in range (1,3)] # 2 inspectors with id 1,2
        fel = []
        
        self.snapshot = Snapshot(clock, workstations, products, components, inspectors, fel)
    
    # This is where the simulations happens
    def simulate(self):
        raise NotImplementedError
    
    # So this function will probably return a pandas object or some object that we can use to do analysis and visualization
    def generate_report(self):
        raise NotImplementedError

    # Process the event
    def process_event(self, event):
        if event.get_event_type == EventType.Inspection_Finished:
            # Handle Inspection_Finished
            raise NotImplementedError
        elif event.get_event_type == EventType.Processing_Finished:
            # Handle Processing_Finished
            raise NotImplementedError
        else:
            raise Exception("Unknow event type")