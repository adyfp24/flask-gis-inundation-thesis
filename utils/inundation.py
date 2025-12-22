# import rasterio
# import numpy as np
# import geopandas as gpd
# from rasterio.merge import merge
# from rasterio.features import shapes
# from shapely.geometry import shape

# DEM_FILES = [
#     "data/DEMNAS_1607-33_v1.0.tif",
#     "data/DEMNAS_1607-61_v1.0.tif"
# ]

# def generate_inundation_geojson(sea_level: float):
#     # 1. Baca & merge DEM
#     datasets = [rasterio.open(fp) for fp in DEM_FILES]
#     dem, transform = merge(datasets)
#     dem = dem[0]  # single band

#     # 2. Bathtub condition
#     inundated = dem <= sea_level

#     # 3. Raster → vector
#     results = []
#     for geom, val in shapes(inundated.astype(np.uint8), transform=transform):
#         if val == 1:
#             results.append(shape(geom))

#     # 4. GeoDataFrame
#     gdf = gpd.GeoDataFrame(geometry=results, crs=datasets[0].crs)

#     # optional: simplify
#     gdf["geometry"] = gdf["geometry"].simplify(0.0001)

#     return gdf.to_json()

import rasterio
import numpy as np
import geopandas as gpd
from rasterio.merge import merge
from rasterio.features import shapes
from rasterio.mask import mask
from shapely.geometry import shape, box
from scipy.ndimage import binary_dilation


# ===============================
# INPUT DATA
# ===============================
DEM_FILES = [
    "data/DEMNAS_1607-33_v1.0.tif",
    "data/DEMNAS_1607-61_v1.0.tif"
]

# AOI (HARUS SAMA DENGAN DATA SLA)
AOI_BOUNDS = {
    "west": 113.53192284124258,
    "east": 113.73236098432594,
    "south": -8.616956880254662,
    "north": -8.427068113123065,
}

# ===============================
# MAIN FUNCTION
# ===============================
def generate_inundation_geojson(sea_level: float):

    datasets = [rasterio.open(fp) for fp in DEM_FILES]
    dem_merged, transform = merge(datasets)
    dem_merged = dem_merged[0]

    meta = datasets[0].meta.copy()

    # AOI
    aoi_geom = box(
        AOI_BOUNDS["west"],
        AOI_BOUNDS["south"],
        AOI_BOUNDS["east"],
        AOI_BOUNDS["north"],
    )

    # Clip DEM
    with rasterio.io.MemoryFile() as memfile:
        with memfile.open(
            driver="GTiff",
            height=dem_merged.shape[0],
            width=dem_merged.shape[1],
            count=1,
            dtype=dem_merged.dtype,
            crs=meta["crs"],
            transform=transform,
        ) as tmp:
            tmp.write(dem_merged, 1)
            dem_clipped, clipped_transform = mask(tmp, [aoi_geom], crop=True)

    dem = dem_clipped[0]

    # =========================
    # BATHTUB LOGIC (FIXED)
    # =========================

    # 1️⃣ Kandidat genangan
    lowland = dem <= sea_level

    # 2️⃣ Laut sebagai seed
    sea = dem <= 0

    # 3️⃣ Flood-fill dari laut ke darat rendah
    inundated = sea.copy()
    for _ in range(50):  # iterasi cukup
        inundated = binary_dilation(inundated) & lowland

    # =========================
    # Raster → Vector
    # =========================

    results = []
    for geom, val in shapes(inundated.astype(np.uint8),
                            transform=clipped_transform):
        if val == 1:
            results.append(shape(geom))

    gdf = gpd.GeoDataFrame(geometry=results, crs=meta["crs"])
    gdf["geometry"] = gdf["geometry"].simplify(0.0001, preserve_topology=True)

    return gdf.to_json()