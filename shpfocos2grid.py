# encoding: utf-8

import sys

# Carrega a Biblioteca GDAL/OGR
try:
    from osgeo import gdal, ogr, osr
except:
    sys.exit("ERRO: Biblioteca GDAL/OGR não encontrada!")


try:
    import geopandas as gpd
except:
    sys.exit("ERRO: Biblioteca GeoPandas não encontrada!")

import numpy as np

from utils import *

os.chdir('/home/torvizz/pdi_adv/focos')

# definições básicas

vector_file = "/home/torvizz/pdi_adv/focos/focos-2016.shp"

vector_file_base_name = os.path.basename(vector_file)

layer_name = os.path.splitext(vector_file_base_name)[0]

output_file_dir = "/home/torvizz/pdi_adv/focos"

file_format = "GTiff"

spatial_extent = { 'xmin': -89.975, 'ymin': -59.975,
                   'xmax': -29.975, 'ymax': 10.025 }

spatial_resolution = { 'x': 0.05, 'y': 0.05 }

grid_dimensions = { 'cols': 1200, 'rows': 1400 }

sats = ['TERRA_M-M', 'TERRA_M-T', 'AQUA_M-T', 'AQUA_M-M' ]

driver = gdal.GetDriverByName(file_format)

if driver is None:
	sys.exit("Erro: não foi possível identificar o driver '{0}'.".format(out_file_format))


# abrindo shape via gdal para extração da projeção em wkt

shp_focos = ogr.Open(vector_file)

if shp_focos is None:
    sys.exit("Erro: não foi possível abrir o arquivo '{0}'.".format(vector_file))

layer_focos = shp_focos.GetLayer(layer_name)

# shp_focos = None

if layer_focos is None:
    sys.exit("Erro: não foi possível acessar a camada '{0}' no arquivo {1}!".format(layer_name, vector_file))

srs_focos = layer_focos.GetSpatialRef()

pj = srs_focos.ExportToWkt()

# layer_focos = None

# manipulação do shape via geopandas e matrizes de focos

fshp = gpd.read_file(vector_file)
fshp.set_index('timestamp',inplace=True)
fshp = fshp.sort_index()
gfshp = fshp.groupby('satelite')

TMM = gfshp.get_group(sats[0])
TMT = gfshp.get_group(sats[1])
AMT = gfshp.get_group(sats[2])
AMM = gfshp.get_group(sats[3])


satlist = [TMM,
TMT,
AMT,
AMM]

ts1 = ['2016/%02d' % m for m in range(1,13)]
ts2 = ts1[1:]+['2017/01']

matriz = np.zeros((4,12,grid_dimensions['rows'], grid_dimensions['cols']),np.int16)

from itertools import izip 

for sat, mtx in izip(satlist,matriz):
	for t1,t2,m in izip(ts1,ts2,mtx):
		locs = sat.loc[t1:t2,'geometry'].values
		for x in locs:
			col, row = Geo2Grid(x, grid_dimensions,
		                        spatial_resolution, spatial_extent)
			m[row, col] += 1 

# escrevendo as matrizes em geotiff

N1 = [0]*12+[1]*12+[2]*12+[3]*12
N2 = range(12)*4
satnames = [sats[0]]*12+[sats[1]]*12+[sats[2]]*12+[sats[3]]*12


for n1,n2,sn in izip(N1,N2,satnames):
	
	filename = '%s/grade_focos_%s_mes%02d' % (output_file_dir, sn, (n2+1))
	
	
	raster = driver.Create(filename, grid_dimensions['cols'],
							grid_dimensions['rows'], gdal.GDT_UInt16)
	
	if raster is None:
		sys.exit("Erro: não foi possível criar o arquivo '{0}'.".format(filename))
	
	raster.SetGeoTransform((spatial_extent['xmin'], spatial_resolution['x'], 0,
								spatial_extent['ymax'], 0, -spatial_resolution['y']))
	
	raster.SetProjection(pj)
	
	band = raster.GetRasterBand(1)
	
	band.WriteArray(matriz[n1,n2], 0, 0)
	
	band.FlushCache()
	
	
	raster = None
	del raster, band
