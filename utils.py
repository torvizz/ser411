# encoding: utf-8

# import sys

# Carrega a Biblioteca GDAL/OGR
# try:
#     from osgeo import gdal
# except:
#     sys.exit("ERRO: Biblioteca GDAL/OGR não encontrada!")


def Geo2Grid(location, dimensions, resolution, extent):
    """
    Converts a geographic coordinate position to a regular grid coordinate.
    Args:
        location (Geometry): A geometric point with coordinates X and Y.
        dimensions (dict): The number of columns and rows in the grid.
        resolution (dict): The spatial resolution along the X and Y coordinates.
        extent (dict): The spatial extent associated to the grid.
    Returns:
        (int, int): the grid column and row where the point lies in.
    """

    x = location.x
    y = location.y

    col = int( ( x - extent['xmin'] ) / resolution['x'])

    row = int ( dimensions['rows'] - (y - extent['ymin']) / resolution['y'] )

    return col, row


# def array2gtif(mat, grid_dim, extent, resolution, projct, out_file_format, out_file_name):
#     try:
#         from osgeo import gdal
#     except:
#         sys.exit("ERRO: Biblioteca GDAL/OGR não encontrada!")
    
#     driver = gdal.GetDriverByName(file_format)
    
#     if driver is None:
#         sys.exit("Erro: não foi possível identificar o driver '{0}'.".format(out_file_format))
    
#     raster = driver.Create(out_file_name,
#                            grid_dim['cols'], grid_dim['rows'],
#                            1, gdal.GDT_UInt16)
    
#     if raster is None:
#         sys.exit("Erro: não foi possível criar o arquivo '{0}'.".format(out_file_name))
    
#     raster.SetGeoTransform((extent['xmin'], resolution['x'], 0,
#                             extent['ymax'], 0, -resolution['y']))
    
#     # proj = layer_focos.GetSpatialRef()
    
#     raster.SetProjection(projct.ExportToWkt())
    
#     band = raster.GetRasterBand(1)
    
#     band.WriteArray(mat, 0, 0)
    
#     band.FlushCache()
    
    
    
#     raster = None
#     del raster, band

