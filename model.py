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
            
            self.process_event(event)

            if event.get_event_type() == EventType.EOS:
                break
    
    def get_snapshots(self):
        return self.snapshots

    # So this function will probably return a pandas object or some object that we can use to do analysis and visualization
    def generate_report(self):
        latest_snap = self.snapshots[-1]
        # for i, snapshot in enumerate(self.snapshots):
        #     print(f'############################ SNAPSHOT {i} ############################')
        #     print(f'Clock: {snapshot.get_clock()}')
        #     if snapshot.get_event() is not None:
        #         print(f'Event: {snapshot.get_event().get_event_type()}')
        #     print()
        #     print(f'############################ Inspectors ############################')
        #     for inspector in snapshot.get_inspectors():
                
        #         print(f'| Inspector {inspector.get_id()} |')
        #         print(f'Is Blocked: {inspector.is_blocked()}')
        #         print(f'Busy Time: {inspector.get_busy_time()}')
        #         print(f'Blocked Time: {inspector.get_blocked_time()}')
        #         print()

        #     print()
        #     print(f'############################ Workstations ############################')
        #     for workstation in snapshot.get_workstations():
                
        #         print(f'| Workstation {workstation.get_id()} |')

        #         for buffer_number, buffer in workstation.get_buffers().items():
        #             component_list = [str(component) for component in buffer]
        #             print(f'Buffer {buffer_number}: {component_list}')
        #             print()

        print("############################### OUTPUTS ###############################")
        print("Total components created:", len(latest_snap.get_components()))
        components_dict = {}
        for c in latest_snap.get_components():
            components_dict[c.get_id()] = components_dict.get(c.get_id(), 0) + 1 
        print("Component frequency: ", components_dict)

        print("Total products created:", len(latest_snap.get_products()))
        product_dict = {}
        for p in latest_snap.get_products():
            product_dict[p.get_id()] = product_dict.get(p.get_id(), 0) + 1
        print("Product frequency: ", product_dict)

        print("Total blocked time for Inspector 1: ", latest_snap.get_inspectors()[0].get_blocked_time())
        print("Total busy time for Inspector 1: ", latest_snap.get_inspectors()[0].get_busy_time())
        print("Total blocked time for Inspector 2: ", latest_snap.get_inspectors()[1].get_blocked_time())
        print("Total busy time for Inspector 2: ", latest_snap.get_inspectors()[1].get_busy_time())
        return self.snapshots
    
    def get_inspector1_blocked_time(self, t0):
        if t0 is None:
            return self.snapshots[-1].get_inspectors()[0].get_blocked_time()

        for index in range(len(self.snapshots)):
            if self.snapshots[index].get_clock() > t0:
                return self.snapshots[-1].get_inspectors()[0].get_blocked_time() - self.snapshots[index - 1].get_inspectors()[0].get_blocked_time()
    
    def get_inspector2_blocked_time(self, t0):
        if t0 is None:
            return self.snapshots[-1].get_inspectors()[1].get_blocked_time()

        for index in range(len(self.snapshots)):
            if self.snapshots[index].get_clock() > t0:
                return self.snapshots[-1].get_inspectors()[1].get_blocked_time() - self.snapshots[index - 1].get_inspectors()[1].get_blocked_time()
    
    def get_total_num_of_products(self, t0):
        if t0 is None:
            return len(self.snapshots[-1].get_products())

        for index in range(len(self.snapshots)):
            if self.snapshots[index].get_clock() > t0:
                return len(self.snapshots[-1].get_products()) - len(self.snapshots[index - 1].get_products())

    # Process the event
    def process_event(self, event):
        # We are always working with a new copy of the snapshot
        # At first, this new copy is the same as the previous snapshot
        current_snapshot = copy.deepcopy(self.snapshots[-1])
        self.policy.set_workstations(current_snapshot.workstations)

        clock = event.get_time()

        # current_snapshot.events.append(event)

        # Calculate cumulative stats
         # We are tracking the busy and idle time for inspectors and workstaions
        for inspector in current_snapshot.get_inspectors():
            if inspector.is_blocked():
                inspector.set_blocked_time(inspector.get_blocked_time() + (clock - current_snapshot.get_clock()))
            elif inspector.is_busy():
                inspector.set_busy_time(inspector.get_busy_time() + (clock - current_snapshot.get_clock()))
                

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
            current_snapshot.get_components().append(component)

            inspector.set_busy(False)

            # Check all buffers
            full = True
            for workstation in workstations:
                for c_type, buff in workstation.get_buffers().items():
                    if component.get_id() == c_type and len(buff) < 2:
                        full = False

            # Select a workstation according to a policy if buffers are not all full
            if not full:
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

                # Generate new event and append to the fel
                new_inspection_event = create_inspection_finished(clock + self.generator.get_inspection_time(new_component.get_id()), new_component, inspector)

                # add the new event to the FEL
                current_snapshot.add_to_fel(new_inspection_event)          

                inspector.set_busy(True)
            else:
                # Because inspector will always be working when not blocked. Therefore
                # idle means blocked and busy means not blocked
                inspector.set_blocked(True) 
                inspector.set_busy(False)

            # Update snapshot
            current_snapshot.set_clock(clock)
            current_snapshot.set_event(event)

            
            # Append the new snapshot
            self.snapshots.append(current_snapshot)
            self.policy.set_workstations(workstations)
        elif event.get_event_type() == EventType.Processing_Finished:
            #retrieve relevant event entities
            clock = event.get_time()
            product = event.get_entity()
            workstation = current_snapshot.get_workstations()[event.get_creator().get_id() - 1]

            # Update snapshot with new product  
            current_snapshot.get_products().append(product)

            # try to assemble new product
            new_product = workstation.assemble_products()

            if new_product is not None:
                workstation.set_busy(True)
                new_processing_event = create_processing_finished(clock + self.generator.get_processing_time(workstation.get_id()), new_product, workstation)
                current_snapshot.add_to_fel(new_processing_event)

            else:
                workstation.set_busy(False)
            
            # Unblock inspectors
            buffers = workstation.get_buffers()
            inspectors = current_snapshot.get_inspectors()
            for component_type, buf in buffers.items():
                if len(buf) < 2:
                    if component_type == 1:
                        inspectors[0].set_blocked(False)
                        if not inspectors[0].is_busy():
                            new_component = inspectors[0].inspect_component()

                            # Generate new event and append to the fel
                            new_inspection_event = create_inspection_finished(clock + self.generator.get_inspection_time(new_component.get_id()), new_component, inspector)

                            # add the new event to the FEL
                            current_snapshot.add_to_fel(new_inspection_event) 
                            inspectors[0].set_busy(True)   

                    elif component_type == 2 or component_type == 3:
                        inspectors[1].set_blocked(False)
                        if not inspectors[1].is_busy():
                            new_component = inspectors[1].inspect_component()

                            # Generate new event and append to the fel
                            new_inspection_event = create_inspection_finished(clock + self.generator.get_inspection_time(new_component.get_id()), new_component, inspector)

                            # add the new event to the FEL
                            current_snapshot.add_to_fel(new_inspection_event) 
                            inspectors[1].set_busy(True) 

            # Update snapshots
            current_snapshot.set_clock(clock)
            current_snapshot.set_event(event)
            # Save snapshot
            self.snapshots.append(current_snapshot)
            self.policy.set_workstations(current_snapshot.get_workstations())
        elif event.get_event_type() == EventType.EOS:
            current_snapshot.set_clock(clock)
            current_snapshot.set_event(event)
            self.snapshots.append(current_snapshot)
        else:
            raise Exception("Unknown event type")
    