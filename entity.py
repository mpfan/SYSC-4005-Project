'''
This file contains the class definition of the entities. The model tracks 
four types of eneities: Inspector, Component, Product, Workstation.
'''

class Entity:
    def __init__(self, id):
        self.id = id
    
    def get_id(self):
        return self.id

class Component(Entity):
    def __init__(self, id):
        super().__init__(id)

class Product(Entity):
    def __init__(self, id):
        super().__init__(id)

class Inspector(Entity):
    def __init__(self, id):
        super().__init__(id)
        self.busy = False
        self.busy_time = 0
        self.idle_time = 0
        self.blocked = False
    
    def is_busy(self):
        return self.is_busy
    
    def set_busy(self, busy):
        self.busy = busy

    def get_busy_time(self):
        return self.busy_time
    
    def set_busy_time(self, busy_time):
        self.busy_time = busy_time
    
    def get_idle_time(self):
        return self.idle_time
    
    def set_idle_time(self, idle_time):
        self.idle_time = idle_time
    
    def is_blocked(self):
        return self.blocked
    
    def set_blocked(self, blocked):
        self.blocked = blocked

    def inspect_component(self):
        # Return C1 if id = 1
        # Return C2 or C3 randomly if id = 2
        raise NotImplementedError

class Workstation(Entity):
    def __init__(self, id):
        super().__init__(id)
        self.busy = False
        self.busy_time = 0
        self.idle_time = 0
        self.buffer = []
    
    def is_busy(self):
        return self.is_busy
    
    def set_busy(self, busy):
        self.busy = busy

    def get_busy_time(self):
        return self.busy_time
    
    def set_busy_time(self, busy_time):
        self.busy_time = busy_time
    
    def get_idle_time(self):
        return self.idle_time
    
    def set_idle_time(self, idle_time):
        self.idle_time = idle_time
    
    def get_buffer_size(self):
        return len(self.buffer)
    
    def add_to_buffer(self, component):
        self.buffer.append(component)
    
    # Removes from the buffer head
    def remove_from_buffer(self):
        return self.buffer.pop(0)

    def assemble_products(self):
        # Consume C1 and produces P1 if id = 1
        # Consume C1 and C2 and produces P2 if id = 2
        # Consume C1 and C3 and produces P3 if id = 3
        raise NotImplementedError