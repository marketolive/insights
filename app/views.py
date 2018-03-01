from app import app
from flask import request, session, render_template, send_file, redirect
from re import search
from json import load, loads, dumps
from random import randint, random
from copy import deepcopy
from globals import *
import os, requests

# Global Variables
base_url = os.path.abspath(os.path.dirname(__file__))
json_url = os.path.join(base_url, 'static/json')
json_resp_headers = {
	'Content-Type': 'application/json; charset=UTF-8'
}

@app.before_request
def before_request():
	if (search('(^/cmo/v1/metadata/|^/mpi$|^/marketo-performance$|^/marketing-performance$)', request.path)):
		if (request.path == '/cmo/v1/metadata/export.json'):
			return send_file('static/export/mpi-revenue_won_to_cost_ratio_mt-previous_year.pptx')
		else:
			mpi.getChannel = load(open(os.path.join(json_url, 'mpi.getChannel.json')))
			mpi.getProgramRank = load(open(os.path.join(json_url, 'mpi.getProgramRank.json')))
			mpi.getChannelTrend = load(open(os.path.join(json_url, 'mpi.getChannelTrend.json')))
			mpi.filters = load(open(os.path.join(json_url, 'mpi.filters.json')))
			mpi.quickcharts = load(open(os.path.join(json_url, 'mpi.quickcharts.json')))
	elif (request.path == '/cmo/v1/export/getExcelData.json'):
		return send_file('static/export/mpi-revenue_won_to_cost_ratio_mt-previous_year.xlsx')

@app.route('/mpi')
@app.route('/marketo-performance')
@app.route('/marketing-performance')
def mpi_page():
	return render_template('mpi.html')

@app.route('/cmo/v1/metadata/<endpoint>.json')
def mpi_endpoint(endpoint):
	if (endpoint in ['getChannel', 'getProgramRank', 'getChannelTrend', 'getProgram']):
		resp = None
		
		sidebar = request.args.get('sidebar')
		tab_name = request.args.get('tab_name')
		top_view_metrics = request.args.get('top_view_metrics')
		isAttribution = request.args.get('isAttribution')
		time_period = request.args.get('time_period')
		mode = request.args.get('mode')
		settings = request.args.get('settings')
		channel_id = request.args.get('channel_id')
		
		program_tag = request.args.get('program_tag')
		workspace = request.args.get('workspace')
		abm_account_list = request.args.get('abm_account_list')
		custom_attribute = request.args.get('custom_attribute')
		investment_period = request.args.get('investment_period')
		opportunity_type = request.args.get('opportunity_type')
		
		if (isAttribution not in mpi.isAttribution_dict[top_view_metrics]):
			isAttribution = 'false'
		
		if (time_period not in mpi.time_period_list):
			time_period = 'YTD'
		
		settings = mpi.settings_dict[top_view_metrics][settings]
		
		if (endpoint == 'getChannel'):
			resp = deepcopy(mpi.getChannel[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
		elif (endpoint in ['getProgramRank', 'getProgram']):
			resp = deepcopy(mpi.getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
			if (channel_id):
				channel_id = loads(channel_id)
				resp['program'] = []
				for program in mpi.getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['program']:
					if (program['channelId'] in channel_id):
						resp['program'].append(program)
		elif (endpoint == 'getChannelTrend'):
			resp = deepcopy(mpi.getChannelTrend[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
		
		if (program_tag or workspace or abm_account_list or custom_attribute or investment_period or opportunity_type):
			filters = [program_tag, workspace, abm_account_list, custom_attribute, investment_period, opportunity_type]
			num_of_filters = sum(filter is not None for filter in filters)
			rand = 1
			for i in range(num_of_filters):
				rand *= (randint(33, 66) / 100)
			
			if (endpoint == 'getChannel'):
				resp['channel'] = []
				session['channel_ids_filtered'] = []
				session.modified = True
				
				for channel in mpi.getChannel[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['channel']:
					if (random() <= rand):
						resp['channel'].append(channel)
						session['channel_ids_filtered'].append(channel['id'])
						print(session['channel_ids_filtered'])
			
			elif (endpoint == 'getProgramRank'):
				programs = None
				
				if (not channel_id):
					resp['program'] = []
					programs = mpi.getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['program']
				else:
					programs = deepcopy(resp['program'])
				
				for program in programs:
					if (program['channelId'] in session['channel_ids_filtered']):
						resp['program'].append(program)
					elif (not session['channel_ids_filtered'] and random() <= rand):
						resp['program'].append(program)
			
			elif (endpoint == 'getChannelTrend'):
				resp['metric']['channel'] = []
				for channelTrend in mpi.getChannelTrend[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['metric']['channel']:
					if (channelTrend['id'] in session['channel_ids_filtered']):
						resp['metric']['channel'].append(program)
					elif (not session['channel_ids_filtered'] and random() <= rand):
						resp['metric']['channel'].append(program)
			print('\n')
			print(session['channel_ids_filtered'])
			print('\n')
		else:
			session.pop('channel_ids_filtered', None)
		
		if (mode == 'bottom'):
			resp['program'].reverse()
		
		return dumps(resp), 200, json_resp_headers
	
	elif (endpoint in ['getProgramTagName', 'getWorkspace', 'getAbmAccountList', 'getCustomAttributeName', 'getOpportunityType']):
		results_array = {
			'getProgramTagName': 'program_tag_name',
			'getWorkspace': 'workspace',
			'getAbmAccountList': 'abm_account_list',
			'getCustomAttributeName': 'custom_attribute_name',
			'getOpportunityType': 'opportunity_type'
		}
		page = request.args.get('page')
		resp = deepcopy(mpi.filters[endpoint])
		
		if (page == '0'):
			return dumps(resp), 200, json_resp_headers
		else:
			return dumps({'success': 'true', 'count': resp['count']}), 200, json_resp_headers
	
	elif (endpoint in ['getProgramTagValue', 'getCustomAttributeValue']):
		results_array = {
			'getProgramTagValue': 'program_tag_value',
			'getCustomAttributeValue': 'custom_attribute_value'
		}
		name = request.args.get('name')
		page = request.args.get('page')
		resp = deepcopy(mpi.filters[endpoint][name])
		
		if (page == '0'):
			return dumps(resp), 200, json_resp_headers
		else:
			return dumps({'success': 'true', 'count': resp['count']}), 200, json_resp_headers
	
	elif (endpoint == 'quickcharts'):
		resp = deepcopy(mpi.quickcharts)
		return dumps(resp), 200, json_resp_headers
	
	elif (endpoint == 'getUser'):
		return dumps({"munchkin_id":"000-AAA-000","customer_prefix":"mpi4marketolive","user_id":"mpi@marketolive.com"}), 200, json_resp_headers
	
	elif (endpoint == '150'):
		return dumps({}), 200, json_resp_headers

@app.route('/email')
@app.route('/email-insights')
def ei_page():
	return render_template('ei.html')

@app.after_request
def add_header(response):
	if (search('^application/json;?', response.headers['Content-Type'])):
		response.headers['Cache-Control'] = 'public, max-age=28800'
	elif (search('/?javascript;?', response.headers['Content-Type'])):
		response.headers['Cache-Control'] = 'public, max-age=86400'
	elif (search('^text/(html|css);?', response.headers['Content-Type'])):
		response.headers['Cache-Control'] = 'public, max-age=86400'
	elif (search('^image/', response.headers['Content-Type'])):
		response.headers['Cache-Control'] = 'public, max-age=86400'
	else:
		response.headers['Cache-Control'] = 'public, max-age=86400'
	
	return response