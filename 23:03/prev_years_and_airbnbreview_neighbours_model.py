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

from sklearn.linear_model import LogisticRegression
from sklearn import linear_model
from sklearn import svm
from sklearn.model_selection import cross_val_score

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

def create_variables_for_params(data):
	instances = [[] for x in data[0]]
	for param in data:
		for i in range(len(param)):
			instances[i].append(param[i])
	return instances

import statsmodels.formula.api as smf

def choose_params_from_int(X, n):
	param_count_range = range(len(X[0]) - 1)
	included = [False for x in X[0][1:]]
	remainder = n
	for i in param_count_range:
		included[i] = False if remainder % 2 == 0 else True
		remainder /= 2

	new_X = []
	for i in param_count_range:
		if included[i]:
			new_X.append([x[i+1] for x in X])
	print "this"
	print n
	print X
	print included

	return create_variables_for_params(new_X), included




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
prev_years = 3
for i in range(2016, 2017):
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

	# data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'x3' : X3, 'x4': X4, 'x5' : X5, 'y': Y})
	# model = ols("y ~ x1 + x2 + x3 + x4 + x5", data).fit()

	Xs = [X1,X2,X3,X4,X5]

	X = sm.add_constant(create_variables_for_params([X1,X2,X3,X4,X5]))
	print range(2 ** len(Xs))
	# for l in range(1,2 **len(Xs)):
	l = 2 **len(Xs) - 1
	if l > 0:
		print l
		final_X, included = choose_params_from_int(X, l)
		model = sm.OLS(Y,final_X)
		results = model.fit()
		print "\n\n\n\n\nmodel for year: " + str(i) + "param inclusion = "
		print included
		print results.summary()

		inted_x = []
		for x in final_X:
			inted_x.append([int(10000*e) for e in x])
		inted_y = [int(10000*e) for e in Y]
		# model1 = LogisticRegression(fit_intercept = False, C = 1e9)
		# mdl1 = model1.fit(inted_x,inted_y)

		# print mdl1
		# print model1.coef_

		
		scores = []
		Cs = [0, .002, .01, .02, .03, .1, .2, .3, .4, .5]
		for i in range(1,10001,1000):
			svr_rbf = svm.SVR(kernel='rbf', C=i)
			svr_rbf.fit(final_X,Y)
			s = svr_rbf.score(final_X,Y)
			print s
			scores.append(s)

		plt.plot(scores,range(1,10001,1000))
		plt.show()


		# reg = linear_model.Lasso(alpha =.00001)
		# reg.fit(final_X, Y)
		# print "sam"
		# print reg.score(final_X, Y)
	# if airbnb_on:
	# 	if airbnb_review_not_listing:
	# 		# data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'x5' : X5, 'y': Y})
	# 		# model = ols("y ~ x1 + x2 + x5", data).fit()

	# 		data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'x3' : X3, 'x4' : X4, 'x5' : X5, 'y': Y})
	# 		model = ols("y ~ x1 + x2 + x3 + x4 + x5", data).fit()

	# 	else:
	# 		data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'x3' : X3, 'x4' : X4, 'y': Y})
	# 		model = ols("y ~ x1 + x2 + x3 + x4", data).fit()
	# else:
	# 	data = pandas.DataFrame({'x1': X1, 'x2' : X2, 'y': Y})
	# 	model = ols("y ~ x1 + x2", data).fit()

	# Print the summary









