from json import load, loads, dumps
from copy import deepcopy
from random import random, uniform
from app import session
#from math import ceil
#from re import compile, search
import os

base_url = os.path.abspath(os.path.dirname(__file__))
json_url = os.path.join(base_url, 'app/static/json')

class mpi:
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
	
	# Handles getChannel, getProgramRank, getChannelTrend
	def get_data(request):
		# Loads the appropriate JSON data file
		path_split = request.path.rpartition('/')
		endpoint = path_split[len(path_split) - 1]
		jsonData = request.args.get('jsonData') or 'default'
		
		data = load(open(os.path.join(json_url, 'mpi.' + jsonData + '.' + endpoint)))
		
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
		if isAttribution not in mpi.isAttribution_dict[top_view_metrics]:
			isAttribution = 'false'
		# If the time_period selected is any custom range
		if time_period not in mpi.time_period_list:
			time_period = 'YTD'
		# Sets settings based upon the selected metric and setting as some settings have no effect on the data for the metric selected
		settings = mpi.settings_dict[top_view_metrics][settings]
		
		data = data[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]
		
		# User selected a set of channels to segment the data via post-filtering
		if channel_id:
			channel_id = loads(channel_id)
			programs = deepcopy(data['program'])
			data['program'] = []
			for program in programs:
				if program['channelId'] in channel_id:
					data['program'].append(program)
		
		resp = mpi.filter_data(endpoint, filters, channel_id, data)
		
		# User selected to sort the programs in ascending value so simply reverse the list of programs
		if mode == 'bottom':
			resp['program'].reverse()
		
		# If a 0 or small value is found in getChannelTrend response then set the value as a random percentage of the first value
		period_val_modified = False
		if endpoint == 'getChannelTrend.json':
			for channel_idx, channel in enumerate(resp['metric']['channel']):
				for period in channel['period']:
					period_val = float(period.get('value', '0'))
					period_first_val = float(resp['metric']['channel'][channel_idx]['period'][0].get('value', '100'))
					if period_first_val == 0:
						period_first_val = 100
					if period_val == 0 or (period_val / period_first_val) < 0.2:
						period['value'] = str(period_first_val * uniform(0.2, 1.8))
						period_val_modified = True
		
		if period_val_modified:
			session['getChannelTrend'] = resp
			session.modified = True
			print('************ Stored getChannelTrend session ************')
		elif tab_name != 'trend':
			session.pop('getChannelTrend', None)
			print('************ Removed getChannelTrend session ************')
		
		# Returns the data as JSON
		return dumps(resp)
	
	def getProgram(request):
		# Loads the appropriate JSON data file
		jsonData = request.args.get('jsonData') or 'default'
		
		channelData = load(open(os.path.join(json_url, 'mpi.' + jsonData + '.getChannel.json')))
		programData = load(open(os.path.join(json_url, 'mpi.' + jsonData + '.getProgramRank.json')))
		
		# Required query string parameters
		sidebar = request.args.get('sidebar')
		tab_name = request.args.get('tab_name')
		top_view_metrics = request.args.get('top_view_metrics')
		isAttribution = request.args.get('isAttribution')
		time_period = request.args.get('time_period')
		settings = request.args.get('settings')
		channel_id = request.args.get('channel_id')
		
		# If the isAttribution selected has no effect on the data for metric selected
		if isAttribution not in mpi.isAttribution_dict[top_view_metrics]:
			isAttribution = 'false'
		# If the time_period selected is any custom range
		if time_period not in mpi.time_period_list:
			time_period = 'YTD'
		# Sets settings based upon the selected metric and setting as some settings have no effect on the data for the metric selected
		settings = mpi.settings_dict[top_view_metrics][settings]
		
		channelData = channelData[sidebar][tab_name]
		programData = programData[sidebar][tab_name]
		channel_id = loads(channel_id)
		resp = {
			'success': 'true',
			'last_update_timestamp': '2018-01-16 22:18:00.0',
			'program': []
		}
		
		for channel in deepcopy(channelData[top_view_metrics][isAttribution][time_period][settings]['channel']):
			if channel['id'] in channel_id:
				channel['channelId'] = deepcopy(channel['id'])
				for metric in channel['metrics']:
					metric['channelTotal'] = deepcopy(metric.get('value', '0'))
					metric['channelPreviousPeriodTotal'] = deepcopy(metric['previousPeriodValue'])
				for program in programData[top_view_metrics][isAttribution][time_period][settings]['program']:
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
		
		# Required query string parameters
		sidebar = request.args.get('sidebar')
		tab_name = request.args.get('tab_name')
		top_view_metrics = request.args.get('top_view_metrics')
		isAttribution = request.args.get('isAttribution')
		time_period = request.args.get('time_period')
		settings = request.args.get('settings')
		channel_id = request.args.get('channel_id')
		
		# If the isAttribution selected has no effect on the data for metric selected
		if isAttribution not in mpi.isAttribution_dict[top_view_metrics]:
			isAttribution = 'false'
		# If the time_period selected is any custom range
		if time_period not in mpi.time_period_list:
			time_period = 'YTD'
		# Sets settings based upon the selected metric and setting as some settings have no effect on the data for the metric selected
		settings = mpi.settings_dict[top_view_metrics][settings]
		
		resp = {
			'success': 'true',
			'last_update_timestamp': '2018-01-16 22:18:00.0',
			'metric': {
				'metric_name': None,
				'metric_format': None,
				'program': []
			}
		}
		
		# Loads either the getChannelTrend session data or JSON data file
		if session.get('getChannelTrend', None):
			print('************ Using getChannelTrend session ************')
			channelData = deepcopy(session['getChannelTrend'])
			resp['metric']['metric_name'] = channelData['metric']['metric_name']
			resp['metric']['metric_format'] = channelData['metric']['metric_format']
		else:
			channelData = load(open(os.path.join(json_url, 'mpi.' + jsonData + '.getChannelTrend.json')))
			channelData = channelData[sidebar][tab_name]
			resp['metric']['metric_name'] = channelData[top_view_metrics][isAttribution][time_period][settings]['metric']['metric_name']
			resp['metric']['metric_format'] = channelData[top_view_metrics][isAttribution][time_period][settings]['metric']['metric_format']
			channelData = channelData[top_view_metrics][isAttribution][time_period][settings]
		
		programData = load(open(os.path.join(json_url, 'mpi.' + jsonData + '.getProgramRank.json')))
		programData = programData[sidebar]['contribution']
		channel_id = loads(channel_id)
		
		for channel in deepcopy(channelData['metric']['channel']):
			if channel['id'] in channel_id:
				channel['channelId'] = deepcopy(channel['id'])
				for period in channel['period']:
					period['channelTotal'] = deepcopy(period.get('value', '0'))
				for program in programData[top_view_metrics][isAttribution]['previousYear'][settings]['program']:
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
		
		# Returns the data as JSON
		return dumps(resp)
	
	# Handles getProgramTagName, getWorkspace, getAbmAccountList, getCustomAttributeName, getOpportunityType
	def get_filter_names(request):
		# Loads the appropriate JSON data file
		path_split = request.path.rpartition('/')
		jsonData = request.args.get('jsonData') or 'default'
		
		data = load(open(os.path.join(json_url, 'mpi.' + jsonData + '.' + path_split[len(path_split) - 1])))
		
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
		
		data = load(open(os.path.join(json_url, 'mpi.' + jsonData + '.' + path_split[len(path_split) - 1])))
		
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
		return dumps(load(open(os.path.join(json_url, 'mpi.' + jsonData + '.quickcharts.json'))))
	
	def getUser():
		return dumps({'munchkin_id':'000-AAA-000','customer_prefix':'mpi4marketolive','user_id':'mpi@marketolive.com'})
	
	# Handles 150
	'''
	def del_quickchart():
		return dumps({})
	'''

class ei:
	# Default parameter values
	dateRange_default = 'last30days'
	isCompare_default = 'false'
	comparisonBenchmark_default = 'n/a'
	
	sortingTypes_dict = {
		'timeseries': ['n/a'],
		'breakdown': ['BY_NAME', 'BY_METRIC'],
		'sends': ['BY_SEND_TIME', 'BY_METRIC']
	}
	sortByMetrics_dict = {
		'timeseries': {
			'n/a': ['n/a']
		},
		'breakdown': {
			'BY_NAME': ['n/a'],
			'BY_METRIC': ['OPENS', 'CLICKED_EMAILS', 'TOTAL_UNSUBSCRIBES', 'TOTAL_SENT', 'TOTAL_DELIVERED', 'TOTAL_BOUNCES', 'TOTAL_HARD_BOUNCES', 'TOTAL_SOFT_BOUNCES']
		},
		'sends': {
			'BY_SEND_TIME': ['n/a'],
			'BY_METRIC': ['TOTAL_SENT', 'TOTAL_DELIVERED', 'DELIVERY_RATE', 'TOTAL_BOUNCES', 'TOTAL_SOFT_BOUNCES', 'TOTAL_HARD_BOUNCES', 'BOUNCE_RATE', 'OPENS', 'OPEN_RATE', 'CLICKED_EMAILS', 'CLICK_THRU_RATE', 'CLICK_TO_OPEN_RATE', 'TOTAL_UNSUBSCRIBES', 'UNSUBSCRIBE_RATE']
		}
	}

	# Handles dimensions, metrics, user, kpis
	def get_data_info(request):
		# Loads the appropriate JSON data file
		path_split = request.path.rpartition('/')
		jsonData = request.args.get('jsonData') or 'default'
		
		# Returns the data as JSON
		return dumps(load(open(os.path.join(json_url, 'ei.' + jsonData + '.' + path_split[len(path_split) - 1]))))
	
	def analytics(request):
		# Loads the appropriate JSON data file
		path_split = request.path.rpartition('/')
		endpoint = path_split[len(path_split) - 1]
		jsonData = request.args.get('jsonData') or 'default'
		
		data = load(open(os.path.join(json_url, 'ei.' + jsonData + '.' + endpoint)))
		
		# Required query string parameters
		dateRange = request.args.get('dateRange')
		isCompare = request.args.get('isCompare')
		comparisonBenchmark = request.args.get('comparisonBenchmark')
		
		# Multi-value query string parameter
		kpiTypes_list = None
		for arg in request.args:
			if arg[0] == 'kpiTypes':
				kpiTypes_list.append(arg[1])
		
		# Required query string parameters
		groupByDimension = request.args.get('groupByDimension')
		granularity = request.args.get('granularity')
		sortingType = request.args.get('sortingType')
		sortByMetric = request.args.get('sortByMetric')
		sortingDirection = request.args.get('sortingDirection')
		
		if not dateRange:
			dateRange = dateRange_default
		
		if not isCompare:
			isCompare = isCompare_default
		
		if not comparisonBenchmark:
			comparisonBenchmark = comparisonBenchmark_default
		
		return dumps(data)