from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import vrp

app = Flask(__name__)
cors = CORS(app)

@app.route("/", methods=("GET", "POST"))
@cross_origin(origin='*')
def index():
    if request.method == "POST":
        coordinates = request.json["coordinates"]
        num_veh = request.json["number_of_vehicles"]
        depot = request.json["depot"]
        obj, max_route_dist, routes_coords, total_distances = vrp.find_routes(
            coordinates, num_veh, depot
        )
        response = jsonify(
            objective=obj,
            max_route_dist=max_route_dist,
            routes_coords=routes_coords,
            total_distances=total_distances,
        )
        # response.header.add('Access-Control-Allow-Origin', '*')
        return response

    else:
        return "Do POST Request"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
