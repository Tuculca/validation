import pandas
import numpy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
import scipy.interpolate
import cartopy.crs as crs
from netCDF4 import Dataset
import wrf


def plot(fileInput):
	Nlons = 470 #377
	Nlats = 420 #429
	data='2019/07/10 15.00'
	obs = pandas.read_csv(fileInput)
	obs = obs.rename(columns={'DATE/TIME':'DATE_TIME'})
	obs_15 = obs[(obs['DATE_TIME'] == data)]
	obs_15 = obs_15.drop(obs_15[obs_15.VALUE < -5].index)
	obs_15 = obs_15.drop(obs_15[obs_15.VALUE > 45].index)
	obs_15 = obs_15.drop(obs_15[obs_15.LAT < 40.1].index)
	obs_15 = obs_15.drop(obs_15[obs_15.LAT > 42.9].index)
	obs_15 = obs_15.drop(obs_15[obs_15.LON < 11.3].index)
	obs_15 = obs_15.drop(obs_15[obs_15.LON > 16.9].index)
	lats_15 = numpy.array(obs_15['LAT'])
	lons_15 = numpy.array(obs_15['LON'])
	values_15 = numpy.array(obs_15['VALUE'])
	#values_15[values_15<0]=numpy.nan
	print("Max observed value: " + str(values_15.max()))
	print("Min observed value: " + str(values_15.min()))
	#plt.scatter(lons_15, lats_15, s=0.2, c=values_15, cmap='rainbow')
	#plt.colorbar()
	#plt.savefig('TempDewetra.jpg')
	#plt.clf()
	
	file_nc = Dataset('griglia_wrf_1km.nc')
	grid_lons, grid_lats = file_nc['XLONG'][0], file_nc['XLAT'][0]
	#landmask = wrf.getvar(file_nc, 'LANDMASK')
	#grid_lons, grid_lats = grid_lons*landmask, grid_lats*landmask
	#grid_lons[grid_lons==0]=numpy.nan
	#grid_lats[grid_lats==0]=numpy.nan
	#print(grid_lons)
	#print(grid_lons.shape)
	
	#grid_lons2 = numpy.linspace(lons_15.min(),lons_15.max(), Nlons) #prenderle direttamente dal netcdf
	#grid_lats2 = numpy.linspace(lats_15.min(),lats_15.max(), Nlats)
	#grid_lons2, grid_lats2 = numpy.meshgrid(grid_lons2, grid_lats2)
	#print("2:")
	#print(grid_lons2)
	#print(grid_lons2.shape)
	
	for i in range(len(lats_15)):
		coords = wrf.ll_to_xy(file_nc, lats_15[i], lons_15[i])
		height = file_nc['HGT'][0][coords.values[1]][coords.values[0]]
		values_15[i] = values_15[i] + (((height)/100)*0.9)
	
	grid_lons_r = grid_lons.reshape(1, Nlats*Nlons)
	grid_lats_r = grid_lats.reshape(1, Nlats*Nlons)
	for i in range(len(grid_lats_r[0])):
		if grid_lats_r[0][i]>42 and grid_lons_r[0][i]>15:
			grid_lats_r[0][i] = numpy.nan
			grid_lons_r[0][i] = numpy.nan
	xobs=numpy.stack((lons_15, lats_15), axis=-1)
	xflat=numpy.array((grid_lons_r[0], grid_lats_r[0])).T
	grid_values = scipy.interpolate.RBFInterpolator(xobs, values_15,kernel='gaussian', epsilon=1, smoothing=0.1)(xflat)
	grid_values = grid_values.reshape(Nlats,Nlons)
	#Xs = numpy.linspace(lons_15.min(),lons_15.max(), Nlons)
	#Ys = numpy.linspace(lats_15.min(),lats_15.max(), Nlats)
	

	cmap = plt.cm.jet
	cmap = colors.LinearSegmentedColormap.from_list('trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=0.40, b=1), cmap(numpy.linspace(0.40, 1, 10)))
	norm = colors.BoundaryNorm(numpy.arange(15, 43.5, 1.5), cmap.N)
	
	heights = wrf.getvar(file_nc, 'HGT')
	grid_values = grid_values - ((heights/100)*0.9) 
	print("Max interpolated value: " + str(grid_values.values.max()))
	print("Min interpolated value: " + str(grid_values.values.min()))
	
	
	fig = plt.figure()
	get_var = wrf.getvar(file_nc, 'XLONG')
	cart_proj = wrf.get_cartopy(get_var)
	landmask = wrf.getvar(file_nc, 'LANDMASK')
	grid_values = landmask*grid_values
	for i in grid_values:
		i[i==0]=numpy.nan
	
	ax = fig.add_subplot(projection=cart_proj)
	#plt.contourf(Xs, Ys, grid_values, cmap=cmap, norm=norm, levels=10)
	cs = ax.contourf(grid_lons, grid_lats, grid_values, cmap=cmap, norm=norm, levels=20, transform=crs.PlateCarree())
	cbar = fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm))
	cbar.set_label("°C", rotation=0)
	font3 = {'family':'serif','color':'black','size':12}
	plt.title(data, fontdict=font3)
	#ax.clabel(cs, inline=True, fontsize=10, colors='black')
	#plt.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm))
	plt.xlim([-250000, 219000])
	plt.ylim([-220000, 200000])
	plt.show()
	#plt.savefig('TempRBF.jpg')
	
	
plot('temp2.csv')
