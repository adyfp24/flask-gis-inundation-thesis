from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.gee import init_gee

# INIT GEE SEKALI SAAT START
init_gee()

from utils.inundation import generate_inundation_tile
from utils.elevation import generate_elevation_tile
from utils.slr import get_slr_by_year, get_slr_timeseries

app = Flask(__name__)
CORS(app)

# ======================
# MAP: ELEVATION
# ======================
@app.route("/api/map/elevation")
def elevation_map():
    tile_url = generate_elevation_tile()
    return jsonify({
        "type": "elevation",
        "tile_url": tile_url
    })

# ======================
# MAP: INUNDATION (DINAMIS)
# ======================
@app.route("/api/map/inundation")
def inundation_map():
    year = int(request.args.get("year"))
    subsidence_rate_mm = float(
        request.args.get("subsidence_rate_mm", 300)  # default 300 mm/tahun
    )

    tile_url = generate_inundation_tile(
        year=year,
        subsidence_rate_mm=subsidence_rate_mm
    )

    return jsonify({
        "year": year,
        "subsidence_rate_mm": subsidence_rate_mm,
        "type": "inundation",
        "tile_url": tile_url
    })


# ======================
# SLR (PUNYA KAMU)
# ======================
@app.route("/api/slr")
def slr():
    year = int(request.args.get("year"))
    slr_value = get_slr_by_year(year)
    return jsonify({"year": year, "slr_m": slr_value})

@app.route("/api/slr/timeseries")
def slr_timeseries():
    return jsonify(get_slr_timeseries())

if __name__ == "__main__":
    app.run(debug=True)
