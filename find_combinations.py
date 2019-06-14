import sys
import csv
from datetime import datetime


def find_combinations(bags_num):
	"""
	Find all combinations of flights for passengers with no bags,
	one bag or two bags are able to travel, having 1 to 4 hours
	for each transfer between flights.
	"""

	with open('input.csv') as f:
		reader = csv.reader(f)

		# Create initial list with itineraries.
		initial = []
		for row in reader:
			if reader.line_num == 1:
				continue
			price = int(row[5]) + int(row[7])*bags_num
			if int(row[6]) >= bags_num:
				initial.append({'route': [row[0], row[1]],
				                'arr_time': row[3],
				                'price': price})

		current_len = 2
		final = []
		# Set flag to control if program should stop or look for the next link.
		found_next_flight = True

		f.seek(0)
		time_format = '%Y-%m-%dT%H:%M:%S'
		while found_next_flight:
			found_next_flight = False
			temp_list = []
			for item in initial:
				# Skip first line to avoid errors without using try - except.
				next(reader)

				for row in reader:
					# Set place condition (next source == last destination).
					place_cond = bool(row[0] == item['route'][current_len-1])
					# Set time condition.
					next_dep = datetime.strptime(row[2], time_format)
					last_arr = datetime.strptime(item['arr_time'], time_format)
					transfer = next_dep - last_arr
					time_cond = bool(3600 <= transfer.total_seconds() <= 4 * 3600)
					# Avoid travelling through same cities.
					repeat_cond = not bool(row[1] in item['route'][1:-1])

					if place_cond and time_cond and repeat_cond \
							and int(row[6]) >= bags_num:
						# If next flight was found run the whole process once more.
						found_next_flight = True
						price = int(row[5]) + int(row[7]) * bags_num
						new_route = []
						for n in range(current_len):
							new_route.append(item['route'][n])
						new_route.append(row[1])
						temp_list.append({'route': new_route,
						                'arr_time': row[3],
						                'price': item['price'] + price})

				f.seek(0)
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

			for item in cinitial:
				print(item)
			print(len(cinitial))
			current_len += 1

		for item in final:
			print(item)
		print(len(final))


find_combinations(1)

# TODO: Check if there's really only one connection for 2 bags.

# TODO: Modify to access from command line.

# TODO: Good output.

# TODO: Return for further processing.

# TODO: Simplify.