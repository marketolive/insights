from app import app
from flask import request, render_template, send_file, redirect, abort
from re import search
from json import load, loads, dumps
from copy import deepcopy
from globals import *
import os, requests

# Global Vars
base_url = os.path.abspath(os.path.dirname(__file__))
json_url = os.path.join(base_url, 'static/json')
resp_code = 200
json_resp_headers = {
	'Content-Type': 'application/json; charset=UTF-8'
}

# Loads the appropriate JSON data file into a global var before handling the request
@app.before_request
def before_request():
	if request.path == '/cmo/v1/metadata/getChannel.json':
		mpi.getChannel = load(open(os.path.join(json_url, 'mpi.getChannel.json')))
	elif request.path in ['/cmo/v1/metadata/getProgramRank.json',
												'/cmo/v1/metadata/getProgram.json']:
		mpi.getProgramRank = load(open(os.path.join(json_url, 'mpi.getProgramRank.json')))
	elif request.path == '/cmo/v1/metadata/getChannelTrend.json':
		mpi.getChannelTrend = load(open(os.path.join(json_url, 'mpi.getChannelTrend.json')))
	elif request.path in ['/cmo/v1/metadata/getProgramTagName.json',
												'/cmo/v1/metadata/getWorkspace.json',
												'/cmo/v1/metadata/getAbmAccountList.json',
												'/cmo/v1/metadata/getCustomAttributeName.json',
												'/cmo/v1/metadata/getOpportunityType.json',
												'/cmo/v1/metadata/getProgramTagValue.json',
												'/cmo/v1/metadata/getCustomAttributeValue.json']:
		mpi.filters = load(open(os.path.join(json_url, 'mpi.filters.json')))
	elif request.path == '/cmo/v1/metadata/quickcharts.json':
		mpi.quickcharts = load(open(os.path.join(json_url, 'mpi.quickcharts.json')))
	elif request.path == '/cmo/v1/metadata/export.json': # Returns static file for 'PPT Download'
		return send_file('static/export/mpi-revenue_won_to_cost_ratio_mt-previous_year.pptx')
	elif request.path == '/cmo/v1/export/getExcelData.json': # Returns static file for 'EXCEL Download'
		return send_file('static/export/mpi-revenue_won_to_cost_ratio_mt-previous_year.xlsx')

# MPI Page
@app.route('/mpi')
@app.route('/marketo-performance')
@app.route('/marketing-performance')
def mpi_page():
	return render_template('mpi.html')

#MPI JSON Endpoints
@app.route('/cmo/v1/metadata/<endpoint>.json')
def mpi_endpoint(endpoint):
	if endpoint in ['getChannel', 'getProgramRank', 'getChannelTrend', 'getProgram']:
		resp = None
		
		# Required (mostly) query string parameters
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
		
		# If the isAttribution selected has no effect on the data for metric selected
		if isAttribution not in mpi.isAttribution_dict[top_view_metrics]:
			isAttribution = 'false'
		
		# If the time_period selected is any custom range
		if time_period not in mpi.time_period_list:
			time_period = 'YTD'
		
		# Sets settings based upon the selected metric and setting as some settings have no effect on the data for the metric selected
		settings = mpi.settings_dict[top_view_metrics][settings]
		
		if endpoint == 'getChannel':
			resp = deepcopy(mpi.getChannel[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
		elif endpoint in ['getProgramRank', 'getProgram']:
			resp = deepcopy(mpi.getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
			# User selected a set of channels to segment the data via post-filtering
			if channel_id:
				channel_id = loads(channel_id)
				resp['program'] = []
				for program in mpi.getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['program']:
					if program['channelId'] in channel_id:
						resp['program'].append(program)
		elif endpoint == 'getChannelTrend':
			resp = deepcopy(mpi.getChannelTrend[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
		
		# User selected a set of filters to segment the data via post-filtering
		if program_tag or workspace or abm_account_list or custom_attribute or investment_period or opportunity_type:
			# Counts the number of filters selected plus 1 to set a divisor used to determine if a channel id is an even multiple
			# Ensures that subset of programs returned are part of the subset of channels returned and are decreasing in size as the number of filters increases
			filters = [program_tag, workspace, abm_account_list, custom_attribute, investment_period, opportunity_type]
			num_of_filters = sum(filter is not None for filter in filters)
			mod = num_of_filters + 1
			
			if endpoint == 'getChannel':
				resp['channel'] = []
				for channel in mpi.getChannel[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['channel']:
					if int(channel['id']) % mod == 0:
						resp['channel'].append(channel)
			
			elif endpoint == 'getProgramRank':
				programs = None
				# If user selected a set of channels then use that subset of programs to segment
				if not channel_id:
					resp['program'] = []
					programs = mpi.getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['program']
				else:
					programs = deepcopy(resp['program'])
					resp['program'] = []
				for program in programs:
					if int(program['channelId']) % mod == 0:
						resp['program'].append(program)
			
			elif endpoint == 'getChannelTrend':
				resp['metric']['channel'] = []
				for channelTrend in mpi.getChannelTrend[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['metric']['channel']:
					if int(channelTrend['id']) % mod == 0:
						resp['metric']['channel'].append(channelTrend)
		
		# User selected to sort the programs in ascending value so simply reverse the list of programs
		if mode == 'bottom':
			resp['program'].reverse()
		
		# Returns the data as JSON w/ 200 response and sets the Content-Type header
		return dumps(resp), None, json_resp_headers
	
	elif endpoint in ['getProgramTagName', 'getWorkspace', 'getAbmAccountList', 'getCustomAttributeName', 'getOpportunityType']:
		page = request.args.get('page')
		# If page is 0 then returns all the data for the selected filter as JSON and otherwise simply returns the count of the filter values
		if page == '0':
			return dumps(mpi.filters[endpoint]), None, json_resp_headers
		else:
			return dumps({'success': 'true', 'count': mpi.filters[endpoint]['count']}), None, json_resp_headers
	
	elif endpoint in ['getProgramTagValue', 'getCustomAttributeValue']:
		name = request.args.get('name')
		page = request.args.get('page')
		# If page is 0 then returns all the data for the selected tag/attribute filter as JSON and otherwise simply returns the count of the tag/attribute values
		if page == '0':
			return dumps(mpi.filters[endpoint][name]), None, json_resp_headers
		else:
			return dumps({'success': 'true', 'count': mpi.filters[endpoint][name]['count']}), None, json_resp_headers
	
	elif endpoint == 'quickcharts':
		return dumps(mpi.quickcharts), None, json_resp_headers
	
	elif endpoint == 'getUser':
		return dumps({'munchkin_id':'000-AAA-000','customer_prefix':'mpi4marketolive','user_id':'mpi@marketolive.com'}), None, json_resp_headers
	
	# Returns empty JSON for endpoint which deletes a Quick Chart (header is 'DELETE')
	#elif (endpoint == '150'):
	#	return dumps({}), 200, json_resp_headers
	
	else:
		abort(404)

# Email Insights Page
@app.route('/email')
@app.route('/email-insights')
def ei_page():
	return render_template('ei.html')

# Sets Cache-Control header based upon the Content-Type header
@app.after_request
def add_header(response):
	if search('^application/json;?', response.headers['Content-Type']):
		response.headers['Cache-Control'] = 'public, max-age=86400'
	elif search('/?javascript;?', response.headers['Content-Type']):
		response.headers['Cache-Control'] = 'public, max-age=86400'
	elif search('^text/(html|css);?', response.headers['Content-Type']):
		response.headers['Cache-Control'] = 'public, max-age=86400'
	elif search('^image/', response.headers['Content-Type']):
		response.headers['Cache-Control'] = 'public, max-age=86400'
	else:
		response.headers['Cache-Control'] = 'public, max-age=86400'
	return response