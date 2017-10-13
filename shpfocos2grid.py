# encoding: utf-8

os.chdir('/home/torvizz/pdi_adv/focos')

from utils import *

# # definições básicas

# vector_file = "/home/torvizz/pdi_adv/focos/focos-2016.shp"

# vector_file_base_name = os.path.basename(vector_file)

# layer_name = os.path.splitext(vector_file_base_name)[0]

# output_file_dir = "/home/torvizz/pdi_adv/focos"

# file_format = "GTiff"

# spatial_extent = { 'xmin': -89.975, 'ymin': -59.975,
#                    'xmax': -29.975, 'ymax': 10.025 }

# spatial_resolution = { 'x': 0.05, 'y': 0.05 }

# grid_dimensions = { 'cols': 1200, 'rows': 1400 }

# sats = ['TERRA_M-M', 'TERRA_M-T', 'AQUA_M-T', 'AQUA_M-M' ]

# # abrindo shape via gdal para extração da projeção em wkt

# shp_focos = ogr.Open(vector_file)

# if shp_focos is None:
#     sys.exit("Erro: não foi possível abrir o arquivo '{0}'.".format(vector_file))

# layer_focos = shp_focos.GetLayer(layer_name)

# # shp_focos = None

# if layer_focos is None:
#     sys.exit("Erro: não foi possível acessar a camada '{0}' no arquivo {1}!".format(layer_name, vector_file))

# srs_focos = layer_focos.GetSpatialRef()

# # layer_focos = None

# # manipulação do shape via geopandas e matrizes de focos

# fshp = gpd.read_file(vector_file)
# fshp.set_index('timestamp',inplace=True)
# fshp = fshp.sort_index()
# gfshp = fshp.groupby('satelite')

# TMM = gfshp.get_group(sats[0])
# TMT = gfshp.get_group(sats[1])
# AMT = gfshp.get_group(sats[2])
# AMM = gfshp.get_group(sats[3])


# satlist = [TMM,
# TMT,
# AMT,
# AMM]

# ts1 = ['2016/%02d' % m for m in range(1,13)]
# ts2 = ts1[1:]+['2017/01']

# matriz = np.zeros((4,12,grid_dimensions['rows'], grid_dimensions['cols']),np.int16)

# for sat, mtx in izip(satlist,matriz):
# 	for t1,t2,m in izip(ts1,ts2,mtx):
# 		locs = sat.loc[t1:t2,'geometry'].values
# 		for x in locs:
# 			col, row = Geo2Grid(x, grid_dimensions,
# 		                        spatial_resolution, spatial_extent)
# 			m[row, col] += 1 

# # escrevendo as matrizes em geotiff

# N1 = [0]*12+[1]*12+[2]*12+[3]*12
# N2 = range(12)*4
# satnames = [sats[0]]*12+[sats[1]]*12+[sats[2]]*12+[sats[3]]*12


for n1,n2,sn in izip(N1,N2,satnames):
	filename = '%s/grade_focos_%s_mes%02d' % (output_file_dir, sn, (n2+1))
	array2gtif(matriz[n1,n2], grid_dimensions, spatial_extent, spatial_resolution,
				srs_focos, file_format, filename)
