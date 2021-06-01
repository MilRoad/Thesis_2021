from cvrp_info import CVRPInfo
from cvrp_advancedga import CVRPAdvancedGA
import os
import time
import signal
import json
import numpy as np
import sys

class CVRPRunner(object):

    def __init__(self, algorithm,  iterations):
        self.algorithm = algorithm
        self.print_cycle = 10
        self.num_iter = iterations
        #self.timings_file = open("timings/timings_{0}.txt".format(time.time()), "w")
        self.iter = 0
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        handling = True
        while handling:
            print("Iter:{0}\nPath:{1}\nWhat do? E for exec(), V for visualise, C to continue, S to save, X to exit".format(self.iter, self.best))
            c = raw_input()
            if c == "E":
                print("exec:")
                exec(raw_input())
            if c == "S":
                self.write_to_file("best-solution-{0}.part".format(self.iter))
            if c == "C":
                handling = False
            if c == "V":
                self.algorithm.info.visualise(self.best).show()
            elif c == "X":
                exit(0)

    def run(self):
        self.start_time = time.time()
        while self.iter < self.num_iter:
            best = self.algorithm.step()
            self.best = best
            # if self.iter % self.print_cycle == 0:
            #     print("iter: {0} best:{1}".format(self.iter, self.best.cost))
            self.iter += 1
            if time.time() - self.start_time > 1800:
                self.write_to_file("best-solution-marking.txt")
                break
        # print("Best solution: " + str(best))
        # print("Cost: " + str(best.cost))


    def write_to_file(self, file_name):
        lst = []
        for route in self.algorithm.best_solution.routes:
            temp = [int(c.strip()) for c in str(route).split(',')]
            lst.append(temp)
        info = {'cost': self.algorithm.best_solution.cost, 'routes': lst}
        with open('solution_ga.json', 'w') as f:
            json.dump(info, f)


if __name__ == "__main__":

    with open('data_new.json', 'r') as f:
        a = json.load(f)
    coords = a['coords']
    demand = a['demand']
    dimension = a['dimension']
    capacity = a['capacity']

    distance_matrix = np.array(a['matrix'])
    import time
    start_time = time.time()
    cvrp = CVRPRunner(CVRPAdvancedGA(CVRPInfo(distance_matrix, demand, capacity, dimension, coords, start_node=1, debug=True), 1, 100), 100)
    cvrp.run()
    print("--- %s seconds ---" % (time.time() - start_time))