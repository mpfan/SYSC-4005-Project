from enum import Enum

'''
This module contains the class definition for events. 
'''

EventType = Enum('EventType', 'Inspection_Finished Processing_Finished')

class Event:
    def __init__(self, event_type, time, entity):
        self.event_type = event_type
        self.time = time
        self.entity = entity
    
    def get_event_type(self):
        return self.event_type

    def get_time(self):
        return self.time

    def get_entity(self):
        return self.entity

# Use these two methods to create the events
def create_inspection_finished(time, entity):
    return Event(EventType.Inspection_Finished, time, entity)

def create_processing_finished(time, entity):
    return Event(EventType.Processing_Finished, time, entity)
