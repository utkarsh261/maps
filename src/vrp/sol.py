from vrp.dist_mat import *
from vrp.ort import *


def find_routes(coords, num_veh, depot):
    mat = dist_mat(coords)
    obj, max_route_dist, routes, total_distances = ort(mat, num_veh, depot)
    routes_coords = [[coords[i] for i in r] for r in routes]
    return obj, max_route_dist, routes_coords, total_distances
