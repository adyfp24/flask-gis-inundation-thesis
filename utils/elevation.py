import ee

def generate_elevation_tile():
    nasadem = ee.Image('NASA/NASADEM_HGT/001')
    elevation = nasadem.select('elevation')
    land = elevation.updateMask(elevation.gt(0))

    vis = land.visualize(
        min=0,
        max=2000,
        palette=[
            '006400','7FFF00','FFFF00',
            'FFA500','A52A2A','FFFFFF'
        ],
        opacity=0.9
    )

    return vis.getMapId()["tile_fetcher"].url_format
