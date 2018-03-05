from json import load, dumps
from copy import deepcopy
import os

base_url = os.path.abspath(os.path.dirname(__file__))
json_url = os.path.join(base_url, 'app/static/json')

class mpi:
	getChannel = getProgramRank = getChannelTrend = None
	
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
				programs = items['program']
				data['program'] = []
				# If user selected a set of channels then use that subset of programs to segment
				if not channel_id:
					data['program'] = []
					programs = items['program']
				else:
					programs = deepcopy(data['program'])
					data['program'] = []
				for program in programs:
					if int(program['channelId']) % mod == 0:
						data['program'].append(program)
			
			elif endpoint == 'getChannelTrend.json':
				data['metric']['channel'] = []
				for channelTrend in items['metric']['channel']:
					if int(channelTrend['id']) % mod == 0:
						data['metric']['channel'].append(channelTrend)
			
			return data
		return data
	
	# 
	def get_data(request):
		# Loads the appropriate JSON data file
		path_split = request.path.rpartition('/')
		endpoint = path_split[len(path_split) - 1]
		if endpoint == 'getProgram.json':
			endpoint = 'getProgramRank.json'
		data = load(open(os.path.join(json_url, 'mpi.' + endpoint)))
		
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
		
		resp = mpi.filter_data(endpoint, filters, channel_id, deepcopy(data[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]))
		
		# User selected to sort the programs in ascending value so simply reverse the list of programs
		if mode == 'bottom':
			resp['program'].reverse()
		
		# Returns the data as JSON
		return dumps(resp)
	
	def get_filter_names(request):
		# Loads the appropriate JSON data file
		path_split = request.path.rpartition('/')
		data = load(open(os.path.join(json_url, 'mpi.' + path_split[len(path_split) - 1])))
		
		# Required query string parameters
		page = request.args.get('page')
		
		# If page is 0 then returns all the data for the selected filter as JSON and otherwise simply returns the count of the filter values
		if page == '0':
			return dumps(data)
		else:
			return dumps({'success': 'true', 'count': data['count']})
	
	def get_filter_values(request):
		# Loads the appropriate JSON data file
		path_split = request.path.rpartition('/')
		data = load(open(os.path.join(json_url, 'mpi.' + path_split[len(path_split) - 1])))
		
		# Required query string parameters
		name = request.args.get('name')
		page = request.args.get('page')
		
		# If page is 0 then returns all the data for the selected filter as JSON and otherwise simply returns the count of the filter values
		if page == '0':
			return dumps(data[name])
		else:
			return dumps({'success': 'true', 'count': data[name]['count']})
	
	def quickcharts():
		return dumps(load(open(os.path.join(json_url, 'mpi.quickcharts.json'))))
	
	def getUser():
		return dumps({'munchkin_id':'000-AAA-000','customer_prefix':'mpi4marketolive','user_id':'mpi@marketolive.com'})
	
	'''
	def del_quickchart():
		return dumps({})
	'''