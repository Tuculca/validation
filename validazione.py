import sys
import numpy
import pandas
import hashlib
import datetime

### INPUT FROM TERMINAL ###
date = sys.argv[1] #esempio 2022/08/17
### DATE FOR OUTPUT FILENAME ###
date_for_filename = datetime.datetime.strptime(date,"%Y/%m/%d").strftime("%d%m%Y")
### READ CSV ###
obs = pandas.read_csv('exportData.csv')
len_obs_extracted = len(obs)
### RENAME COLUMNS TO REMOVE SPECIAL CHARACTERS ###
obs = obs.rename(columns={'CUMULATED 3 hours':'CUMULATED_3_hours'})
obs = obs.rename(columns={'DATE/TIME':'DATE_TIME'})
### BUILD ARRAYS FOR EACH HOUR TIME ###
datetime_firstday = datetime.datetime.strptime(date, "%Y/%m/%d")
datetime_previous = datetime_firstday + datetime.timedelta(-1)
datetime_followin = datetime_firstday + datetime.timedelta(1)
date_previous = datetime_previous.strftime("%Y/%m/%d")
date_followin = datetime_followin.strftime("%Y/%m/%d")
obs_m9 = obs[obs.DATE_TIME == date_previous + ' 15.00']
obs_m6 = obs[obs.DATE_TIME == date_previous + ' 18.00']
obs_m3 = obs[obs.DATE_TIME == date_previous + ' 21.00']
obs_00 = obs[obs.DATE_TIME == date + ' 00.00']
obs_03 = obs[obs.DATE_TIME == date + ' 03.00']
obs_06 = obs[obs.DATE_TIME == date + ' 06.00']
obs_09 = obs[obs.DATE_TIME == date + ' 09.00']
obs_12 = obs[obs.DATE_TIME == date + ' 12.00']
obs_15 = obs[obs.DATE_TIME == date + ' 15.00']
obs_18 = obs[obs.DATE_TIME == date + ' 18.00']
obs_21 = obs[obs.DATE_TIME == date + ' 21.00']
len_obs_singleH = len(obs_00)

obs_acc6h_00 = numpy.array(obs_m3)[:,10] + numpy.array(obs_00)[:,10]
obs_acc6h_03 = numpy.array(obs_00)[:,10] + numpy.array(obs_03)[:,10]
obs_acc6h_06 = numpy.array(obs_03)[:,10] + numpy.array(obs_06)[:,10]
obs_acc6h_09 = numpy.array(obs_06)[:,10] + numpy.array(obs_09)[:,10]
obs_acc6h_12 = numpy.array(obs_09)[:,10] + numpy.array(obs_12)[:,10]
obs_acc6h_15 = numpy.array(obs_12)[:,10] + numpy.array(obs_15)[:,10]
obs_acc6h_18 = numpy.array(obs_15)[:,10] + numpy.array(obs_18)[:,10]
obs_acc6h_21 = numpy.array(obs_18)[:,10] + numpy.array(obs_21)[:,10]
obs_list_6h = [[obs_00, obs_acc6h_00], [obs_03, obs_acc6h_03], [obs_06, obs_acc6h_06], [obs_09, obs_acc6h_09], [obs_12, obs_acc6h_12], [obs_15, obs_acc6h_15], [obs_18, obs_acc6h_18], [obs_21, obs_acc6h_21]]

obs_acc12h_00 = numpy.array(obs_m9)[:,10] + numpy.array(obs_m6)[:,10] + numpy.array(obs_m3)[:,10] + numpy.array(obs_00)[:,10]
obs_acc12h_06 = numpy.array(obs_m3)[:,10] + numpy.array(obs_00)[:,10] + numpy.array(obs_03)[:,10] + numpy.array(obs_06)[:,10]
obs_acc12h_12 = numpy.array(obs_03)[:,10] + numpy.array(obs_06)[:,10] + numpy.array(obs_09)[:,10] + numpy.array(obs_12)[:,10]
obs_acc12h_18 = numpy.array(obs_09)[:,10] + numpy.array(obs_12)[:,10] + numpy.array(obs_15)[:,10] + numpy.array(obs_18)[:,10]
obs_list_12h = [[obs_00, obs_acc6h_00], [obs_06, obs_acc6h_06], [obs_12, obs_acc6h_12], [obs_18, obs_acc6h_18]] #errore?

#obs = obs[obs.CUMULATED_3_hours != -9998.0]
#obs = obs[obs.DATE_TIME == date + ' ' + ora]
stazioni = dict([(y, x) for x, y in list(enumerate(sorted(set(obs['STATION']))))])


with open('PLUVIO_acc6h_' + date_for_filename + '.txt', 'w') as f:
	for obsX in obs_list_6h:
		obs = obsX[0].copy()
		obs['CUMULATED_3_hours'] = obsX[1]
		obs = obs[obs.CUMULATED_3_hours > -1000]
		for j in range(len_obs_singleH):
			try:
				f.write('ADPSFC ' + \
				"{0:>4}".format(str(stazioni[obs['STATION'][j]])) + ' ' + \
				datetime.datetime.strptime(obs['DATE_TIME'][j],"%Y/%m/%d %H.%M").strftime("%Y%m%d_%H%M%S") + '   ' + \
				"{0:>5}".format(str("%.2f" % obs['LAT'][j])) + '   ' + \
				"{0:>5}".format(str("%.2f" % obs['LON'][j])) + \
				" -9999.00 61 12 -9999.00 NA   " + \
				"{0:>4}".format(str("%.2f" % obs['CUMULATED_3_hours'][j])) + '\n') 
			except KeyError:
				pass
				
with open('PLUVIO_acc12h_' + date_for_filename + '.txt', 'w') as f:
	for obsX in obs_list_12h:
		obs = obsX[0].copy()
		obs['CUMULATED_3_hours'] = obsX[1]
		obs = obs[obs.CUMULATED_3_hours > -1000]
		for j in range(len_obs_singleH):
			try:
				f.write('ADPSFC ' + \
				"{0:>4}".format(str(stazioni[obs['STATION'][j]])) + ' ' + \
				datetime.datetime.strptime(obs['DATE_TIME'][j],"%Y/%m/%d %H.%M").strftime("%Y%m%d_%H%M%S") + '   ' + \
				"{0:>5}".format(str("%.2f" % obs['LAT'][j])) + '   ' + \
				"{0:>5}".format(str("%.2f" % obs['LON'][j])) + \
				" -9999.00 61 12 -9999.00 NA   " + \
				"{0:>4}".format(str("%.2f" % obs['CUMULATED_3_hours'][j])) + '\n') 
			except KeyError:
				pass
