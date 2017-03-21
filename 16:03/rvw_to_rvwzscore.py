import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn import datasets, linear_model
import xlrd
import scipy

input_file_name = "year_msoa_reviewcount.csv"
output_file_name = "year_msoa_reviewzscore.csv"


year_msoacd_hp = {}

year_msoa_order = {}
for year in range(2009, 2017):
	year_msoa_order[str(year)] = []

year_price_order = {}
for year in range(2009, 2017):
	year_price_order[str(year)] = []

with open(input_file_name, 'r') as input_file:
	for line in input_file:
		if line[0] != '\n':
			data = line[:-1].split(',')
			if data[0] not in year_msoacd_hp:
				year_msoacd_hp[data[0]] = {}
			year_msoacd_hp[data[0]][data[1]] = data[2]

			year_msoa_order[data[0]].append(data[1])
			year_price_order[data[0]].append(data[2])

# Transform data into normal distribution
new_y = {}
for year in range(2009, 2017):
	new_y[str(year)] = []

for y in year_price_order:

	logged_y = [math.log(float(x) + 10) for x in year_price_order[y]]

	(transformed_data, b) = scipy.stats.boxcox(logged_y)

	transformed_data = scipy.stats.zscore(transformed_data)
	new_y[y] = transformed_data

for y in new_y:
	plt.hist(new_y[y])
	plt.show()

with open(output_file_name, 'w') as output_file:
	output_buffer = ''
	for y in new_y:
		for i in range(len(new_y[y])):
			output_buffer += y
			output_buffer += ',' + year_msoa_order[y][i]
			output_buffer += ',' + str(new_y[y][i]) + '\n'
	output_file.write(output_buffer)











