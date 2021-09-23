import sys
sys.path.append(".")
sys.path.append("..")

import vrp
import requests

def test_coords():
    coords = [
        "-89.790945,35.053347",
        "-90.019375,35.094509",
        "-90.052027,35.14259",
        "-89.919783,35.103347",
        "-90.010188,35.138495",
        "-90.04027,35.13988",
        "-89.940793,35.122824",
        "-90.031549,35.116131",
        "-89.917591,35.106069",
        "-89.96206,35.116435",
        "-89.988856,35.15564",
        "-90.045273,35.155601",
        "-90.053361,35.148298",
        "-89.865175,35.09867",
        "-89.966336,35.155342",
        "-89.960472,35.159009",
    ]

    obj, max_route_dist, routes_coords, total_distances = vrp.find_routes(coords, 3, 0)
    assert obj == 6721589
    assert max_route_dist == 65376
    assert total_distances == [65376, 60977, 57636]

def test_server():
    with open('tests/coords.json', 'r') as f:
        d = f.read();

    response = requests.post(
        'http://192.168.1.8:8080/',
        headers = {'Content-type': 'application/json'},
        data=d
    )
    res = response.content.decode('utf-8')
    with open('tests/out.json', 'r') as f:
        o = f.read();
    assert res == o

