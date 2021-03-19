'''
This file contains the class definition for the scheduling policy for 
workstations. The Policy follows the strategy pattrn
'''

class Policy:
    def __init__(self, workstations):
        self.workstations = workstations

    # Implemented by an actual policy
    def get_workstation(self, component_type: int):
        # This is where the workstation is picked according to the choose policy
        raise NotImplementedError
    
    def set_workstations(self, workstations):
        self.workstations = workstations

class RoundRobin(Policy):
    def __init__(self, workstations, starting_workstation):
        super().__init__(workstations)

        self.index = starting_workstation
    
    # Override
    # Note: Potential stack overflow. The condition is if all buffers are full.
    # This probably will not happen since we check the buffers before calling this function
    def get_workstation(self, component_type: int):
        # Retrive the workstation that's next in line
        workstation = self.workstations[self.index]

        # if not full, return the current workstation
        if len(workstation.get_buffers()[component_type]) < 2:

            # update the index for the next work station
            self.index = (self.index + 1) % len(self.workstations)
            return workstation

        # If the workstation that's next in line is full then we select 
        return self.get_workstation(component_type)
            
class ShortestQueue(Policy):
    def __init__(self, workstations):
        super().__init__(workstations)
    
    # Override
    def get_workstation(self, component_type: int):
        # Initialize to the first workstation
        workstation = self.workstations[0] 
        for work in self.workstations:
            # Strictly less than
            if len(work.get_buffers[component_type]) < len(workstation.get_buffers[component_type]):
                workstation = work
            # If equal W1 > W2 > W3
            elif len(work.get_buffers[component_type]) == len(workstation.get_buffers[component_type]):
                workstation = workstation if workstation.get_id() < work.get_id() else work

        return workstation
