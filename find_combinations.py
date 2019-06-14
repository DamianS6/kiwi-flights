import sys
import csv
from datetime import datetime


def find_combinations():
	"""
	Find all combinations of flights for passengers with no bags,
	one bag or two bags are able to travel, having 1 to 4 hours
	for each transfer between flights.
	"""

	try:
		bags_num = int(sys.argv[-1])
	except ValueError:
		# Assume 0 bags if not provided.
		bags_num = 0
	if bags_num > 2:
		print("You cannot take more than 2 bags with you.")
		return

	lines = sys.stdin.readlines()
	reader = csv.reader(lines)

	# Create initial list with itineraries.
	initial = []
	for row in reader:
		if reader.line_num == 1:
			continue
		price = int(row[5]) + int(row[7])*bags_num
		if int(row[6]) >= bags_num:
			initial.append({'route': [row[0], row[1]],
			                'dep_time': row[2],
			                'arr_time': row[3],
			                'price': price})

	current_len = 2
	final = []
	# Set flag to control if program should stop or look for the next link.
	found_next_flight = True

	time_format = '%Y-%m-%dT%H:%M:%S'
	while found_next_flight:
		found_next_flight = False
		temp_list = []

		for item in initial:
			for line in lines:
				line = line.rstrip().split(',')
				if line[0] == 'source':
					continue

				# Set place condition (next source == last destination).
				place_cond = bool(line[0] == item['route'][current_len-1])
				# Set time condition.
				next_dep = datetime.strptime(line[2], time_format)
				last_arr = datetime.strptime(item['arr_time'], time_format)
				transfer = next_dep - last_arr
				time_cond = bool(3600 <= transfer.total_seconds() <= 4 * 3600)
				# Avoid travelling through same cities.
				repeat_cond = not bool(line[1] in item['route'][1:-1])

				if place_cond and time_cond and repeat_cond and int(line[6]) >= bags_num:
					# If next flight was found run the whole process once more.
					found_next_flight = True
					price = int(line[5]) + int(line[7]) * bags_num
					new_route = []
					for n in range(current_len):
						new_route.append(item['route'][n])
					new_route.append(line[1])
					temp_list.append({'route': new_route,
					                  'dep_time': item['dep_time'],
					                  'arr_time': line[3],
					                  'price': item['price'] + price})

		initial.extend(temp_list)

		# Make and work on copies to avoid doing extra loops - working
		# on originals doesn't delete mentioned below combinations at once.
		cinitial = initial[:]
		for item in initial:
			# Delete all combinations that don't go any further.
			if len(item['route']) == current_len:
				cinitial.remove(item)
		initial = cinitial[:]

		# Move finished combinations to final list.
		for item in initial:
			if item['route'][0] == item['route'][-1]:
				final.append(item)
				cinitial.remove(item)
		final.extend(cinitial)
		initial = cinitial

		current_len += 1

	print("For given amount of bags I have found the following flight combinations\n"
	      "(1 to 4 hours for each transfer between flights):\n")
	for item in final:
		print(' -> '.join(place for place in item['route']))
		print(f"Departure from {item['route'][0]}: {item['dep_time']}.")
		print(f"Arrival to {item['route'][-1]}: {item['arr_time']}.")
		print(f"Total price: {item['price']}€.\n")

	return final


find_combinations()

# TODO: Output to stdout stderr?

# TODO: Return output for further processing.

# TODO: Simplify.
