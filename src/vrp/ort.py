"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Distances are in meters.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model(dist_mat, num_veh, depot):
    """Stores the data for the problem."""
    data = {}
    # data["distance_matrix"] = [
    #    [0.0, 25771.4, 16242.1],
    #    [26280.4, 0.0, 29361.2],
    #    [16318.5, 29566.2, 0.0],
    # ]
    # with open('dist_matrix.txt', 'r') as f:
    #    l = [[int(num) for num in line.split(',')] for line in f]
    data["distance_matrix"] = dist_mat

    for i in range(len(data["distance_matrix"])):
        for j in range(len(data["distance_matrix"])):
            data["distance_matrix"][i][j] = int(data["distance_matrix"][i][j])

    # data["distance_matrix"] = list(map(list, zip(*data["distance_matrix"])))
    data["num_vehicles"] = num_veh
    data["depot"] = depot
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    # print(f"Objective: {solution.ObjectiveValue()}")
    routes = []
    total_distances = []
    max_route_distance = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        # plan_output = "Route for vehicle {}:\n".format(vehicle_id)
        route_distance = 0
        vehicle_route = []
        while not routing.IsEnd(index):
            # plan_output += " {} -> ".format(manager.IndexToNode(index))
            vehicle_route.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        vehicle_route.append(manager.IndexToNode(index))
        # plan_output += "{}\n".format(manager.IndexToNode(index))
        # plan_output += "Distance of the route: {}m\n".format(route_distance)
        # print(plan_output)
        routes.append(vehicle_route)
        total_distances.append(route_distance)
        max_route_distance = max(route_distance, max_route_distance)
    # print("Maximum of the route distances: {}m".format(max_route_distance))
    return solution.ObjectiveValue(), max_route_distance, routes, total_distances


def ort(dist_mat, num_veh, depot):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(dist_mat, num_veh, depot)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing odel.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(data, manager, routing, solution)
    else:
        print("No solution found !")
        return None


if __name__ == "__main__":
    ort()
