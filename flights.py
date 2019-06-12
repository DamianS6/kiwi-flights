import csv
from datetime import datetime


def find_flights(bags_number):
	"""
	Find all combinations of flights for passengers with no bags,
	one bag or two bags are able to travel, having 1 to 4 hours
	for each transfer between flights.
	"""

	with open('input.csv') as f:
		input_reader = csv.reader(f)

		# Create initial list with itineraries.
		itineraries = []
		for row in input_reader:
			if input_reader.line_num == 1:
				continue
			if int(row[6]) >= bags_number:
				itineraries.append([row[0], row[1]])

		f.seek(0)
		time_format = '%Y-%m-%dT%H:%M:%S'
		for n in range(len(itineraries)):
			for row in input_reader:

				# Set place, time and avoid same city conditions for the next flight.
				place_cond = bool(row[0] == itineraries[n][1])
				repeat_cond = not bool(row[1] in itineraries[n][1:-1])

				with open('input.csv') as check:
					check_reader = csv.reader(check)
					try:
						next_dep = datetime.strptime(row[2], time_format)
						last_arr = datetime.strptime(list(check_reader)[n+1][3], time_format)
						transfer_time = next_dep - last_arr
						time_cond = bool(3600 < transfer_time.total_seconds() < 4*3600)
					except ValueError:
						continue

				# If conditions are met append next place (flight) to the list.
				if place_cond and time_cond and repeat_cond:
					if len(itineraries[n]) >= 3:
						itineraries.append([itineraries[n][0], itineraries[n][1], row[1]])
					else:
						itineraries[n].append(row[1])
			f.seek(0)

		# Make and work on copy of itineraries to avoid doing extra loop.
		citineraries = itineraries[:]
		final_list = []
		for itinerary in itineraries:
			# Delete all 2-items lists - combinations which don't go any further.
			if len(itinerary) == 2:
				citineraries.remove(itinerary)
			# Move finished combinations (returned to source) to the final list.
			if itinerary[0] == itinerary[-1]:
				final_list.append(itinerary)
				citineraries.remove(itinerary)
		itineraries = citineraries

		print(final_list)
		print(len(final_list))
		print(citineraries)
		print(len(citineraries))


find_flights(1)