from matplotlib import pyplot as plt
import numpy as np
import random
import math
import itertools
import time

class VehicleRoutingProblem:
    # if by_hand is True, user will be prompted to enter station coordinates
    # otherwise, stations will be generated randomly
    def __init__(self, matrix_size, num_stations, start_point, end_point, by_hand=False):
        self.matrix_size = matrix_size
        self.num_stations = num_stations
        self.start_point = start_point
        self.end_point = end_point
        self.matrix = self.generate_matrix()
        self.stations = self.generate_stations(by_hand=by_hand)

    def generate_matrix(self):
        return np.random.randint(1, 20, size=(self.matrix_size, self.matrix_size))

    def generate_stations(self, by_hand=False):
        stations = set()

        # generate randomly
        if not by_hand:
            while len(stations) < self.num_stations:
                station = (random.randint(0, self.matrix_size - 1), random.randint(0, self.matrix_size - 1))
                if station not in stations and station != self.start_point and station != self.end_point:
                    stations.add(station)
            return list(stations)
        # generate by hand with user prompts
        else:
            for i in range(self.num_stations):
                print(f'Station {i + 1}:')
                try:
                    x = int(input('x: '))
                    y = int(input('y: '))

                    if x < 0 or x >= self.matrix_size or y < 0 or y >= self.matrix_size:
                        raise IndexError
                except(ValueError, IndexError) as e:
                    if e == ValueError:
                        print('Invalid input. Type integer.')
                    else:
                        print(f'Invalid input. Coordinates must be in the range of matrix size. -> {self.matrix_size}x{self.matrix_size}')
                    return self.generate_stations(by_hand=True)
                station = (x, y)
                if station not in stations and station != self.start_point and station != self.end_point:
                    stations.add(station)
                else:
                    print('Invalid input. Try again.')
                    return self.generate_stations(by_hand=True)
            return list(stations)


    def calculate_distance(self, route):
        distance = 0
        current_location = self.start_point
        for location in route:
            distance += abs(location[0] - current_location[0]) + abs(location[1] - current_location[1])
            current_location = location
        distance += abs(self.end_point[0] - current_location[0]) + abs(self.end_point[1] - current_location[1])
        return distance

    def exp_cooling(self, initial_temperature, cooling_rate, iteration):
        return initial_temperature * math.exp(-cooling_rate * iteration)
    
    def linear_cooling(self, initial_temperature, cooling_rate, iteration):
        return initial_temperature - cooling_rate * iteration

    # metaheuristics 1
    def tabu_search(self, max_iterations):
        start = time.time()

        current_route = random.sample(self.stations, len(self.stations))
        best_route = current_route.copy()
        tabu_list = []
        best_distance = self.calculate_distance(best_route)
        scores = []
        
        for i in range(max_iterations):
            neighbors = []
            for j in range(len(current_route)):
                for k in range(j + 1, len(current_route)):
                    neighbor = current_route[:]
                    neighbor[j], neighbor[k] = neighbor[k], neighbor[j]
                    neighbors.append(neighbor)

            best_neighbor = None
            best_neighbor_distance = float('inf')

            for neighbor in neighbors:
                if neighbor not in tabu_list:
                    neighbor_distance = self.calculate_distance(neighbor)
                    if neighbor_distance < best_neighbor_distance:
                        best_neighbor = neighbor
                        best_neighbor_distance = neighbor_distance
            
            
            if best_neighbor_distance < best_distance:
                best_route = best_neighbor[:]
                best_distance = best_neighbor_distance

            current_route = best_neighbor[:]
            tabu_list.append(best_neighbor)
            if len(tabu_list) > 10:
                tabu_list.pop(0)
                
            scores.append(best_distance)
        end = time.time()

        return best_route, best_distance, end - start, scores

    # metaheuristics 2
    def simulated_annealing(self, max_iterations, initial_temperature, cooling_rate, cooling_factor = 'lin'):
        start = time.time()
        scores = []
        current_route = random.sample(self.stations, len(self.stations))
        best_route = current_route.copy()
        best_distance = self.calculate_distance(best_route)

        for i in range(max_iterations):
            if cooling_factor == 'exp':
                temperature = self.exp_cooling(initial_temperature, cooling_rate, i)
            else:
                temperature = self.linear_cooling(initial_temperature, cooling_rate, i)           
            if temperature == 0:
                break     
            #print(temperature)  

            random_index_1, random_index_2 = random.sample(range(len(current_route)), 2)
            neighbor = current_route[:]
            neighbor[random_index_1], neighbor[random_index_2] = neighbor[random_index_2], neighbor[random_index_1]

            neighbor_distance = self.calculate_distance(neighbor)
            current_distance = self.calculate_distance(current_route)

            if cooling_factor == 'exp':
                if neighbor_distance < current_distance or random.random() < math.exp(-(neighbor_distance - current_distance) / temperature):
                    current_route = neighbor[:]
                
                    if neighbor_distance < best_distance:
                        best_route = neighbor[:]
                        best_distance = neighbor_distance
            else:
                if neighbor_distance < current_distance or random.random() < (neighbor_distance - current_distance) / temperature:
                    current_route = neighbor[:]
                
                    if neighbor_distance < best_distance:
                        best_route = neighbor[:]
                        best_distance = neighbor_distance
            scores.append(best_distance)
        end = time.time()

        return best_route, best_distance, end - start, scores

    # metaheuristics 3
    def ant_colony_optimization(self, max_iterations, num_ants, evaporation_rate=0.5):
        start = time.time()
        scores = []
        pheromone = np.ones((self.matrix_size, self.matrix_size))
        best_distance = float('inf')
        best_route = []

        for iteration in range(max_iterations):
            ants = []
            for ant in range(num_ants):
                current_route = random.sample(self.stations, len(self.stations))
                distance = self.calculate_distance(current_route)
                
                if distance < best_distance:
                    best_distance = distance
                    best_route = current_route.copy()
                ants.append((current_route, distance))

            pheromone *= evaporation_rate

            for ant, (route, distance) in enumerate(ants):
                pheromone_to_add = 1 / distance
                for i in range(len(route) - 1):
                    pheromone[route[i][0], route[i][1]] += pheromone_to_add
            scores.append(best_distance)
        end = time.time()

        return best_route, best_distance, end - start, scores
    
    # low performance, best solution
    """ def shortest_route(self, start_point, end_point):
        shortest_path = []
        shortest_distance = float('inf')

        for route in itertools.permutations(self.stations):
            distance = self.calculate_distance(route)
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_path = route
                
        return shortest_path, shortest_distance """