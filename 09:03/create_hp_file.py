import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn import datasets, linear_model
import xlrd
path2Book = '/Users/Samusof/Desktop/Data I currently Have/avg_qrtr_house_prc_msoa/house_price.xls'
sheet_number = 4
london_las = ['City of London', 'Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley', 'Camden', 'Croydon', 'Ealing', 'Enfield', 'Greenwich', 'Hackney', 'Hammersmith and Fulham', 'Haringey', 'Harrow', 'Havering', 'Hillingdon', 'Hounslow', 'Islington', 'Islington', 'Kingston upon Thames', 'Kensington and Chelsea', 'Lambeth', 'Lewisham', 'Merton', 'Newham', 'Redbridge', 'Richmond upon Thames', 'Southwark', 'Sutton', 'Tower Hamlets', 'Waltham Forest', 'Wandsworth', 'Westminster']

def get_data_from_row(row):
	counter = 0
	la_code = ''
	la_name = ''
	msoa_code = ''
	msoa_name = ''
	avrg_house_price = []
	for cell in row:
		counter += 1
		if counter == 88:
			break
		elif counter == 1:
			la_code = cell.value
		elif counter == 2:
			la_name = cell.value
		elif counter == 3:
			msoa_code = cell.value
		elif counter == 4:
			msoa_name = cell.value
		else:
			try:
				avrg_house_price.append(int(float(cell.value)))
			except ValueError:
				avrg_house_price.append(-1)
			
	return {'la_code':la_code,
			'la_name':la_name,
			'msoa_code':msoa_code,
			'msoa_name':msoa_name,
			'avrg_house_price':avrg_house_price
			}

def extract_data_from_file(path, sheet_number):
	data = []
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(sheet_number)
	for i in range(6, sheet.nrows):
		row = sheet.row(i)
		data.append(get_data_from_row(row))
	return data

def get_yearly_house_price(data, year):
	msoa_to_price_map = {}
	for msoa in data:
		avrg_hp =  msoa['avrg_house_price'][year - 1995]
		msoa_code =  msoa['msoa_code']
		msoa_to_price_map[msoa_code] = avrg_hp
	return msoa_to_price_map

def filter_data(data):
	filtered_data = []
	for point in data:
		if point['la_name'] in london_las:
			filtered_data.append(point)
	return filtered_data

def change_date_format(data):
	for point in data:
		new_avrgs = []
		new_avrgs.append(point['avrg_house_price'][0])
		for i in range(0,20):
			a = sum([point['avrg_house_price'][j] 
					for j in range(i*4 + 1, i*4 + 5)])/4
			new_avrgs.append(a)
		new_avrgs.append((point['avrg_house_price'][81]+point['avrg_house_price'][82])/2)
		point['avrg_house_price'] = new_avrgs

raw_data = extract_data_from_file(path2Book, sheet_number)
data = filter_data(raw_data)
# change format to yearly instead of quarterly
change_date_format(data)

year = 2012
year_gap_for_x2 = 4

with open('year_msoacd_hp.csv', 'w') as output_file:
	output_buffer = ''
	for year in range(1995, 2017):
		yearly_house_price = get_yearly_house_price(data, year - 1)
		print yearly_house_price
		for key in yearly_house_price:
			output_buffer += str(year) + ',' + key + ','
			output_buffer += str(yearly_house_price[key])
			output_buffer += '\n'
	output_file.write(output_buffer)












