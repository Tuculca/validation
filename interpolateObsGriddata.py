import pandas
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.interpolate
import cartopy.crs as crs
from netCDF4 import Dataset
import wrf
import cartopy.io.shapereader as shpreader
	
def plot(fileInput):
	Nlons= 339 #377
	Nlats= 318 #429
	obs = pandas.read_csv(fileInput)
	obs = obs.rename(columns={'DATE/TIME':'DATE_TIME'})
	obs = obs.rename(columns={'CUMULATED 3 hours':'CUMULATED_3_hours'})
	obs_15 = obs[(obs['DATE_TIME'] == '2022/09/15 18.00')]
	obs_15 = obs_15.drop(obs_15[obs_15.CUMULATED_3_hours < 0].index)
	lats_15 = numpy.array(obs_15['LAT'])
	lons_15 = numpy.array(obs_15['LON'])
	values_15 = numpy.array(obs_15['CUMULATED_3_hours'])
	print("Max value: " + str(values_15.max()))
	print("Min value: " + str(values_15.min()))
	#plt.scatter(lons_15, lats_15, s=values_15, c=values_15, cmap='rainbow')
	#plt.colorbar()
	#plt.savefig('Rain.jpg')
	#plt.clf()
	
	file_nc = Dataset('wrfout_d01_2022-09-15_18')
	grid_lons, grid_lats = file_nc['XLONG'][0], file_nc['XLAT'][0]
	
	#grid_lons = numpy.linspace(lons_15.min(),lons_15.max(), Nlons) #prenderle direttamente dal netcdf
	#grid_lats = numpy.linspace(lats_15.min(),lats_15.max(), Nlats) #
	#grid_lons, grid_lats = numpy.meshgrid(grid_lons, grid_lats)
	grid_values = scipy.interpolate.griddata((lons_15,lats_15), values_15, (grid_lons,grid_lats), fill_value=0, method='cubic')
	
	get_var = wrf.getvar(file_nc, 'XLONG')
	landmask = wrf.getvar(file_nc, 'LANDMASK')
	grid_values = landmask*grid_values
	for i in grid_values:
		i[i==0]=numpy.nan
	
	colours=['#d2fffe', '#88fefd', '#00c6ff', '#1996ff', '#3c41ff', '#3cbc3d', '#a5d71f', '#ffe600', '#ffc300', '#ff7d00', '#ff0000', '#c80000', '#d464c3', '#b5199d', '#840094', '#dcdcdc', '#b4b4b4', '#8c8c8c', '#5a5a5a']
	cmap = (mpl.colors.ListedColormap(colours).with_extremes(over='black', under='white'))
	bounds = [0.2,1,3,5,7,10,15,20,25,30,40,50,60,70,80,100,125,150,175,200]
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	
	fig = plt.figure(dpi=120)
	ax = fig.add_subplot(projection=crs.PlateCarree())
	
	bounds_with_extremes = [0,0.2,1,3,5,7,10,15,20,25,30,40,50,60,70,80,100,125,150,175,200,1000]
	ax.contourf(grid_lons, grid_lats, grid_values, levels=bounds_with_extremes, cmap=cmap, norm=norm)
	
	fname = 'C:/Users/Aless/Downloads/gadm41_ITA_shp/gadm41_ITA_1.shp'
	adm1_shapes = list(shpreader.Reader(fname).geometries())
	ax.add_geometries(adm1_shapes, crs.PlateCarree(), edgecolor='black', facecolor='white', alpha=0.15, zorder=3)
	
	fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm), extend='both', 
	extendfrac='auto',
	ticks=bounds,
	spacing='uniform')
	plt.show()
	
	
	
plot('rainDewetraMarche.csv')
