# encoding: utf-8

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

os.chdir('/home/torvizz/pdi_adv')

focos_vector_file = "focos/focos-2016.shp"

fshp = gpd.read_file(focos_vector_file)

fshp["timestamp"] = pd.to_datetime(fshp["timestamp"])

fshp_toc09 = fshp[(fshp.estado=='Tocantins') & (fshp.timestamp>='2016-09-01') & (fshp.timestamp<'2016-10-01')]

mun_vector_file = "BR/BRMUE250GC_SIR.shp"

mun_shp = gpd.read_file(mun_vector_file)

mun_toc = mun_shp[mun_shp.CD_GEOCMU.str[:2] == '17']

toc_join = gpd.sjoin(fshp_toc09, mun_toc, how="right", op='intersects')

toc09_nf=toc_join.groupby('NM_MUNICIP').size()

toc09_nf = toc09_nf.to_frame(name="nfocos").reset_index()

toc09_nf_pormun = pd.merge(mun_toc,nfpm, on='NM_MUNICIP',how='right')

f, ax = plt.subplots(1)
nfpms.plot(ax=ax, column='nfocos', scheme='fisher_jenks',k=10, legend=True)# cmap='Reds',
ax.set_title(u'Número de focos de queimada por município')
ax.set_xlim([-52,-42])



	