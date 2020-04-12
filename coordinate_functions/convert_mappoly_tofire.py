def poly_to_fire(longs,lats):
    """Convert the longitude/latitude polygon from Mapbox input
    to Fire CRS (EPSG 3857)
    Input: List of Longitudes and Latitudes that form a polygon
    Output: List of (X,Y) tuples defining polygon on the fire CRS
    """

    import geopandas as gpd
    import rasterio as rio
    from shapely.geometry import Polygon
    # Define CRSs
    poly_crs = "epsg:4326" # Long/Lat from map
    fire_crs = "epsg:3857"

    # Create polygon and put in GDF
    poly_poly = Polygon(zip(longs,lats))
    poly_gdf = gpd.GeoDataFrame(index=[0],crs=poly_crs,geometry = [poly_poly])

    #Transform the gdf crs
    outgdf = poly_gdf.to_crs(fire_crs)

    # pull data from dataframe
    polyout = outgdf.iloc[0]['geometry']

    # create list of tuples of x,y
    l = list(map(tuple,np.asarray(polyout.exterior.coords)))

    return l
