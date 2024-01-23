from   VehicleRoutingProblem import *
import pandas                as pd
import matplotlib.pyplot     as plt
import time
import webbrowser

def create_comparison_table(routes, distances, algorithm_names):
    data = {}
    for i, name in enumerate(algorithm_names):
        data[f'{name} Route']    = [str(station) for station in routes[i]] + [''] * (max(len(route) for route in routes) - len(routes[i]))
        data[f'{name} Distance'] = [distances[i]] + [''] * (len(routes[i]) - 1)
    
    comparison_table = pd.DataFrame(data)
    return comparison_table

def save_html(table, filename):
    html = table.to_html()
    with open(filename, 'w') as file:
        file.write(html)

def plot_routes(start_point, end_point, route, color, plot_name, subplot_id):
    plt.scatter(*zip(*[start_point] + route + [end_point]), color='red', s=100, label='Stations')
    plt.scatter(start_point[0], start_point[1], color='green', s=100, label='Start')
    plt.scatter(end_point[0], end_point[1], color='orange', s=100, label='End')

    current_point = start_point
    for next_point in route + [end_point]:
        plt.plot([current_point[0], next_point[0]], [current_point[1], current_point[1]], linestyle='-', color=color, linewidth=2)
        plt.plot([next_point[0], next_point[0]], [current_point[1], next_point[1]], linestyle='-', color=color, linewidth=2)
        current_point = next_point

    all_points = [start_point] + route + [end_point]
    for i, txt in enumerate(all_points):
        plt.annotate(f"{i}", (txt[0], txt[1]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.title(f'{plot_name}')
    plt.legend()
    plt.grid(True)
    
    
def plot_results(algorithm_names, best_scores_list, iteration_times_list):
        plt.figure(figsize=(12, 4))

        for i in range(len(algorithm_names)):
            plt.plot(1, 2, 1)
            plt.plot(best_scores_list[i], label=algorithm_names[i])

          
        plt.title('Best Scores')
        plt.xlabel('Iteration')
        plt.ylabel('Best Distance')
        plt.legend()

        plt.tight_layout()
        plt.show()
