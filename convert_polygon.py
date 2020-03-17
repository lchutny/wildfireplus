def convert_polygon(fire_polygon):
    """Convert Coord ref system (CRS) from fire data (EPSG 3857) to map
    lat/long (EPSG 4326), polygon starts and ends on same point (to close it)

    Input: list containing tuples of x,y points in fire CRS that describe a polygon
    Output: list containing tuples of lat/long points that describe the polygon
    """
    from shapely import geometry
    import geopandas as gpd
    import numpy as np
    # create polygon
    poly = geometry.Polygon([(p[0], p[1]) for p in fire_polygon])

    #CRS
    src_crs = "EPSG:3857"
    dst_crs = "EPSG:4326"

    # Create Geo DataFrame
    gfp = gpd.GeoDataFrame(index=[0],crs=src_crs,geometry=[poly])

    # Convert CRS
    gfp2 = gfp.to_crs(dst_crs)

    # pull data from dataframe
    polyout = gfp2.iloc[0]['geometry']

    # create list of tuples, but longitude is first
    l = list(map(tuple,np.asarray(polyout.exterior.coords)))
    l = list(map(lambda m: (m[1],m[0]), l))

    return l
