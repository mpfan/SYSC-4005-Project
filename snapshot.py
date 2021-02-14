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

    def set_clock(clock):
        self.clock = clock
    
    def set_workstations(workstations):
        self.workstations = workstations
    
    def set_products(products):
        self.products = products
    
    def set_components(components):
        self.components = components
    
    def set_inspectors(inspectors):
        self.inspectors = inspectors
    
    def set_fel(fel):
        self.fel = fel