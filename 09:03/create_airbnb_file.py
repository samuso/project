import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
from scipy import stats

filename = 'airbnb_msoa'

def my_hist(data, n):
	plt.hist(data, n)
	plt.show()
	
def my_plot(data):
	plt.plot(data)
	plt.show()

msoa_cd_nm_map = {}
with open('all_msoas', 'r') as infile:
	for line in infile:
		if len(line) > 10:
			line.replace('\n','')
			msoa_nm = line.split(':')[0]
			msoa_cd = line.split(':')[1]
			msoa_cd_nm_map[msoa_cd[:-1]] = msoa_nm

years = ['11','12','13','14','15','16']
all_years = {}
for i in range(len(years)):
	all_years[years[i]] = {}
	for code in msoa_cd_nm_map:
		all_years[years[i]][code] = 0

with open(filename) as infile:
	for line in infile:
		data = line[:-1].split(',')
		if data[5] in all_years[data[3]]:
			all_years[data[3]][data[5]] += 1

with open("year_msoacd_airbnb.csv", 'w') as output_file:
	for year in all_years:
		if int(year) > 13:
			my_data = []
			my_order = []
			for msoa_cd in all_years[year]:
				value = int(all_years[year][msoa_cd])
				my_data.append(float(value)*10 + 1)
				my_order.append(msoa_cd)

			my_data = [math.log(x + .1, 500000) for x in my_data]
			my_data = [np.log(x) for x in my_data]
			my_data = [np.log(x + 10) for x in my_data]
			my_data, _ = scipy.stats.boxcox([x + .5 for x in my_data])
			my_data = scipy.stats.zscore(my_data)

			my_hist(my_data, 6)

			for i in range(len(my_order)):
				buffer_str = '20' + year
				buffer_str += ',' + str(my_order[i])
				buffer_str += ',' + str(my_data[i])
				buffer_str += '\n'
				output_file.write(buffer_str)









