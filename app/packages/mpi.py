from os import path
from json import load, loads, dumps
from copy import deepcopy
from random import random, uniform
#from math import ceil
#from re import compile, search
#import os

app_path = path.abspath(path.join(__file__, '..', '..'))
json_url = path.join(app_path, 'static/json')

time_period_list = [
	'currentMonth',
	'currentQuarter',
	'YTD',
	'previousMonth',
	'previousQuarter',
	'previousYear',
	'last12Month'
]

isAttribution_dict = {
	'Successes': ['false'],
	'New Names': ['false'],
	'{"First-Touch":["New Opportunities"]}': ['false'],
	'{"First-Touch":["Pipeline Created"]}': ['false'],
	'{"First-Touch":["Pipeline Open"]}': ['false'],
	'{"First-Touch":["Expected Revenue"]}': ['false'],
	'{"Multi-Touch":["New Opportunities"]}': ['false'],
	'{"Multi-Touch":["Pipeline Created"]}': ['false'],
	'{"Multi-Touch":["Pipeline Open"]}': ['false'],
	'{"Multi-Touch":["Expected Revenue"]}': ['false'],
	'{"First-Touch":["Opportunities Won"]}': ['false'],
	'{"First-Touch":["Revenue Won"]}': ['false'],
	'{"Multi-Touch":["Opportunities Won"]}': ['false'],
	'{"Multi-Touch":["Revenue Won"]}': ['false'],
	'{"First-Touch":["Cost Per Opportunity Created"]}': ['false', 'true'],
	'{"First-Touch":["Pipeline Created to Cost Ratio"]}': ['false', 'true'],
	'{"Multi-Touch":["Cost Per Opportunity Created"]}': ['false', 'true'],
	'{"Multi-Touch":["Pipeline Created to Cost Ratio"]}': ['false', 'true'],
	'{"First-Touch":["Cost Per Opportunity Won"]}': ['false', 'true'],
	'{"First-Touch":["Revenue Won to Cost Ratio"]}': ['false', 'true'],
	'{"Multi-Touch":["Cost Per Opportunity Won"]}': ['false', 'true'],
	'{"Multi-Touch":["Revenue Won to Cost Ratio"]}': ['false', 'true']
}

settings_dict = {
	'Successes': {
		None: 'n/a'
	},
	'New Names': {
		None: 'n/a'
	},
	'{"First-Touch":["New Opportunities"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	},
	'{"First-Touch":["Pipeline Created"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	},
	'{"First-Touch":["Pipeline Open"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	},
	'{"First-Touch":["Expected Revenue"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	},
	'{"First-Touch":["Cost Per Opportunity Created"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	},
	'{"First-Touch":["Pipeline Created to Cost Ratio"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show Multi-Touch"]}'
	},
	'{"Multi-Touch":["New Opportunities"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	},
	'{"Multi-Touch":["Pipeline Created"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	},
	'{"Multi-Touch":["Pipeline Open"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	},
	'{"Multi-Touch":["Expected Revenue"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	},
	'{"Multi-Touch":["Cost Per Opportunity Created"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	},
	'{"Multi-Touch":["Pipeline Created to Cost Ratio"]}': {
		None: '{"Before Opportunity Created":[]}',
		'{"Before Opportunity Created":["Show First-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}',
		'{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Created":["Show First-Touch"]}'
	},
	'{"First-Touch":["Opportunities Won"]}': {
		None: '{"Before Opportunity Closed":[]}',
		'{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}'
	},
	'{"First-Touch":["Revenue Won"]}': {
		None: '{"Before Opportunity Closed":[]}',
		'{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}'
	},
	'{"First-Touch":["Cost Per Opportunity Won"]}': {
		None: '{"Before Opportunity Closed":[]}',
		'{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}'
	},
	'{"First-Touch":["Revenue Won to Cost Ratio"]}': {
		None: '{"Before Opportunity Closed":[]}',
		'{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show Multi-Touch"]}'
	},
	'{"Multi-Touch":["Opportunities Won"]}': {
		None: '{"Before Opportunity Closed":[]}',
		'{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
		'{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}'
	},
	'{"Multi-Touch":["Revenue Won"]}': {
		None: '{"Before Opportunity Closed":[]}',
		'{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
		'{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}'
	},
	'{"Multi-Touch":["Cost Per Opportunity Won"]}': {
		None: '{"Before Opportunity Closed":[]}',
		'{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
		'{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}'
	},
	'{"Multi-Touch":["Revenue Won to Cost Ratio"]}': {
		None: '{"Before Opportunity Closed":[]}',
		'{"Before Opportunity Closed":["Show First-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
		'{"Before Opportunity Closed":["Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}',
		'{"Before Opportunity Closed":["Show First-Touch","Show Multi-Touch"]}': '{"Before Opportunity Closed":["Show First-Touch"]}'
	}
}

# User selected a set of filters to segment the data via post-filtering
def filter_data(endpoint, filters, channel_id, data):
	# Counts the number of filters selected plus 1 to set a divisor used to determine if a channel id is an even multiple
	# Ensures that subset of programs returned are part of the subset of channels returned and are decreasing in size as the number of filters increases
	num_of_filters = sum(filter is not None for filter in filters)
	if num_of_filters > 0:
		mod = num_of_filters + 1
		items = deepcopy(data)
		
		if endpoint == 'getChannel.json':
			data['channel'] = []
			for channel in items['channel']:
				if int(channel['id']) % mod == 0:
					data['channel'].append(channel)
		
		elif endpoint == 'getProgramRank.json':
			data['program'] = []
			for program in items['program']:
				if channel_id:
					if int(program['id']) % mod == 0:
						data['program'].append(program)
				else:
					if int(program['channelId']) % mod == 0:
						data['program'].append(program)
		
		elif endpoint == 'getChannelTrend.json':
			data['metric']['channel'] = []
			for channelTrend in items['metric']['channel']:
				if int(channelTrend['id']) % mod == 0:
					data['metric']['channel'].append(channelTrend)
		
		return data
	return data

# If a value < min_bound_pct is found in getChannelTrend, getProgramTrend responses then set the value as (min_pct <= random_pct <= max_pct) of the first value
def populate_data(endpoint, data, min_bound_pct, min_pct, max_pct, default_val):
	if endpoint == 'getChannelTrend.json':
		dimension_name = 'channel'
	elif endpoint == 'getProgramTrend.json':
		dimension_name = 'program'
	else:
		return data
	
	for dimension_idx, dimension in enumerate(data['metric'][dimension_name]):
		if dimension_idx < 16:
			for period in dimension['period']:
				period_val = float(period.get('value', '0'))
				period_first_val = float(data['metric'][dimension_name][dimension_idx]['period'][0].get('value', default_val))
				if period_first_val == 0:
					period_first_val = default_val
				if period_val == 0 or (period_val / period_first_val) < min_bound_pct:
					period['value'] = str(period_first_val * uniform(min_pct, max_pct))
		else:
			break
	
	return data

# Handles getChannel, getProgramRank, getChannelTrend
def get_data(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	endpoint = path_split[len(path_split) - 1]
	jsonData = request.args.get('jsonData') or 'default'
	
	data = load(open(path.join(json_url, 'mpi.' + jsonData + '.' + endpoint)))
	
	# Required query string parameters
	sidebar = request.args.get('sidebar')
	tab_name = request.args.get('tab_name')
	top_view_metrics = request.args.get('top_view_metrics')
	isAttribution = request.args.get('isAttribution')
	time_period = request.args.get('time_period')
	mode = request.args.get('mode')
	settings = request.args.get('settings')
	channel_id = request.args.get('channel_id')
	# Optional query string parameters
	program_tag = request.args.get('program_tag')
	workspace = request.args.get('workspace')
	abm_account_list = request.args.get('abm_account_list')
	custom_attribute = request.args.get('custom_attribute')
	investment_period = request.args.get('investment_period')
	opportunity_type = request.args.get('opportunity_type')
	filters = [program_tag, workspace, abm_account_list, custom_attribute, investment_period, opportunity_type]
	
	# If the isAttribution selected has no effect on the data for metric selected
	if isAttribution not in isAttribution_dict[top_view_metrics]:
		isAttribution = 'false'
	# If the time_period selected is any custom range
	if time_period not in time_period_list:
		time_period = 'YTD'
	# Sets settings based upon the selected metric and setting as some settings have no effect on the data for the metric selected
	settings = settings_dict[top_view_metrics][settings]
	
	data = data[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]
	
	# User selected a set of channels to segment the data via post-filtering
	if channel_id:
		channel_id = loads(channel_id)
		programs = deepcopy(data['program'])
		data['program'] = []
		for program in programs:
			if program['channelId'] in channel_id:
				data['program'].append(program)
	
	resp = filter_data(endpoint, filters, channel_id, data)
	
	# User selected to sort the programs in ascending value so simply reverse the list of programs
	if mode == 'bottom':
		resp['program'].reverse()
	
	if endpoint == 'getChannelTrend.json':
		resp = populate_data('getChannelTrend.json', resp, 0.2, 0.2, 0.8, 100)
	
	# Returns the data as JSON
	return dumps(resp)

def getProgram(request):
	# Loads the appropriate JSON data file
	jsonData = request.args.get('jsonData') or 'default'
	
	channelData = load(open(path.join(json_url, 'mpi.' + jsonData + '.getChannel.json')))
	programData = load(open(path.join(json_url, 'mpi.' + jsonData + '.getProgramRank.json')))
	
	# Required query string parameters
	sidebar = request.args.get('sidebar')
	tab_name = request.args.get('tab_name')
	top_view_metrics = request.args.get('top_view_metrics')
	isAttribution = request.args.get('isAttribution')
	time_period = request.args.get('time_period')
	settings = request.args.get('settings')
	channel_id = request.args.get('channel_id')
	
	# If the isAttribution selected has no effect on the data for metric selected
	if isAttribution not in isAttribution_dict[top_view_metrics]:
		isAttribution = 'false'
	# If the time_period selected is any custom range
	if time_period not in time_period_list:
		time_period = 'YTD'
	# Sets settings based upon the selected metric and setting as some settings have no effect on the data for the metric selected
	settings = settings_dict[top_view_metrics][settings]
	
	resp = {
		'success': 'true',
		'last_update_timestamp': '2018-01-16 22:18:00.0',
		'program': []
	}
	channelData = channelData[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]
	programData = programData[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]
	channel_id = loads(channel_id)
	
	for channel in deepcopy(channelData['channel']):
		if channel['id'] in channel_id:
			channel['channelId'] = deepcopy(channel['id'])
			for metric in channel['metrics']:
				metric['channelTotal'] = deepcopy(metric.get('value', '0'))
				metric['channelPreviousPeriodTotal'] = deepcopy(metric['previousPeriodValue'])
			for program in programData['program']:
				if program['channelId'] in channel_id:
					channel['name'] = program['name']
					channel['id'] = program['id']
					''' Used for pulling in the actual value for the viewed metric in the program drill-down
					channel['viewMetric'] = {
						'name': program['metrics'][0]['name'],
						'value': program['metrics'][0]['value']
					}
					'''
					resp['program'].append(deepcopy(channel))
			
			r_curr_list = []
			r_prev_list = []
			for idx in range(len(channel['metrics'])):
				r = [random() for i in range(len(resp['program']))]
				s = sum(r)
				r_curr_list.append([ i/s for i in r ])
			for idx in range(len(channel['metrics'])):
				r = [random() for i in range(len(resp['program']))]
				s = sum(r)
				r_prev_list.append([ i/s for i in r ])
			
			for idx_program, program in enumerate(resp['program']):
				for idx_metric, metric in enumerate(channel['metrics']):
					metric_val = r_curr_list[idx_metric][idx_program] * float(metric['channelTotal'])
					''' Used for pulling in the actual value for the viewed metric in the program drill-down
					if idx_program == 0 and (metric['name'] == program['viewMetric']['name'] or metric['name'] == '% ' + program['viewMetric']['name']):
						metric_val = float(program['viewMetric']['value'])
						metric['channelTotal'] -= metric_val
					'''
					
					if metric['format'] == 'percentage':
						metric['value'] = str(round((metric_val / float(metric['channelTotal'])) * 100, 7))
					else:
						metric['value'] = str(round(metric_val, 7))
					
					metric['previousPeriodValue'] = str(round(r_prev_list[idx_metric][idx_program] * float(metric['channelPreviousPeriodTotal']), 7))
					program['metrics'][idx_metric] = deepcopy(metric)
			
			break
	
	# Returns the data as JSON
	return dumps(resp)

def getProgramTrend(request):
	# Loads the appropriate JSON data file
	jsonData = request.args.get('jsonData') or 'default'
	
	channelData = load(open(path.join(json_url, 'mpi.' + jsonData + '.getChannelTrend.json')))
	programData = load(open(path.join(json_url, 'mpi.' + jsonData + '.getProgramRank.json')))
	
	# Required query string parameters
	sidebar = request.args.get('sidebar')
	tab_name = request.args.get('tab_name')
	top_view_metrics = request.args.get('top_view_metrics')
	isAttribution = request.args.get('isAttribution')
	time_period = request.args.get('time_period')
	settings = request.args.get('settings')
	channel_id = request.args.get('channel_id')
	
	# If the isAttribution selected has no effect on the data for metric selected
	if isAttribution not in isAttribution_dict[top_view_metrics]:
		isAttribution = 'false'
	# If the time_period selected is any custom range
	if time_period not in time_period_list:
		time_period = 'YTD'
	# Sets settings based upon the selected metric and setting as some settings have no effect on the data for the metric selected
	settings = settings_dict[top_view_metrics][settings]
	
	resp = {
		'success': 'true',
		'last_update_timestamp': '2018-01-16 22:18:00.0',
		'metric': {
			'metric_name': None,
			'metric_format': None,
			'program': []
		}
	}
	channelData = channelData[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]
	programData = programData[sidebar]['contribution'][top_view_metrics][isAttribution]['previousYear'][settings]
	resp['metric']['metric_name'] = channelData['metric']['metric_name']
	resp['metric']['metric_format'] = channelData['metric']['metric_format']
	channel_id = loads(channel_id)
	
	for channel in deepcopy(channelData['metric']['channel']):
		if channel['id'] in channel_id:
			channel['channelId'] = deepcopy(channel['id'])
			for period in channel['period']:
				period['channelTotal'] = deepcopy(period.get('value', '0'))
			for program in programData['program']:
				if program['channelId'] in channel_id:
					channel['name'] = program['name']
					channel['id'] = program['id']
					resp['metric']['program'].append(deepcopy(channel))
			
			r_curr_list = []
			for idx in range(len(channel['period'])):
				r = [random() for i in range(len(resp['metric']['program']))]
				s = sum(r)
				r_curr_list.append([ i/s for i in r ])
			
			for idx_program, program in enumerate(resp['metric']['program']):
				for idx_period, period in enumerate(channel['period']):
					period_val = r_curr_list[idx_period][idx_program] * float(period['channelTotal'])
					period['value'] = str(round(period_val, 7))
					program['period'][idx_period] = deepcopy(period)
			
			break
	
	resp = populate_data('getProgramTrend.json', resp, 0.2, 0.2, 0.8, 100)
	
	# Returns the data as JSON
	return dumps(resp)

# Handles getProgramTagName, getWorkspace, getAbmAccountList, getCustomAttributeName, getOpportunityType
def get_filter_names(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	jsonData = request.args.get('jsonData') or 'default'
	
	data = load(open(path.join(json_url, 'mpi.' + jsonData + '.' + path_split[len(path_split) - 1])))
	
	# Required query string parameters
	page = request.args.get('page')
	
	# If page is 0 then returns all the data for the selected filter as JSON and otherwise simply returns the count of the filter values
	if page == '0':
		return dumps(data)
	else:
		return dumps({'success': 'true', 'count': data['count']})

# Handles getProgramTagValue, getCustomAttributeValue
def get_filter_values(request):
	# Loads the appropriate JSON data file
	path_split = request.path.rpartition('/')
	jsonData = request.args.get('jsonData') or 'default'
	
	data = load(open(path.join(json_url, 'mpi.' + jsonData + '.' + path_split[len(path_split) - 1])))
	
	# Required query string parameters
	name = request.args.get('name')
	page = request.args.get('page')
	
	# If page is 0 then returns all the data for the selected filter as JSON and otherwise simply returns the count of the filter values
	if page == '0':
		return dumps(data[name])
	else:
		return dumps({'success': 'true', 'count': data[name]['count']})

def quickcharts(request):
	jsonData = request.args.get('jsonData') or 'default'
	return dumps(load(open(path.join(json_url, 'mpi.' + jsonData + '.quickcharts.json'))))

def getUser():
	return dumps({'munchkin_id':'000-AAA-000','customer_prefix':'mpi4marketolive','user_id':'mpi@marketolive.com'})

# Handles 150
'''
def del_quickchart():
	return dumps({})
'''