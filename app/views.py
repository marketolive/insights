from app import app
from flask import request, render_template, send_file, redirect, abort, session
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

# User selected a set of filters to segment the data via post-filtering
def filter_data(endpoint, filters, channel_id, resp):
	# Counts the number of filters selected plus 1 to set a divisor used to determine if a channel id is an even multiple
	# Ensures that subset of programs returned are part of the subset of channels returned and are decreasing in size as the number of filters increases
	num_of_filters = sum(filter is not None for filter in filters)
	if num_of_filters > 0:
		mod = num_of_filters + 1
		items = deepcopy(resp)
		
		if endpoint == 'getChannel':
			resp['channel'] = []
			for channel in items['channel']:
				if int(channel['id']) % mod == 0:
					resp['channel'].append(channel)
		
		elif endpoint == 'getProgramRank':
			programs = None
			# If user selected a set of channels then use that subset of programs to segment
			if not channel_id:
				resp['program'] = []
				programs = items['program']
			else:
				programs = deepcopy(resp['program'])
				resp['program'] = []
			for program in programs:
				if int(program['channelId']) % mod == 0:
					resp['program'].append(program)
		
		elif endpoint == 'getChannelTrend':
			resp['metric']['channel'] = []
			for channelTrend in items['metric']['channel']:
				if int(channelTrend['id']) % mod == 0:
					resp['metric']['channel'].append(channelTrend)
		
		return resp
	return resp

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
	
	elif request.path == '/cmo/v1/metadata/getProgramTagName.json':
		mpi.getProgramTagName = load(open(os.path.join(json_url, 'mpi.getProgramTagName.json')))
	
	elif request.path == '/cmo/v1/metadata/getWorkspace.json':
		mpi.getWorkspace = load(open(os.path.join(json_url, 'mpi.getWorkspace.json')))
	
	elif request.path == '/cmo/v1/metadata/getAbmAccountList.json':
		mpi.getAbmAccountList = load(open(os.path.join(json_url, 'mpi.getAbmAccountList.json')))
	
	elif request.path == '/cmo/v1/metadata/getCustomAttributeName.json':
		mpi.getCustomAttributeName = load(open(os.path.join(json_url, 'mpi.getCustomAttributeName.json')))
	
	elif request.path == '/cmo/v1/metadata/getOpportunityType.json':
		mpi.getOpportunityType = load(open(os.path.join(json_url, 'mpi.getOpportunityType.json')))
	
	elif request.path == '/cmo/v1/metadata/getProgramTagValue.json':
		mpi.getProgramTagValue = load(open(os.path.join(json_url, 'mpi.getProgramTagValue.json')))
	
	elif request.path == '/cmo/v1/metadata/getCustomAttributeValue.json':
		mpi.getCustomAttributeValue = load(open(os.path.join(json_url, 'mpi.getCustomAttributeValue.json')))
	
	elif request.path == '/cmo/v1/metadata/quickcharts.json':
		mpi.quickcharts = load(open(os.path.join(json_url, 'mpi.quickcharts.json')))
	
	elif request.path == '/cmo/v1/metadata/export.json': # Returns static file for 'PPT Download'
		return send_file('static/export/mpi-revenue_won_to_cost_ratio_mt-previous_year.pptx')
	
	elif request.path == '/cmo/v1/export/getExcelData.json': # Returns static file for 'EXCEL Download'
		return send_file('static/export/mpi-revenue_won_to_cost_ratio_mt-previous_year.xlsx')

# Home Page
@app.route('/')
def home_page():
	return redirect('/mpi')

# MPI Page
@app.route('/mpi')
@app.route('/marketo-performance')
@app.route('/marketing-performance')
def mpi_page():
	# If provided, sets the program and/or channel names for the session
	program_names = request.args.get('programs')
	channel_names = request.args.get('channels')
	if program_names:
		session['programs'] = program_names
		session.modified = True
	elif 'programs' in session:
		session.pop('programs')
	if channel_names:
		session['channels'] = channel_names
		session.modified = True
	elif 'channels' in session:
		session.pop('channels')
	
	return render_template('mpi.html')

#MPI JSON Endpoints
@app.route('/cmo/v1/metadata/getChannel.json')
def mpi_getChannel():
	# Required query string parameters
	sidebar = request.args.get('sidebar')
	tab_name = request.args.get('tab_name')
	top_view_metrics = request.args.get('top_view_metrics')
	isAttribution = request.args.get('isAttribution')
	time_period = request.args.get('time_period')
	settings = request.args.get('settings')
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
	
	resp = filter_data('getChannel', filters, None, deepcopy(mpi.getChannel[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]))
	
	# Sets the first channel names shown using the provided names from the session
	if 'channels' in session and session['channels']:
		channel_names = session['channels'].split(',')
		for i, channel in enumerate(resp['channel']):
			if i < len(channel_names):
				channel['name'] = channel_names[i]
			else:
				break
	
	# Returns the data as JSON w/ 200 response and sets the Content-Type header
	return dumps(resp), None, json_resp_headers

@app.route('/cmo/v1/metadata/getProgramRank.json')
@app.route('/cmo/v1/metadata/getProgram.json')
def mpi_getProgramRank():
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
	
	resp = deepcopy(mpi.getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
	
	# User selected a set of channels to segment the data via post-filtering
	if channel_id:
		channel_id = loads(channel_id)
		resp['program'] = []
		
		for program in mpi.getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['program']:
			if program['channelId'] in channel_id:
				resp['program'].append(program)
	
	resp = filter_data('getProgramRank', filters, channel_id, resp)
	
	# User selected to sort the programs in ascending value so simply reverse the list of programs
	if mode == 'bottom':
		resp['program'].reverse()
	
	# Sets the first program names shown using the provided names from the session
	if 'programs' in session and session['programs']:
		program_names = session['programs'].split(',')
		for i, program in enumerate(resp['program']):
			if i < len(program_names):
				program['name'] = program_names[i]
			else:
				break
	
	# Returns the data as JSON w/ 200 response and sets the Content-Type header
	return dumps(resp), None, json_resp_headers

@app.route('/cmo/v1/metadata/getChannelTrend.json')
def mpi_getChannelTrend():
	# Required query string parameters
	sidebar = request.args.get('sidebar')
	tab_name = request.args.get('tab_name')
	top_view_metrics = request.args.get('top_view_metrics')
	isAttribution = request.args.get('isAttribution')
	time_period = request.args.get('time_period')
	mode = request.args.get('mode')
	settings = request.args.get('settings')
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
	
	resp = filter_data('getChannelTrend', filters, None, deepcopy(mpi.getChannelTrend[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]))
	
	# Returns the data as JSON w/ 200 response and sets the Content-Type header
	return dumps(resp), None, json_resp_headers

@app.route('/cmo/v1/metadata/getProgramTagName.json')
def mpi_getProgramTagName():
	# Required query string parameters
	page = request.args.get('page')
	
	# If page is 0 then returns all the data for the selected filter as JSON and otherwise simply returns the count of the filter values
	if page == '0':
		return dumps(mpi.getProgramTagName), None, json_resp_headers
	else:
		return dumps({'success': 'true', 'count': mpi.getProgramTagName['count']}), None, json_resp_headers

@app.route('/cmo/v1/metadata/getWorkspace.json')
def mpi_getWorkspace():
	page = request.args.get('page')
	if page == '0':
		return dumps(mpi.getWorkspace), None, json_resp_headers
	else:
		return dumps({'success': 'true', 'count': mpi.getWorkspace['count']}), None, json_resp_headers

@app.route('/cmo/v1/metadata/getAbmAccountList.json')
def mpi_getAbmAccountList():
	page = request.args.get('page')
	if page == '0':
		return dumps(mpi.getAbmAccountList), None, json_resp_headers
	else:
		return dumps({'success': 'true', 'count': mpi.getAbmAccountList['count']}), None, json_resp_headers

@app.route('/cmo/v1/metadata/getCustomAttributeName.json')
def mpi_getCustomAttributeName():
	page = request.args.get('page')
	if page == '0':
		return dumps(mpi.getCustomAttributeName), None, json_resp_headers
	else:
		return dumps({'success': 'true', 'count': mpi.getCustomAttributeName['count']}), None, json_resp_headers

@app.route('/cmo/v1/metadata/getOpportunityType.json')
def mpi_getOpportunityType():
	page = request.args.get('page')
	if page == '0':
		return dumps(mpi.getOpportunityType), None, json_resp_headers
	else:
		return dumps({'success': 'true', 'count': mpi.getOpportunityType['count']}), None, json_resp_headers

@app.route('/cmo/v1/metadata/getProgramTagValue.json')
def mpi_getProgramTagValue():
	name = request.args.get('name')
	page = request.args.get('page')
	if page == '0':
		return dumps(mpi.getProgramTagValue[name]), None, json_resp_headers
	else:
		return dumps({'success': 'true', 'count': mpi.getProgramTagValue[name]['count']}), None, json_resp_headers

@app.route('/cmo/v1/metadata/getCustomAttributeValue.json')
def mpi_getCustomAttributeValue():
	name = request.args.get('name')
	page = request.args.get('page')
	if page == '0':
		return dumps(mpi.getCustomAttributeValue[name]), None, json_resp_headers
	else:
		return dumps({'success': 'true', 'count': mpi.getCustomAttributeValue[name]['count']}), None, json_resp_headers

@app.route('/cmo/v1/metadata/quickcharts.json')
def mpi_quickcharts():
	return dumps(mpi.quickcharts), None, json_resp_headers

@app.route('/cmo/v1/metadata/getUser.json')
def mpi_getUser():
	return dumps({'munchkin_id':'000-AAA-000','customer_prefix':'mpi4marketolive','user_id':'mpi@marketolive.com'}), None, json_resp_headers

# Returns empty JSON for endpoint which deletes a Quick Chart
'''
@app.route('/cmo/v1/metadata/150.json', methods=['DELETE'])
def mpi_quickchartsDelete():
	return dumps({}), None, json_resp_headers
'''

# Email Insights Page
@app.route('/email')
@app.route('/email-insights')
def ei_page():
	return render_template('ei.html')

# Robots route set to disallow search engine indexing of all pages
@app.route('/robots.txt')
def robots():
	return app.send_static_file('export/robots.txt')

# Sets Cache-Control header based upon the Content-Type header
@app.after_request
def add_header(response):
	if search('^application/json;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 86400
	elif search('/?javascript;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 86400
	elif search('^text/(html|css);?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 86400
	elif search('^image/', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 86400
	else:
		response.cache_control.public = True
		response.cache_control.max_age = 86400
	return response