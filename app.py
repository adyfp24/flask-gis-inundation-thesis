# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.inundation import generate_inundation_geojson
from utils.slr import get_slr_by_year

app = Flask(__name__)
CORS(app)

@app.route("/api/slr")
def slr():
    year = int(request.args.get("year"))
    slr_value = get_slr_by_year(year)
    return jsonify({
        "year": year,
        "slr_m": slr_value
    })


@app.route("/api/inundation")
def inundation():
    year = int(request.args.get("year"))
    slr_value = get_slr_by_year(year)

    geojson = generate_inundation_geojson(slr_value)
    return geojson


if __name__ == "__main__":
    app.run(debug=True)
