import ee

BASELINE_YEAR = 2025

def generate_inundation_tile(year: int, subsidence_rate_mm: float):

    slr_table = ee.FeatureCollection(
        'users/adyfp24/sea_level_rise_annual_2025_2050'
    )

    nasadem = ee.Image('NASA/NASADEM_HGT/001')
    elevation = nasadem.select('elevation')
    land_elevation = elevation.updateMask(elevation.gt(0))

    feature = slr_table.filter(
        ee.Filter.eq('year', year)
    ).first()

    slr = ee.Number(feature.get('cumulative_rise_mm')).divide(1000)

    subsidence = (
        ee.Number(year)
        .subtract(BASELINE_YEAR)
        .multiply(subsidence_rate_mm)
        .divide(1000)  # mm → meter
    )

    total_rslr = slr.add(subsidence)

    inundation = (
        land_elevation
        .lte(total_rslr)
        .selfMask()
        .visualize(
            palette=['0000FF'],
            opacity=0.6
        )
    )

    map_id = inundation.getMapId()
    return map_id["tile_fetcher"].url_format
