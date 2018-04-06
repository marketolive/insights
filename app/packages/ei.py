from os import path
from json import load, dumps
#from copy import deepcopy
#from random import random, uniform
#from math import ceil
#from re import compile, search
#import os

app_path = path.abspath(path.join(__file__, '..', '..'))
json_url = path.join(app_path, 'static/json')

# Default parameter values
dateRange_default = 'last30days'
isCompare_default = 'false'
comparisonBenchmark_default = 'n/a'
sortingType_default = 'n/a'
sortByMetric_default = 'n/a'
dimensionGroup_default = 'n/a'

sortingTypes_dict = {
	'timeseries.json': ['n/a'],
	'breakdown.json': ['BY_NAME', 'BY_METRIC'],
	'sends.json': ['BY_SEND_TIME', 'BY_METRIC']
}
sortByMetrics_dict = {
	'timeseries.json': {
		'n/a': ['n/a']
	},
	'breakdown.json': {
		'BY_NAME': ['n/a'],
		'BY_METRIC': ['OPENS', 'CLICKED_EMAILS', 'TOTAL_UNSUBSCRIBES', 'TOTAL_SENT', 'TOTAL_DELIVERED', 'TOTAL_BOUNCES', 'TOTAL_HARD_BOUNCES', 'TOTAL_SOFT_BOUNCES']
	},
	'sends.json': {
		'BY_SEND_TIME': ['n/a'],
		'BY_METRIC': ['TOTAL_SENT', 'TOTAL_DELIVERED', 'DELIVERY_RATE', 'TOTAL_BOUNCES', 'TOTAL_SOFT_BOUNCES', 'TOTAL_HARD_BOUNCES', 'BOUNCE_RATE', 'OPENS', 'OPEN_RATE', 'CLICKED_EMAILS', 'CLICK_THRU_RATE', 'CLICK_TO_OPEN_RATE', 'TOTAL_UNSUBSCRIBES', 'UNSUBSCRIBE_RATE']
	}
}

# Handles dimensions, metrics, user, kpis, allfilters, workspaces
def get_data_info(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	# Returns the data as JSON
	return dumps(load(open(path.join(json_url, 'ei.' + jsonData + '.' + endpoint))))

# Handles timeseries, breakdown
def analytics(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	# Required query string parameters
	dateRange = request.args.get('dateRange')
	isCompare = request.args.get('isCompare')
	comparisonBenchmark = request.args.get('comparisonBenchmark')
	groupByDimension = request.args.get('groupByDimension')
	#granularity = request.args.get('granularity')
	sortingType = request.args.get('sortingType')
	sortByMetric = request.args.get('sortByMetric')
	sortingDirection = request.args.get('sortingDirection')
	
	# Multi-value query string parameter
	'''
	kpiTypes_list = None
	for arg in request.args:
		if arg[0] == 'kpiTypes':
			kpiTypes_list.append(arg[1])
	'''
	
	if not dateRange:
		dateRange = dateRange_default
	
	if not isCompare:
		isCompare = isCompare_default
	
	if not comparisonBenchmark:
		comparisonBenchmark = comparisonBenchmark_default
	
	if sortingType not in sortingTypes_dict[endpoint]:
		sortingType = sortingType_default
	
	if sortByMetric not in sortByMetrics_dict[endpoint][sortingType]:
		sortByMetric = sortByMetric_default
	
	data = load(open(path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	data = data[dateRange][isCompare][comparisonBenchmark][groupByDimension][sortingType][sortByMetric]
	
	# User selected to sort the results ascending value so simply reverse the list of results
	if sortingDirection == 'ASCENDING' and endpoint != 'timeseries.json':
		data['result'].reverse()
	
	return dumps(data)

def drivers(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	# Required query string parameters
	dateRange = request.args.get('dateRange')
	kpiType = request.args.get('kpiType')
	dimensionGroup = request.args.get('dimensionGroup')
	
	if not dateRange:
		dateRange = dateRange_default
	
	if not dimensionGroup:
		dimensionGroup = dimensionGroup_default
	
	data = load(open(path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	
	return dumps(data[dateRange][kpiType][dimensionGroup])

def sends(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	# Required query string parameters
	dateRange = request.args.get('dateRange')
	sortingType = request.args.get('sortingType')
	sortByMetric = request.args.get('sortByMetric')
	sortingDirection = request.args.get('sortingDirection')
	
	# Multi-value query string parameter
	'''
	kpiTypes_list = None
	for arg in request.args:
		if arg[0] == 'kpiTypes':
			kpiTypes_list.append(arg[1])
	'''
	
	if not dateRange:
		dateRange = dateRange_default
	
	if sortingType not in sortingTypes_dict[endpoint]:
		sortingType = sortingType_default
	
	if sortByMetric not in sortByMetrics_dict[endpoint][sortingType]:
		sortByMetric = sortByMetric_default
	
	data = load(open(path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	data = data[dateRange][sortingType][sortByMetric]
	
	# User selected to sort the results ascending value so simply reverse the list of results
	if sortingDirection == 'ASCENDING':
		data['result'].reverse()
	
	return dumps(data)

def filter_values(request, filter):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	data = load(open(path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	data = data[filter]
	
	# Returns the data as JSON
	return dumps(data)

def quickcharts(request):
	return dumps({})