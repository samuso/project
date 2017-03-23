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

counter = 0
years = [str(i) for i in range(2009,2017)]
reviews = {}
for year in years:
	reviews[year] = {}

with open("reviews.csv", 'r') as input_file:
	for line in input_file:
		if counter == 0:
			counter += 1
		else:
			data = line[:-1].split(',')
			identifier = data[0]
			date = data[1].split('-')[0]
			if identifier in reviews[date]:
				reviews[date][identifier] += 1
			else:
				reviews[date][identifier] = 1

id_to_msoa_map = {}
with open('airbnb_msoa', 'r') as input_file:
	for line in input_file:
		data = line[:-1].split(',')
		identifier = data[0]
		msoa = data[5]
		id_to_msoa_map[identifier] = msoa

msoa_list = []
with open('all_msoas', 'r') as infile:
	for line in infile:
		if len(line) > 10:
			msoa_list.append(line[:-1].split(':')[1])

msoa_to_review = {}
for year in years:
	msoa_to_review[year] = {}
	for msoa in msoa_list:
		msoa_to_review[year][msoa] = 0

for year in reviews:
	for identifier in reviews[year]:
		if identifier in id_to_msoa_map:
			msoa = id_to_msoa_map[identifier]
			if msoa in msoa_to_review[year]:
				msoa_to_review[year][msoa] += reviews[year][identifier]

# year, msoa, review --> output csv
with open('year_msoa_reviewcount.csv', 'w') as output_file:
	buff = ''
	for year in msoa_to_review:
		for msoa in msoa_to_review[year]:
			buff += year + ',' + msoa + ',' + str(msoa_to_review[year][msoa]) + '\n'
	output_file.write(buff)







