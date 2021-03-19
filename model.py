# Local modules
from entity import *
from snapshot import Snapshot
from policy import RoundRobin, ShortestQueue
from event import create_inspection_finished, create_processing_finished, create_end_of_simulation, EventType
from generator import Generator

# System modules
import copy

'''
This file contains the class definition for the model
'''

class Model:
    def __init__(self, policyName, seed, initial_snapshot):
        self.snapshots = [initial_snapshot]
        self.generator = Generator(seed)

        if policyName == "RoundRobin":
            self.policy = RoundRobin(self.snapshots[0].get_workstations(), 0)
        elif policyName == "ShortestQueue":
            self.policy = ShortestQueue(self.snapshots[0].get_workstations())
    
    # This is where the simulations happens
    def simulate(self):
        while True:
            # get the latest snapshot and state
            event = self.snapshots[-1].get_fel().pop(0)

            if event.get_event_type() == EventType.EOS:
                print("Simulation has completed")
                break
            
            self.process_event(event)
        
    
    # So this function will probably return a pandas object or some object that we can use to do analysis and visualization
    def generate_report(self):
        latest_snap = self.snapshots[-1]
        print("Created components:", len(latest_snap.get_components()))
        print("Created products", len(latest_snap.get_products()))
        return self.snapshots

    # Process the event
    def process_event(self, event):
        # We are always working with a new copy of the snapshot
        # At first, this new copy is the same as the previous snapshot
        current_snapshot = copy.deepcopy(self.snapshots[-1])

        clock = event.get_time()

        # Calculate cumulative stats
         # We are tracking the busy and idle time for inspectors and workstaions
        for inspector in current_snapshot.get_inspectors():
            if not inspector.is_blocked():
                inspector.set_busy_time(inspector.get_busy_time() + (clock - current_snapshot.get_clock()))
            else:
                inspector.set_blocked_time(inspector.get_blocked_time() + (clock - current_snapshot.get_clock()))

        for workstation in current_snapshot.get_workstations():
            if workstation.is_busy():
                workstation.set_busy_time(workstation.get_busy_time() + (clock - current_snapshot.get_clock()))
            else:
                workstation.set_idle_time(workstation.get_idle_time() + (clock - current_snapshot.get_clock()))

        # The new snapshot will diverge from the previous snapshot from here on 
        if event.get_event_type() == EventType.Inspection_Finished:
            # Handle Inspection_Finished
            
            # Retrive relevent entities for this event 
            component = event.get_entity()
            inspector = current_snapshot.get_inspectors()[event.get_creator().get_id() - 1]
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
                    current_workstation = current_snapshot.get_workstations()[component.get_id() - 1] 
                
                current_workstation.add_to_buffer(component.get_id(), component)

                # Check if the workstation is able to start processing the components
                # Try to assemble new product
                if not current_workstation.is_busy():
                    new_product = current_workstation.assemble_products()

                    if new_product is not None:
                        current_workstation.set_busy(True)
                        new_processing_event = create_processing_finished(clock + self.generator.get_processing_time(current_workstation.get_id()), new_product, current_workstation)
                        current_snapshot.add_to_fel(new_processing_event)

                new_component = inspector.inspect_component()
                # add component to snapshot
                current_snapshot.get_components().append(new_component)
                
                # Generate new event and append to the fel
                new_inspection_event = create_inspection_finished(clock + self.generator.get_inspection_time(inspector.get_id()), new_component, inspector)

                # add the new event to the FEL
                current_snapshot.add_to_fel(new_inspection_event)          
            else:
                # Because inspector will always be working when not blocked. Therefore
                # idle means blocked and busy means not blocked
                inspector.set_blocked(True)                     
            # Update snapshot
            current_snapshot.set_clock(clock)
            
            # Append the new snapshot
            self.snapshots.append(current_snapshot)
            self.policy.set_workstations(current_snapshot.get_workstations())
        elif event.get_event_type() == EventType.Processing_Finished:
            #retrieve relevant event entities
            clock = event.get_time()
            product = event.get_entity()
            workstation = current_snapshot.get_workstations()[event.get_creator().get_id() - 1]

            # Update snapshot with new product  
            current_snapshot.get_products().append(product)
            
            # Unblock inspectors
            buffers = workstation.get_buffers()
            inspectors = current_snapshot.get_inspectors()
            inspector = None
            for component_type, buf in buffers.items():
                if len(buf) < 2:
                    if component_type == 1:
                        inspectors[0].set_blocked(False)
                       
                    elif component_type == 2 or component_type == 3:
                        inspectors[1].set_blocked(False)

            if inspector is not None:
                 # Generate new event and append to the fel
                new_inspection_event = create_inspection_finished(clock + self.generator.get_inspection_time(inspector.get_id()), inspector.inspect_component(), inspector)

                # add the new event to the FEL
                current_snapshot.add_to_fel(new_inspection_event) 

            # try to assemble new product
            new_product = workstation.assemble_products()

            if new_product is not None:
                workstation.set_busy(True)
                new_processing_event = create_processing_finished(clock + self.generator.get_processing_time(workstation.get_id()), new_product, workstation)
                current_snapshot.add_to_fel(new_processing_event)
            else:
                workstation.set_busy(False)
            
            # Update snapshots
            current_snapshot.set_clock(clock)
            # Save snapshot
            self.snapshots.append(current_snapshot)
            self.policy.set_workstations(current_snapshot.get_workstations())
        else:
            raise Exception("Unknown event type")
