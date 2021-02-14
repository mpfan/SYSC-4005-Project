from model import Model

if __name__ == '__main__':
    model = Model('RoundRobin')
    model.simulate()
    model.generateReport()
