'''
This file contains the class definition for the scheduling policy for 
workstations. The Policy follows the strategy pattrn
'''

class Policy:
    def __init__(self):
        pass

    # Implemented by an actual policy
    def get_workstation(self):
        # This is where the workstation is picked according to the choose policy
        raise NotImplementedError

class RoundRobin(Policy):
    def __init__(self, workstations, starting_workstation):
        super().__init__()

        self.workstations = workstations
        self.current_workstation = workstations[starting_workstation]
    
    # Override
    def get_workstation(self):
        # Implement round robin here
        raise NotImplementedError