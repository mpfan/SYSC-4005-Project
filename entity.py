import random

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
        self.busy_time = 0
        self.blocked_time = 0
        self.blocked = False

    def get_busy_time(self):
        return self.busy_time
    
    def set_busy_time(self, busy_time):
        self.busy_time = busy_time
    
    def get_blocked_time(self):
        return self.blocked_time
    
    def set_blocked_time(self, blocked_time):
        self.blocked_time = blocked_time
    
    def is_blocked(self):
        return self.blocked
    
    def set_blocked(self, blocked):
        self.blocked = blocked

    def inspect_component(self):
        # Return C1 if id = 1
        if self.id == 1:
            return Component(1)
        # Return C2 or C3 randomly if id = 2
        else:
            return Component(random.randint(2, 3))

class Workstation(Entity):
    def __init__(self, id, buffers):
        super().__init__(id)
        self.busy = False
        self.busy_time = 0
        self.idle_time = 0
        self.buffers = buffers
    
    def is_busy(self):
        return self.busy
    
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
    
    def get_buffers(self):
        return self.buffers
    
    def add_to_buffer(self, componentType, component):
        self.buffers[componentType].append(component)
    
    # Removes from the buffer head
    def remove_from_buffer(self, componentType):
        return self.buffers[componentType].pop(0)

    # Returns the product 
    def assemble_products(self):
        # Consume C1 and produces P1 if id = 1

        if self.id == 1:
            if len(self.buffers[1]) > 0:
                self.remove_from_buffer(1)
                return Product(1)
            else:
                return None
        # Consume C1 and C2 and produces P2 if id = 2
        elif self.id == 2:
            if len(self.buffers[1]) > 0 and len(self.buffers[2]) > 0:
                self.remove_from_buffer(1)
                self.remove_from_buffer(2)
                return Product(2)
            else:
                return None
        # Consume C1 and C3 and produces P3 if id = 3
        elif self.id == 3:
            if len(self.buffers[1]) > 0 and len(self.buffers[3]) > 0:
                self.remove_from_buffer(1)
                self.remove_from_buffer(3)
                return Product(3)
            else:
                return None
        else:
            raise Exepction("Unknown workstation")
            