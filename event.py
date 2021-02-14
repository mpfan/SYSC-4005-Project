from enum import Enum

'''
This module contains the class definition for events. 
'''

EventType = Enum('EventType', 'Inspection_Finished Processing_Finished EOS')

class Event:
    def __init__(self, event_type, time, entity, creator):
        self.event_type = event_type
        self.time = time
        self.entity = entity
        self.creator = creator
    
    def get_event_type(self):
        return self.event_type

    def get_time(self):
        return self.time

    def get_entity(self):
        return self.entity
    
    def get_creator(self):
        return self.creator

# Use these two methods to create the events
def create_inspection_finished(time, entity, creator):
    return Event(EventType.Inspection_Finished, time, entity, creator)

def create_processing_finished(time, entity, creator):
    return Event(EventType.Processing_Finished, time, entity, creator)

def create_end_of_simulation(time):
    return Event(EventType.EOS, time, None, None)
