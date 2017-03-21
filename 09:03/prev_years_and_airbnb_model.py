import numpy as np
import matplotlib.pyplot as plt
import pandas
import statsmodels.api as sm

# For 3d plots. This import is necessary to have 3D plotting below
from mpl_toolkits.mplot3d import Axes3D

# For statistics. Requires statsmodels 5.0 or more
from statsmodels.formula.api import ols
# Analysis of Variance (ANOVA) on linear models
from statsmodels.stats.anova import anova_lm

airbnb_on = True

def get_variables_from_maps(variables, msoa_order, year):
	variable = []
	for msoa_code in msoa_order:
		variable.append(float(variables[year][msoa_code]))
	return variable

# initialize the strctures holding data for variables in model
hp = {}
airbnb = {}
for year in range(1995,2017):
	hp[str(year)] = {}
	airbnb[str(year)] = {}

with open("year_msoacd_hpzscore.csv","r") as input_file:
	for text in input_file:
		for line in text.split('\r'):
			data = line.split(',')
			hp[data[0]][data[1]] = data[2]

with open("year_msoacd_airbnb.csv","r") as input_file:
	for line in input_file:
		data = line[:-1]
		data = data.split(',')
		airbnb[data[0]][data[1]] = data[2]

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

	# airbnb zscore
	X3 = get_variables_from_maps(airbnb, msoa_order, str(i))

	if airbnb_on:
		data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'x3' : X3, 'y': Y})
		model = ols("y ~ x1 + x2 + x3", data).fit()
	else:
		data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'y': Y})
		model = ols("y ~ x1 + x2", data).fit()

	# Print the summary
	print "model for year: " + str(i)
	print model.summary()
	print("*****************************************************************************************\n")