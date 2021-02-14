# Local modules
from entity import *
from snapshot import Snapshot
from policy import RoundRobin
from event import create_inspection_finished, create_processing_finished, EventType
from generator import get_service_time, get_processing_time

# System modules
import copy

'''
This file contains the class definition for the model
'''

class Model:
    def __init__(self, policy):
        # Initializes the initial system snapshot
        clock = 0
        w1 = Workstation(1, {1: []})
        w2 = Workstation(2, {1: [], 2: []})
        w3 = Workstation(3, {1: [], 3: []})
        workstations = [w1, w2, w3]
        products = []
        components = []
        inspectors = [Inspector(n) for n in range (1,3)] # 2 inspectors with id 1,2
        fel = []
        

        self.policy = policy
        self.snapshots = [Snapshot(clock, workstations, products, components, inspectors, fel)]
    
    # This is where the simulations happens
    def simulate(self):
        raise NotImplementedError
    
    # So this function will probably return a pandas object or some object that we can use to do analysis and visualization
    def generate_report(self):
        raise NotImplementedError

    # Process the event
    def process_event(self, event):
        # We are always working with a new copy of the snapshot
        # At first, this new copy is the same as the previous snapshot
        current_snapshot = copy.deepcopy(self.snapshots[len(self.snapshots) - 1])

        # Calculate cumulative stats
         # We are tracking the busy and idle time for inspectors
        if not inspector.is_blocked():
            inspector.set_busy_time(inspector.get_busy_time() + (clock - current_snapshot.get_clock())
        else:
            inspector.set_blocked_time(inspector.get_blocked_time() + (clock - current_snapshot.get_clock())

        if workstation.is_busy():
            workstation.set_busy_time(workstation.get_busy_time() + (clock - current_snapshot.get_clock())
        else:
            workstation.set_idle_time(workstation.get_idle_time() + (clock - current_snapshot.get_clock())

        # The new snapshot will diverge from the previous snapshot from here on 
        if event.get_event_type() == EventType.Inspection_Finished:
            # Handle Inspection_Finished
            
            # Retrive relevent entities for this event 
            component = event.get_entity()
            inspector = current_snapshot.get_inspectors()[event.get_creator().get_id()]
            workstations = current_snapshot.get_workstations()
            clock = event.get_time()
            
            # Check all buffers
            full = True
            for workstation in workstations:
                for c_type, buff in workstation.get_buffers().items():
                    if component.get_id() == c_type and len(buff) < 2:
                        full = False
                        break

            # Select a workstation according to a policy if buffers are not all full
            if not full:
                inspector.set_blocked(False)
                current_workstation = None
                if inspector.get_id() == 1:
                    current_workstation = self.policy.get_workstation(component.get_id())
                else:
                    # inspector 2 will pass component to workstation 2 or 3 depending on component 2 or 3
                    current_workstation = current_snapshot.get_workstation()[component.get_id()] 
                
                current_workstation.get_buffers[component.get_id()].append(component)

                # Check if the workstation is able to start processing the components
                # Try to assemble new product
                if not current_workstation.is_busy():
                    new_product = workstation.assemble.product()

                    if new_product is not None:
                        current_workstation.set_busy(True)
                        new_processing_event = create_processing_finished(clock + generator.get_processing_time(), new_product, current_workstation)
                        current_snapshot.get_fel().append(new_processing_event)

                new_component = inspector.inspect_element()
                # add component to snapshot
                current_snapshot.get_components().append(new_component)
                
                # Generate new event and append to the fel
                new_inspection_event = create_inspection_finished(clock + generator.get_service_time(), new_component, inspector)

                # add the new event to the FEL
                current_snapshot.get_fel().append(new_inspection_event)          
            else:
                # Because inspector will always be working when not blocked. Therefore
                # idle means blocked and busy means not blocked
                inspector.set_blocked(True)                     
            # Update snapshot
            current_snapshot.set_clock(clock)
            
            # Append the new snapshot
            snapshots.append(current_snapshot)

        elif event.get_event_type() == EventType.Processing_Finished:
            #retrieve relevant event entities
            clock = event.get_time()
            product = event.get_entity()
            workstation = current_snapshot.get_workstations()[event.get_creator().get_id()]

            # Update snapshot with new product  
            current_snapshot.get_products().append(product)
            
            # Unblock inspectors
            buffers = workstation.get_buffer()
            inspectors = current_snapshot.get_inspectors()
            for component_type, buf in buffers.items():
                if len(buf) < 2:
                    if component_type == 1:
                        inspectors[1].set_blocked(False)
                    elif component_type == 2 or component_type == 3:
                        inspectors[2].set_blocked(False)
                    
            # Update snapshots
            workstation.set_busy(False)
            current_snapshot.set_clock(clock)
            
            # Save snapshot
            self.snapshots.append(current_snapshot)
        else:
            raise Exception("Unknown event type")