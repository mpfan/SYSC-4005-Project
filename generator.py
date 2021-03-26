import random
import math

'''
This class contains functions that will produce the input data for 
inspection time and workstation processing time
'''
class Generator: 
    def __init__(self, seed):
        random.seed(seed)

    def get_inspection_time(self, component):
        if component == 1:
            return self.get_c1_time()
        elif component == 2:
            return self.get_c2_time()
        elif component == 3:
            return self.get_c3_time()
        else:
            raise Exception("Unkown component")

    def get_processing_time(self, workstation):
        if workstation == 1:
            return self.get_w1_time()
        elif workstation == 2:
            return self.get_w2_time()
        elif workstation == 3:
            return self.get_w3_time()
        else:
            raise Exception("Unkown workstation")

    def get_c1_time(self):
        return self.exponential_variate(0.0965, random.random())

    def get_c2_time(self):
        return self.exponential_variate(0.0644, random.random())

    def get_c3_time(self):
        return self.exponential_variate(0.0491, random.random())

    def get_w1_time(self):
        return self.exponential_variate(0.2172, random.random())

    def get_w2_time(self):
        return self.exponential_variate(0.0902, random.random())

    def get_w3_time(self):
        return self.exponential_variate(0.1143, random.random())

    '''
    Function to generate exponential random variate. The random variate is generated using the 
    ITT method.
    '''
    def exponential_variate(self, lambd, rn):
        return math.floor(-math.log(1 - rn) / lambd)
