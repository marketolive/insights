import os, json, operator, re
#import copy, random, math

app_path = os.path.abspath(os.path.join(__file__, '..', '..'))
json_url = os.path.join(app_path, 'static/json')

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

# User selected a set of filters to segment the data via post-filtering
def filter_data(endpoint, filters, data, sortByMetric=None):
	if filters and len(filters) > 0:
		frac = 20
		div = mod = len(filters) + 1
		for filter in filters:
			div = mod = mod + len(filters[filter])
		
		if endpoint == 'kpis.json':
			for result in data['result']:
				value = result['mainMetric']['value']
				benchmark = result['mainMetric']['benchmark']
				metricType = result['mainMetric']['metricType']
				quality = result['mainMetric']['quality']
				if result['mainMetric']['format'] == 'COUNT':
					result['mainMetric']['value'] = round(int(value) / div)
					result['mainMetric']['benchmark'] = round(int(benchmark) / div)
				else:
					pct = div / frac
					if int(value) % mod == 0:
						result['mainMetric']['value'] = value = float(value) + (float(value) * pct)
					else:
						result['mainMetric']['value'] = value = float(value) - (float(value) * pct)
					if metricType in ['UNSUBSCRIBE_RATE', 'HARD_BOUNCE_RATE']:
						if value <= benchmark:
							quality = 'GOOD'
						else:
							quality = 'BAD'
					else:
						if value >= benchmark:
							quality = 'GOOD'
						else:
							quality = 'BAD'
				for secondaryMetric in result['secondaryMetrics']:
					sec_value = secondaryMetric['value']
					sec_benchmark = secondaryMetric['benchmark']
					sec_metricType = secondaryMetric['metricType']
					if secondaryMetric['format'] == 'COUNT':
						secondaryMetric['value'] = round(int(sec_value) / div)
						secondaryMetric['benchmark'] = round(int(sec_benchmark) / div)
					else:
						sec_pct = div / frac
						if int(sec_value) % mod == 0:
							secondaryMetric['value'] = float(sec_value) + (float(sec_value) * sec_pct)
						else:
							secondaryMetric['value'] = float(sec_value) - (float(sec_value) * sec_pct)
		
		elif endpoint == 'timeseries.json':
			for metric in data['result']:
				for point in data['result'][metric]:
					if point['currentValue']:
						currentValue = int(point['currentValue']['value'])
						newValue = currentValue / div
						if currentValue % 10 != 0:
							pct = (currentValue % 10) / frac
						else:
							pct = 10 / frac
						if currentValue % mod == 0:
							point['currentValue']['value'] = round(newValue + (newValue * pct))
						else:
							point['currentValue']['value'] = round(newValue - (newValue * pct))
					if point['comparisonValue']:
						comparisonValue = int(point['comparisonValue']['value'])
						newValue = comparisonValue / div
						if comparisonValue % 10 != 0:
							pct = (comparisonValue % 10) / frac
						else:
							pct = 10 / frac
						if comparisonValue % mod == 0:
							point['comparisonValue']['value'] = round(newValue + (newValue * pct))
						else:
							point['comparisonValue']['value'] = round(newValue - (newValue * pct))
		
		elif endpoint == 'breakdown.json':
			newValues = []
			results = []
			for i, breakdown in enumerate(data['result']):
				for metricName in breakdown['metricValues']:
					currentValue = int(breakdown['metricValues'][metricName]['currentValue'])
					newValue = currentValue / div
					if currentValue % 10 != 0:
						pct = (currentValue % 10) / frac
					else:
						pct = 10 / frac
					if currentValue % mod == 0:
						breakdown['metricValues'][metricName]['currentValue'] = round(newValue + (newValue * pct))
					else:
						breakdown['metricValues'][metricName]['currentValue'] = round(newValue - (newValue * pct))
					if breakdown['metricValues'][metricName]['comparisonValue']:
						comparisonValue = int(breakdown['metricValues'][metricName]['comparisonValue'])
						newComparisonValue = comparisonValue / div
						if comparisonValue % 10 != 0:
							pct = (comparisonValue % 10) / frac
						else:
							pct = 10 / frac
						if comparisonValue % mod == 0:
							breakdown['metricValues'][metricName]['comparisonValue'] = round(newComparisonValue + (newComparisonValue * pct))
						else:
							breakdown['metricValues'][metricName]['comparisonValue'] = round(newComparisonValue - (newComparisonValue * pct))
				if sortByMetric not in [None, 'n/a']:
					newValues.append([i, breakdown['metricValues'][sortByMetric]['currentValue']])
			if sortByMetric not in [None, 'n/a']:
				newValues.sort(key=operator.itemgetter(1), reverse=True)
				for value in newValues:
					results.append(data['result'][value[0]])
				data['result'] = results
		
		elif endpoint == 'drivers.json':
			newScores = []
			results = []
			for i, driver in enumerate(data['result']):
				value = int(driver['value'])
				score = float(driver['score'])
				newValue = value / div
				newScore = score / div
				if value % 10 != 0:
					pct = (value % 10) / frac
				else:
					pct = 10 / frac
				if value % mod == 0:
					driver['value'] = round(newValue + (newValue * pct))
					driver['score'] = newScore + (newScore * pct)
				else:
					driver['value'] = round(newValue - (newValue * pct))
					driver['score'] = newScore - (newScore * pct)
				newScores.append([i, driver['score']])
			newScores.sort(key=operator.itemgetter(1), reverse=True)
			for score in newScores:
				results.append(data['result'][score[0]])
			data['result'] = results
		
		elif endpoint == 'sends.json':
			newValues = []
			results = []
			for i, send in enumerate(data['result']):
				for metricName in send['metrics']:
					value = float(send['metrics'][metricName])
					newValue = value / div
					if value % 10 != 0:
						pct = (value % 10) / frac
					else:
						pct = 10 / frac
					if value % mod == 0:
						send['metrics'][metricName] = newValue + (newValue * pct)
					else:
						send['metrics'][metricName] = newValue - (newValue * pct)
					if not re.search('_RATE$', metricName):
						send['metrics'][metricName] = round(send['metrics'][metricName])
				if sortByMetric not in [None, 'n/a']:
					newValues.append([i, send['metrics'][sortByMetric]])
			if sortByMetric not in [None, 'n/a']:
				newValues.sort(key=operator.itemgetter(1), reverse=True)
				for value in newValues:
					results.append(data['result'][value[0]])
				data['result'] = results
	
	return data

# Handles dimensions, metrics, user, kpis, allfilters, workspaces
def get_data_info(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	# Optional query string parameters
	dimension = request.args.get('dimension')
	
	if dimension:
		dimension	= json.loads(dimension)
	
	data = json.load(open(os.path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	data = filter_data(endpoint, dimension, data)
	
	# Returns the data as JSON
	return json.dumps(data)

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
	
	# Optional query string parameters
	dimension = request.args.get('dimension')
	
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
	
	if dimension:
		dimension	= json.loads(dimension)
	
	data = json.load(open(os.path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	data = data[dateRange][isCompare][comparisonBenchmark][groupByDimension][sortingType][sortByMetric]
	data = filter_data(endpoint, dimension, data, sortByMetric)
	
	# User selected to sort the results ascending value so simply reverse the list of results
	if sortingDirection == 'ASCENDING' and endpoint != 'timeseries.json':
		data['result'].reverse()
	
	return json.dumps(data)

def drivers(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	# Required query string parameters
	dateRange = request.args.get('dateRange')
	kpiType = request.args.get('kpiType')
	dimensionGroup = request.args.get('dimensionGroup')
	
	# Optional query string parameters
	dimension = request.args.get('dimension')
	
	if not dateRange:
		dateRange = dateRange_default
	
	if not dimensionGroup:
		dimensionGroup = dimensionGroup_default
	
	if dimension:
		dimension	= json.loads(dimension)
	
	data = json.load(open(os.path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	data = data[dateRange][kpiType][dimensionGroup]
	data = filter_data(endpoint, dimension, data)
	
	return json.dumps(data)

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
	
	# Optional query string parameters
	dimension = request.args.get('dimension')
	
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
	
	if dimension:
		dimension	= json.loads(dimension)
	
	data = json.load(open(os.path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	data = data[dateRange][sortingType][sortByMetric]
	data = filter_data(endpoint, dimension, data, sortByMetric)
	
	# User selected to sort the results ascending value so simply reverse the list of results
	if sortingDirection == 'ASCENDING':
		data['result'].reverse()
	
	return json.dumps(data)

def filter_values(request, filter):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	data = json.load(open(os.path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	data = data[filter]
	
	# Returns the data as JSON
	return json.dumps(data)

def filters(request):
	# Required query string parameters
	emailType = int(request.args.get('emailType'))
	isOn = request.args.get('isOn')
	
	resp = {'requestId':None,'success':True,'result':None,'errors':None}
	
	if emailType == 1:
		flag = 'BATCH'
	elif emailType == 2:
		flag = 'TRIGGER'
	elif emailType == 3:
		flag = 'OPERATIONAL'
	else:
		flag = 'OPERATIONAL'
	
	# Sets the appropriate result
	resp['result'] = 'Successfully set ' + flag + ' flag to ' + isOn + ' for user id: email@marketolive.com'
	
	# Returns the data as JSON
	return json.dumps(resp)

def quickcharts(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	data = json.load(open(os.path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
	
	# Returns the data as JSON
	return json.dumps(data)
	#return json.dumps({'requestId':None,'success':True,'result':[],'errors':None})

# Handles getting a Quick Chart
def get_quickchart(request):
	# Loads the appropriate JSON data file
	jsonData = request.args.get('jsonData') or 'default'
	
	# Required query string parameters
	quickchartId = request.args.get('quickchartId')
	
	data = json.load(open(os.path.join(json_url, 'ei.' + jsonData + '.quickcharts.get.json')))
	data = data[quickchartId]
	
	# Returns the data as JSON
	return json.dumps(data)

# Handles reorders and deletes a Quick Chart
def modify_quickchart():
	return json.dumps({'requestId':None,'success':True,'result':None,'errors':None})

# Handles quickcharts POST which saves a Quick Chart
def save_quickchart(request):
	# Required query string parameters
	chartName = request.args.get('chartName')
	
	data = json.load(open(os.path.join(json_url, 'ei.default.quickchart.example.json')))
	data['result'][0]['name'] = chartName
	
	# Returns the data as JSON
	return json.dumps(data)

# Handles activating/deactivating of custom dimensions
def activate_dimension(request, dimension):
	# Required query string parameters
	isActive = request.args.get('isActive')
	
	resp = {'requestId':None,'success':True,'result':None,'errors':None}
	
	# Sets the appropriate result
	resp['result'] = 'Successfully set active flag to ' + isActive + ' for dimension id: ' + dimension
	
	# Returns the data as JSON
	return json.dumps(resp)