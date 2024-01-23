from   VehicleRoutingProblem import *
from   Visualizer            import *
from   Tester                import run_test, write_test_result
import matplotlib.pyplot     as plt

def main():
    matrix_size  = 100
    num_stations = 15
    start_point  = (0, 0)
    end_point    = (99, 99)
    max_iterations = 15000

    vrp = VehicleRoutingProblem(matrix_size, num_stations, start_point, end_point, by_hand=True)
    
    # Tabu Search
    best_route_TS, best_distance_TS, runtime ,scores_tabu  = vrp.tabu_search(max_iterations=max_iterations)
    print(f'Tabu Search Time:             {round(runtime, 3)}')

    # Simulated Annealing
    best_route_SA, best_distance_SA, runtime,scores_sa   = vrp.simulated_annealing(max_iterations=max_iterations, initial_temperature=250.0, cooling_rate=.001, cooling_factor='exp')
    print(f'Simulated Annealing Time:     {round(runtime, 3)}')

    # Ant Colony Optimization
    best_route_ACO, best_distance_ACO, runtime, scores_aco = vrp.ant_colony_optimization(max_iterations=max_iterations, num_ants=10, evaporation_rate=.9)
    print(f'Ant Colony Optimization Time: {round(runtime, 3)}')

    # Plotting
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))  # 1 row, 3 columns

    plt.subplot(1, 3, 1)
    plot_routes(start_point, end_point, best_route_TS, 'blue', 'Tabu Search', 1)
    plt.subplot(1, 3, 2)
    plot_routes(start_point, end_point, best_route_SA, 'black', 'Simulated Annealing', 2)
    plt.subplot(1, 3, 3)
    plot_routes(start_point, end_point, best_route_ACO, 'purple', 'Ant Colony Optimization', 3)

    plt.tight_layout()
    plt.show()

    routes           = [best_route_TS, best_route_SA, best_route_ACO]
    distances        = [best_distance_TS, best_distance_SA, best_distance_ACO]
    algorithm_names  = ['Tabu', 'SA', 'ACO']
    comparison_table = create_comparison_table(routes, distances, algorithm_names) 

    # Comparison Table
    save_html(comparison_table, 'comparison_table.html')
    webbrowser.open('comparison_table.html')
    
    plot_results(
        ['Tabu Search', 'Simulated Annealing', 'Ant Colony Optimization'],
        [scores_tabu, scores_sa, scores_aco],
        [max_iterations,max_iterations,max_iterations]
    )

    #print("Comparison Table:")
    #print(comparison_table)

def test():
    write_test_result('TS' )
    write_test_result('SA' )
    write_test_result('ACO')

if __name__ == "__main__":
    main()
    #test()