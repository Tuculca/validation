import pandas
import numpy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
import scipy.interpolate
import cartopy.crs as crs


def plot(fileInput):
	obs = pandas.read_csv(fileInput)
	obs = obs.rename(columns={'DATE/TIME':'DATE_TIME'})
	obs_hourly = obs[(obs['DATE_TIME'] == '2021/08/01 15.00')]
	obs_hourly = obs_hourly.drop(obs_hourly[obs_hourly.VALUE < -5].index)
	obs_hourly = obs_hourly.drop(obs_hourly[obs_hourly.VALUE > 45].index)
	lats_hourly = numpy.array(obs_hourly['LAT'])
	lons_hourly = numpy.array(obs_hourly['LON'])
	values_hourly = numpy.array(obs_hourly['VALUE'])
	#values_15[values_15<0]=numpy.nan
	print("Max value: " + str(values_hourly.max()))
	print("Min value: " + str(values_hourly.min()))
	plt.scatter(lons_hourly, lats_hourly, s=0.2, c=values_hourly, cmap='rainbow')
	plt.colorbar()
	plt.savefig('TempDewetra.jpg')
	plt.clf()
	grid_lons = numpy.linspace(lons_hourly.min(),lons_hourly.max(),377) #prenderle direttamente dal netcdf
	grid_lats = numpy.linspace(lats_hourly.min(),lats_hourly.max(),429)
	grid_lons, grid_lats = numpy.meshgrid(grid_lons, grid_lats)
	#grid_lons = grid_lons.reshape(1,377*429)
	#grid_lats = grid_lats.reshape(1,377*429)
	xobs=numpy.stack((lons_hourly, lats_hourly), axis=-1)
	xflat=numpy.array((grid_lons[0], grid_lats[0])).T
	#grid_values = scipy.interpolate.RBFInterpolator(xobs, values_hourly,kernel='inverse_quadratic', epsilon=20, smoothing=0.2)(xflat)
	grid_values = scipy.interpolate.griddata(xobs, values_hourly, (grid_lons, grid_lats), method='linear')
	grid_values = grid_values.reshape(429,377)
	Xs = numpy.linspace(lons_hourly.min(),lons_hourly.max(),377)
	Ys = numpy.linspace(lats_hourly.min(),lats_hourly.max(),429)
	
	cmap = plt.cm.rainbow
	norm = colors.BoundaryNorm(numpy.arange(0, 50, 2.5), cmap.N)
	
	plt.contourf(Xs, Ys, grid_values, cmap=cmap, norm=norm, levels=10)
	plt.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm))
	plt.show()
	#plt.savefig('TempGriddata.jpg')
	
	
	
plot('temp.csv')
