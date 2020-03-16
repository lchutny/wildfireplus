def convert_point(lat,long):
    """Convert Coordinate Reference systems from map lat/long
    to fire raster CRS
    Input: Point of latitude,longitude
    Output: Tuple of (x,y) in CRS coordinates
    """

    import geopandas as gpd
    from shapely.geometry import Point

    # Declare point
    point = Point(lat,long)

    # Set Source CRS (Mapbox or Google Maps)
    src_crs = "EPSG:4326"

    # create dataframe from input lat/long
    gdf=gpd.GeoDataFrame(index=[0],crs = src_crs, geometry=[point])

    # Change CRS to match Wildfire CRS (3857)
    gdf_tf = gdf.to_crs("epsg:3857")

    # pull x and y value out from the POINT attribute, then get
    # the value in the data series at row[0]
    x = gdf_tf.geometry.x.at[0]
    y = gdf_tf.geometry.y.at[0]

    return (x,y)
