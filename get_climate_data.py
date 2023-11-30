import requests
import json
import sys
import re



# https://cckpapi.worldbank.org/cckp/v1/cmip6-x0.25_timeseries_hd30,hdd65,r50mm_timeseries_annual,seasonal_1950-2014,2015-2100_median,p10,p90_historical_ensemble_all_mean/USA?_format=json

def get_formatted_fields(field_collection):
	formatted = '_'.join(
		map(
			lambda fields: ','.join(fields),
      			field_collection
		)
	)
	return formatted

def get_climate_data():
	host = 'https://cckpapi.worldbank.org'
	endpoint = '/cckp/v1/'

	collections =	['cmip6-x0.25']
	types =			['timeseries']

	# can do a maximum of 5 fields per any request
	variables_to_names = {
		# number of days
		'hd30':					'Hot Days above 30 degrees Celsius',
		'hd35':					'Hot Days above 35 degrees Celsius',
		'hd40':		 			'Hot Days above 40 degrees Celsius',
		# 'hd45':					'Hot Days above 45 degrees Celsius',

		# # risk categorizations: 0 is low 4 is high
		# 'hdcat':				'Hot Day Heat Risk Categorization', 
		# 'hdtrcat':				'Hot Day and Tropical Nights Heat Risk Categorization',
		# 'hdtrhicat': 			'Hot Day and Tropical Nights with Humidity Heat Risk Categorization',
		# 'hdtrhipopdensitycat':	'Temperature and Humidity-Based Heat + Population Risk Categorization',
		# 'hdtrpopdensitycat': 	'Temperature-Based Heat + Population Risk Categorization',
		# 'hicat': 				'Heat Index Heat Risk Categorization',
		# 'trcat':				'Tropical Night Heat Risk Categorization',

		# # millimeters of rainfall
		'r20mm':				'Number of Days with Precipitation >20mm',
		'r50mm':				'Number of Days with Precipitation >50mm',
	}
	variables = list(variables_to_names.keys())

	products = 		['timeseries']
	aggregations = 	[
		'annual',
		# 'seasonal'
	]
	periods = 	[
		'1950-2014',
		'2015-2100'
	]
	percentiles = 	[
		# 'p10',
		'median',
		# 'p90'
	]
	scenarios = 	['historical']
	models = 		['ensemble']
	calculations =	['all']
	statistics = 	['mean']

	all_fields = [
		collections,
		types,
		variables,
		products,
		aggregations,
		periods,
		percentiles,
		scenarios,
		models,
		calculations,
		statistics,
	]

	# state_keys = {}
	geocodes = [['USA'] #+ [
		# f'USA.{state_code}'
		# for state_code
		# in range(2593214, 2593264 + 1)
	]#]


	formatted_fields = get_formatted_fields(all_fields)
	formatted_geocodes = get_formatted_fields(geocodes)

	formatted_fields = '_'.join(
		map(
			lambda fields: ','.join(fields),
      			all_fields
		)
	)

	request_url = f'{host}{endpoint}{formatted_fields}/{formatted_geocodes}'
	print(request_url)
	params = {'_format': 'json'}

	response = json.loads(requests.get(request_url, params=params).content)
	response_data = response['data']

	print(response_data)


if __name__ == '__main__':
	get_climate_data()
