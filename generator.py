import random
import math

'''
This class contains functions that will produce the input data for 
inspection time and workstation processing time
'''
class Generator: 
    def __init__(self, seed):
        self.rngC1 = random.Random()
        self.rngC1.seed(seed[0])

        self.rngC2 = random.Random()
        self.rngC2.seed(seed[1])

        self.rngC3 = random.Random()
        self.rngC3.seed(seed[2])

        self.rngW1 = random.Random()
        self.rngW1.seed(seed[3])

        self.rngW2 = random.Random()
        self.rngW2.seed(seed[4])

        self.rngW3 = random.Random()
        self.rngW3.seed(seed[5])

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
        return self.exponential_variate(0.0965, self.rngC1.random())

    def get_c2_time(self):
        return self.exponential_variate(0.0644, self.rngC2.random())

    def get_c3_time(self):
        return self.exponential_variate(0.0491, self.rngC3.random())

    def get_w1_time(self):
        return self.exponential_variate(0.2172, self.rngW1.random())

    def get_w2_time(self):
        return self.exponential_variate(0.0902, self.rngW2.random())

    def get_w3_time(self):
        return self.exponential_variate(0.1143, self.rngW3.random())

    '''
    Function to generate exponential random variate. The random variate is generated using the 
    ITT method.
    '''
    def exponential_variate(self, lambd, rn):
        return math.floor(-math.log(1 - rn) / lambd)
