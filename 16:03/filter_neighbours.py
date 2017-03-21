all_msoas = []
with open('all_msoas', 'r') as input_file:
	for line in input_file:
		code = line[:-1].split(':')[1]
		all_msoas.append(code)

neighbours = {}
with open('msoa_neighbours.csv', 'r') as input_file:
	for line in input_file:
		data = line[:-1].split(',')
		msoa = data[0]
		if msoa in all_msoas:
			neighbours[msoa] = [x for x in data[1:] if x in all_msoas]

buff = ''
with open('filtered_msoa_to_neighbours.csv', 'w') as output_file:
	for msoa in neighbours:
		buff+= msoa + ','
		for msoa_neighbour in neighbours[msoa]:
			buff += msoa_neighbour + ','
		buff = buff[:-1]
		buff += '\n'
	output_file.write(buff)