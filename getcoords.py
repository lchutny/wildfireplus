def getcoords(geotif,pixelrow,pixelcol):
    """Get the coordinates of a given pixel in the tif coordinate
    system
    Input: geotiff path+filename, and row,column of the pixel in question
    Output: tuple of the x,y coordinate in the geotif coordinate system
    """

    import rasterio as rio

    with rio.open(geotif) as tif:
        profile = tif.profile

    left = profile['transform'][2]
    top = profile['transform'][5]

    xres = prof['transform'][0]
    yres = prof['transform'][4]

    deltax = xres*pixelcol
    deltay = yres*pixelrow

    x = left+deltax
    y = top+deltay

    return (x,y)
