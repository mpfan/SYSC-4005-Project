'''
This file contains the class definition for the system snapshot
'''


class Snapshot:
    def __init__(self, clock, workstations, products, components, inspectors, fel):
        self.clock = clock
        self.workstations = workstations
        self.products = products
        self.components = components
        self.inspectors = inspectors
        self.fel = fel
    
    def add_to_fel(self, event):
        for i in range(0, len(self.fel)):
            if event.get_time() <= self.fel[i].get_time():
                self.fel.insert(i, event)
                return
        self.fel.append(event)           

    def get_clock(self):
        return self.clock
    
    def get_workstations(self):
        return self.workstations
    
    def get_products(self):
        return self.products
    
    def get_components(self):
        return self.components
    
    def get_inspectors(self):
        return self.inspectors
    
    def get_fel(self):
        return self.fel

    def set_clock(self, clock):
        self.clock = clock
    
    def set_workstations(self, workstations):
        self.workstations = workstations
    
    def set_products(self, products):
        self.products = products
    
    def set_components(self, components):
        self.components = components
    
    def set_inspectors(self, inspectors):
        self.inspectors = inspectors
    
    def set_fel(self, fel):
        self.fel = fel
