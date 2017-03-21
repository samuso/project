import numpy as np
import matplotlib.pyplot as plt
import pandas
import statsmodels.api as sm
import scipy

# For 3d plots. This import is necessary to have 3D plotting below
from mpl_toolkits.mplot3d import Axes3D

# For statistics. Requires statsmodels 5.0 or more
from statsmodels.formula.api import ols
# Analysis of Variance (ANOVA) on linear models
from statsmodels.stats.anova import anova_lm

airbnb_on = True
airbnb_review_not_listing = True

def standardize_data(msoa_map, msoa_order):
	values = []
	for msoa in msoa_order:
		values.append(msoa_map[msoa])
	values = scipy.stats.zscore(values)
	new_msoa_map = {}
	counter = 0
	for msoa in msoa_order:
		new_msoa_map[msoa] = values[counter]
		counter += 1
	return new_msoa_map

def consider_neighbours(neighbours, variables, msoa_order, year):
	new_map = {}
	for msoa in msoa_order:
		new_map[msoa] = 0

	for msoa in variables[year]:
		for neighbour in neighbours[msoa]:
			new_map[msoa] += float(variables[year][neighbour])
		new_map[msoa] /= len(neighbours[msoa])

	variables[year] = standardize_data(new_map, msoa_order)
	return get_variables_from_maps(variables, msoa_order, year)

def get_variables_from_maps(variables, msoa_order, year):
	variable = []
	for msoa_code in msoa_order:
		variable.append(float(variables[year][msoa_code]))
	return variable

neighbours = {}
with open('filtered_msoa_to_neighbours.csv', 'r') as input_file:
	for line in input_file:
		data = line[:-1].split(',')
		msoa = data[0]
		neighbours[msoa] = [x for x in data[1:]]
			


# initialize the strctures holding data for variables in model
hp = {}
airbnb_house = {}
airbnb_room = {}
airbnb_review = {}
for year in range(1995,2017):
	hp[str(year)] = {}
	airbnb_house[str(year)] = {}
	airbnb_room[str(year)] = {}
	airbnb_review[str(year)] = {}

with open("year_msoacd_hpzscore.csv","r") as input_file:
	for text in input_file:
		for line in text.split('\r'):
			data = line.split(',')
			hp[data[0]][data[1]] = data[2]

with open("year_msoacd_airbnb_house.csv","r") as input_file:
	for line in input_file:
		data = line[:-1]
		data = data.split(',')
		airbnb_house[data[0]][data[1]] = data[2]

with open("year_msoacd_airbnb_room.csv","r") as input_file:
	for line in input_file:
		data = line[:-1]
		data = data.split(',')
		airbnb_room[data[0]][data[1]] = data[2]

with open("year_msoa_reviewzscore.csv","r") as input_file:
	for line in input_file:
		data = line[:-1]
		data = data.split(',')
		airbnb_review[data[0]][data[1]] = data[2]

msoa_order = [k for k in hp['2016']]

# number of previous years taken into model
prev_years = 1
for i in range(2014, 2017):
	Y = get_variables_from_maps(hp, msoa_order, str(i))

	# prev year
	X1 = get_variables_from_maps(hp, msoa_order, str(i - 1))

	# multiple prev years
	prices_zscores = [0.0 for x in msoa_order]
	for j in range(prev_years):
		list_to_add = get_variables_from_maps(hp, msoa_order, str(i-2-j))
		for k in range(len(prices_zscores)):
			prices_zscores[k] += list_to_add[k]
	X2 = [x/prev_years for x in prices_zscores]

	# airbnb zscore for rooms
	X3 = get_variables_from_maps(airbnb_review, msoa_order, str(i))

	# airbnb zscore for houses
	X4 = consider_neighbours(neighbours, hp, msoa_order, str(i))

	# airbnb review count zscore
	X5 = consider_neighbours(neighbours, airbnb_review, msoa_order, str(i))

	if airbnb_on:
		if airbnb_review_not_listing:
			# data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'x5' : X5, 'y': Y})
			# model = ols("y ~ x1 + x2 + x5", data).fit()

			data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'x3' : X3, 'x4' : X4, 'x5' : X5, 'y': Y})
			model = ols("y ~ x1 + x2 + x3 + x4 + x5", data).fit()

		else:
			data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'x3' : X3, 'x4' : X4, 'y': Y})
			model = ols("y ~ x1 + x2 + x3 + x4", data).fit()
	else:
		data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'y': Y})
		model = ols("y ~ x1 + x2", data).fit()

	# Print the summary
	print "model for year: " + str(i)
	print model.summary()
	print("*****************************************************************************************\n")