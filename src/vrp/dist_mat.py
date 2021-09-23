from __future__ import division
from __future__ import print_function
import requests
import json
import urllib

from decouple import config

API_KEY = config("API_KEY")


def create_data(coords):
    """Creates the data."""
    data = {}
    data["API_key"] = API_KEY
    # data["addresses"] = ["-122.42,37.78", "-122.45,37.91", "-122.48,37.73"]
    # with open('coordinates.txt', 'r') as f:
    #    l = f.read().splitlines()
    # print(l)
    data["addresses"] = coords
    return data


def create_distance_matrix(data):
    addresses = data["addresses"]
    API_key = data["API_key"]
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses)  # 16 in this example.
    # Maximum number of rows that can be computed per request (6 in this example).
    max_rows = max_elements // num_addresses
    # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []
    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = []
        for i in range(i * max_rows, (i + 1) * max_rows):
            origin_addresses.append(str(i))
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = []
        for i in range(q * max_rows, q * max_rows + r):
            origin_addresses.append(str(i))
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
    return distance_matrix


def send_request(origin_addresses, dest_addresses, API_key):
    """ Build and send request for the given origin and destination addresses."""

    def build_address_str(addresses):
        # Build a semicolon-separated string of addresses
        address_str = ""
        for i in range(len(addresses) - 1):
            address_str += addresses[i] + ";"
        address_str += addresses[-1]
        return address_str

    request = "https://api.mapbox.com/directions-matrix/v1/mapbox/driving/"
    origin_address_str = build_address_str(origin_addresses)
    dest_address_str = build_address_str(dest_addresses)
    request = (
        request
        + dest_address_str
        + "?sources="
        + origin_address_str
        + "&annotations=distance,duration"
        + "&destinations="
        + "all"
        + "&access_token="
        + API_key
    )
    # print("request: ", request)
    jsonResult = urllib.request.urlopen(request).read()
    response = json.loads(jsonResult)
    # print("response: ", response)
    return response


def build_distance_matrix(response):
    distance_matrix = []
    for row in response["distances"]:
        # print(row)
        # row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        row_list = row
        distance_matrix.append(row_list)
    return distance_matrix


def dist_mat(coords):
    """Entry point of the program"""
    # Create the data.
    data = create_data(coords)
    addresses = data["addresses"]
    API_key = data["API_key"]
    distance_matrix = create_distance_matrix(data)
    # print(distance_matrix)
    return distance_matrix


# if __name__ == "__main__":
#    dist_mat()
