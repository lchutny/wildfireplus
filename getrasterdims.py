def getrasterdims(geotif_filename):
    """Get the top left and resolution for pixels in an array
    given the tif coordinate reference system
    Input: geotiff path+filename
    Output: tuple of the x,y coordinate of top left and resolutions of pixel

    Example to find out which pixel a given x,y coordinate refers to:
    pixel_column = (x-left)/xres
    pixel_row = (y-top)/yres
    """

    import rasterio as rio

    with rio.open(geotif_filename) as tif:
        profile = tif.profile

    left = profile['transform'][2]
    top = profile['transform'][5]

    xres = prof['transform'][0]
    yres = prof['transform'][4]

    return ((left,top),(xres,yres))
