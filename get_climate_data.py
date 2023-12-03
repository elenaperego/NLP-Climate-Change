import requests
import json
import sys
import re

from collections import defaultdict

DELIMITER = ','

def get_formatted_fields(field_collection):
	formatted = '_'.join(
		map(
			lambda fields: ','.join(fields),
      			field_collection
		)
	)
	return formatted

var_codes_to_names = {
	'fd':		'Number of Frost Days (Tmin < 0°C)',
	'pr':		'Precipitation',
	'rx1day':	'Average Largest 1-Day Precipitation',
	'rx5day':	'Average Largest 5-Day Cumulative Precipitation',
	'tas':		'Average Mean Surface Air Temperature',
	'tasmax':	'Average Maximum Surface Air Temperature',
	'tasmin':	'Average Minimum Surface Air Temperature',
	'tnn':		'Minimum of Daily Min-Temperature',
	'tr':		'Number of Tropical Nights (T-min > 20°C)',
	'txx':		'Maximum of Daily Max-Temperature',
}

var_codes_to_labels = {
	'fd':		'num_frost_days',
	'pr':		'precipitation',
	'rx1day':	'max_1day_precipitation',
	'rx5day':	'max_5day_cumulative_precipitation',
	'tas':		'mean_temperature',
	'tasmax':	'max_avg_temperature',
	'tasmin':	'min_avg_temperature',
	'tnn':		'min_temperature',
	'tr':		'num_trop_nights',
	'txx':		'max_temperature',
}

ordered_labels = [
	'max_avg_temperature',
	'min_avg_temperature',
	'mean_temperature',
	'max_temperature',
	'min_temperature',
	'num_frost_days',
	'num_trop_nights',
	'max_1day_precipitation',
	'max_5day_cumulative_precipitation',
	'precipitation',
]

labels_to_codes = {
	'max_avg_temperature': 'tasmax',
	'min_avg_temperature': 'tasmin',
	'mean_temperature': 'tas',
	'max_temperature': 'txx',
	'min_temperature': 'tnn',
	'num_frost_days': 'fd',
	'num_trop_nights': 'tr',
	'max_1day_precipitation': 'rx1day',
	'max_5day_cumulative_precipitation': 'rx5day',
	'precipitation': 'pr',
}

def get_climate_data():

	host = 'https://cckpapi.worldbank.org'
	endpoint = '/cckp/v1/'

	collection_code		= 'era5-x0.5'
	type_code 			= 'timeseries'


	variable_placeholder 	= '{}'
	product_code			= 'timeseries'
	aggregation_code		= 'monthly'
	period_code 			= '1950-2020'
	percentile_code			= 'mean'
	scenario_code			= 'historical'
	model_code				= 'era5' # could also be x0.5
	calculation_code		= 'era5'
	stat_code				= 'mean'

	all_fields = [
		collection_code,
		type_code,
		variable_placeholder,
		product_code,
		aggregation_code,
		period_code,
		percentile_code,
		scenario_code,
		model_code,
		calculation_code,
		stat_code
	]

	template_url = '_'.join(all_fields)

	
	geocodes = [['USA'] + [
		f'USA.{state_code}'
		for state_code
		in range(2593214, 2593264 + 1)
	]]


	geocode_to_name = {
		'USA.2593214':	'Alabama',
		'USA.2593215':	'Alaska',
		'USA.2593216':	'Arizona',
		'USA.2593217':	'Arkansas',
		'USA.2593218':	'California',
		'USA.2593219':	'Colorado',
		'USA.2593220':	'Connecticut',
		'USA.2593221':	'Delaware',
		'USA.2593222':	'District of Columbia',
		'USA.2593223':	'Florida',
		'USA.2593224':	'Georgia',
		'USA.2593225':	'Hawaii',
		'USA.2593226':	'Idaho',
		'USA.2593227':	'Illinois',
		'USA.2593228':	'Indiana',
		'USA.2593229':	'Iowa',
		'USA.2593230':	'Kansas',
		'USA.2593231':	'Kentucky',
		'USA.2593232':	'Louisiana',
		'USA.2593233':	'Maine',
		'USA.2593234':	'Maryland',
		'USA.2593235':	'Massachusetts',
		'USA.2593236':	'Michigan',
		'USA.2593237':	'Minnesota',
		'USA.2593238':	'Mississippi',
		'USA.2593239':	'Missouri',
		'USA.2593240':	'Montana',
		'USA.2593241':	'Nebraska',
		'USA.2593242':	'Nevada',
		'USA.2593243':	'New Hampshire',
		'USA.2593244':	'New Jersey',
		'USA.2593245':	'New Mexico',
		'USA.2593246':	'New York',
		'USA.2593247':	'North Carolina',
		'USA.2593248':	'North Dakota',
		'USA.2593249':	'Ohio',
		'USA.2593250':	'Oklahoma',
		'USA.2593251':	'Oregon',
		'USA.2593252':	'Pennsylvania',
		'USA.2593253':	'Rhode Island',
		'USA.2593254':	'South Carolina',
		'USA.2593255':	'South Dakota',
		'USA.2593256':	'Tennessee',
		'USA.2593257':	'Texas',
		'USA.2593258':	'Utah',
		'USA.2593259':	'Vermont',
		'USA.2593260':	'Virginia',
		'USA.2593261':	'Washington',
		'USA.2593262':	'West Virginia',
		'USA.2593263':	'Wisconsin',
		'USA.2593264':	'Wyoming',
	}

	collected_data = defaultdict(lambda: defaultdict(dict))
	for var_code in var_codes_to_names.keys():
		full_url = f'{host}{endpoint}{template_url.format(var_code)}/{get_formatted_fields(geocodes)}?_format=json'
		# print(full_url)
		response = requests.get(full_url).content
		if not response:
			print(f'skipping {var_code}', file=sys.stderr)
		response_data = json.loads(response)['data']
		for state, month_data in response_data.items():
			for date, data in month_data.items():
				collected_data[date][state][var_code] = data

	# write results to stdout in csv format
	print(DELIMITER.join(['date', 'state'] + ordered_labels))

	for date, state_data in collected_data.items():
		for state, metric_data in state_data.items():
			entry = [
				date,
				geocode_to_name[state] if state != 'USA' else 'USA'
			]
			for label in ordered_labels:
				code = labels_to_codes[label]
				entry.append(str(metric_data[code]))
			print(DELIMITER.join(entry))

if __name__ == '__main__':
	get_climate_data()
