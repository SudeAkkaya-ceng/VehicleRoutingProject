from VehicleRoutingProblem import *
from Visualizer            import *
import matplotlib.pyplot     as plt
import sys

def num_station_generator(matrix_size):
    return [
        int(matrix_size ** (1 / 2)),
        int(2 * matrix_size ** (1 / 2)),
        int(4 * matrix_size ** (1 / 2))
    ]

def start_end_generator(matrix_size):
    # 0: left bottom to right top  
    # 1: left bottom to left top
    # 2: left bottom to right bottom

    return {
        0: [(0, 0), (matrix_size - 1, matrix_size - 1)],
        1: [(0, 0), (0, matrix_size - 1)],
        2: [(0, 0), (matrix_size - 1, 0)]
    }

def optimize_SA():
    num_of_times = 5
    matrix_size  = 100
    stations     = 50
    start_point  = (0, 99)
    end_point    = (99, 99)
    iter         = 5000

    vrp = VehicleRoutingProblem(matrix_size, stations, start_point, end_point)

    initial_temperatures     = [250.0, 500.0, 750.0]
    lin_cooling_rates        = [.01, .02, .03]
    exp_cooling_rates        = [.001, .0005, .0001]
    cooling_factors          = ['lin', 'exp']

    for initial_temperature in initial_temperatures:
        for cooling_factor in cooling_factors:
            if cooling_factor == 'lin':
                for cooling_rate in lin_cooling_rates:
                    sum = 0
                    for i in range(num_of_times):
                        best_route, best_distance, runtime, scores = vrp.simulated_annealing(max_iterations=iter, initial_temperature=initial_temperature, cooling_rate=cooling_rate, cooling_factor=cooling_factor)
                        
                        sum += best_distance
                        print(
                            f"Step: {iter} \tSearch Space: {matrix_size}x{matrix_size} - Number of Stations: {stations} - {start_point} <-> {end_point}\tTime: {round(runtime, 3)} - Distance: {best_distance}\nInitial Temperature: {initial_temperature} - Cooling Rate: {cooling_rate} - Cooling Factor: {cooling_factor}"
                        )
                    print(f"Average Distance: {round(sum / len(lin_cooling_rates), 3)}\n")
            else:
                for cooling_rate in exp_cooling_rates:
                    sum = 0
                    for i in range(num_of_times):
                        best_route, best_distance, runtime, scores = vrp.simulated_annealing(max_iterations=iter, initial_temperature=initial_temperature, cooling_rate=cooling_rate, cooling_factor=cooling_factor)

                        sum += best_distance
                        print(
                            f"Step: {iter} \tSearch Space: {matrix_size}x{matrix_size} - Number of Stations: {stations} - {start_point} <-> {end_point}\tTime: {round(runtime, 3)} - Distance: {best_distance}\nInitial Temperature: {initial_temperature} - Cooling Rate: {cooling_rate} - Cooling Factor: {cooling_factor}"
                        )
                    print(f"Average Distance: {round(sum / len(exp_cooling_rates), 3)}\n")
def optimize_ACO():
    num_of_times = 5
    matrix_size  = 100
    stations     = 50
    start_point  = (0, 99)
    end_point    = (99, 99)
    iter         = 5000

    vrp = VehicleRoutingProblem(matrix_size, stations, start_point, end_point)

    num_ants          = [10, 20, 30, 40, 50]
    evaporation_rates = [.1, .3, .5, .7, .9]

    for num_ant in num_ants:
        for evaporation_rate in evaporation_rates:
            sum = 0
            for i in range(num_of_times):
                best_route, best_distance, runtime, scores = vrp.ant_colony_optimization(max_iterations=iter, num_ants=num_ant, evaporation_rate=evaporation_rate)

                sum += best_distance 
                print(
                    f"Step: {iter} \tSearch Space: {matrix_size}x{matrix_size} - Number of Stations: {stations} - {start_point} <-> {end_point}\tTime: {round(runtime, 3)} - Distance: {best_distance}\nNumber of Ants: {num_ant} - Evaporation Rate: {evaporation_rate}"
                ) 
            print(f"Average Distance: {round(sum / len(evaporation_rates), 3)}\n")       

def test_TS(vrp, iter):
    start = time.time()
    best_route, best_distance, runtime, scores = vrp.tabu_search(max_iterations=iter)
    end   = time.time()
    return end - start, best_distance
def test_SA(vrp, iter):
    # Simulated annealing parameters are chosen with respect to the results of optimize_SA() function
    # which is: initial_temperature = 250.0, cooling_rate = .001, cooling_factor = 'exp'
    
    start = time.time()
    best_route, best_distance, runtime, scores = vrp.simulated_annealing(max_iterations=iter, initial_temperature=250.0, cooling_rate=.001, cooling_factor='exp')
    end   = time.time()
    return end - start, best_distance                
def test_ACO(vrp, iter):
    # Ant colony optimization parameters are chosen with respect to the results of optimize_ACO() function
    # which is: num_ants = 10, evaporation_rate = .9

    start = time.time()
    best_route, best_distance, runtime, scores = vrp.ant_colony_optimization(max_iterations=iter, num_ants=10, evaporation_rate=.9)
    end   = time.time()
    return end - start, best_distance

def run_test(algorithm):
    random.seed(42)
    matrix_sizes   = [100, 150, 300,]
    max_iterations = [5000, 15000, 25000]
    num_stations   = [10, 20, 40] 
    
    for iter in max_iterations:
        for matrix_size in matrix_sizes:
            
            for stations in num_stations:
                runtime_sum = 0
                
                for i in range(0, 3):
                    start_point, end_point = start_end_generator(matrix_size)[i]
                    vrp = VehicleRoutingProblem(matrix_size, stations, start_point, end_point)
                    
                    if   algorithm == 'TS':
                        runtime, best_distance = test_TS(vrp, iter)
                    elif algorithm == 'SA':
                        runtime, best_distance = test_SA(vrp, iter)
                    elif algorithm == 'ACO':
                        runtime, best_distance = test_ACO(vrp, iter)
                    
                    runtime_sum += runtime

                    print(
                        f"Step: {iter} \tSearch Space: {matrix_size}x{matrix_size} - Number of Stations: {stations} - {start_point} <-> {end_point}\t Method: {algorithm}\t Time: {round(runtime, 3)} - Distance: {best_distance}"
                    )
                print(f"Average Runtime: {round(runtime_sum / 3, 3)}\n")

def write_test_result(algorithm):
    with open(f'{algorithm}_results.txt', 'w') as f: sys.stdout = f; run_test(algorithm)
