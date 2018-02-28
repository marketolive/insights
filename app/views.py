from app import app
from flask import request, render_template, send_file, redirect
from re import search
from json import load, loads, dumps
from random import randint, random
from copy import deepcopy
import os, requests

# Global Variables
static_url = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
mpi_getChannel = None
mpi_getProgramRank = None
mpi_getChannelTrend = None
mpi_filters = None
mpi_quickcharts = None
mpi_channel_ids = []

@app.before_request
def before_request():
	if (request.path in ['/mpi', '/marketo-performance', '/marketing-performance']):
		global mpi_getChannel, mpi_getProgramRank, mpi_getChannelTrend, mpi_filters, mpi_quickcharts
		mpi_getChannel = load(open(os.path.join(static_url, 'mpi.getChannel.json')))
		mpi_getProgramRank = load(open(os.path.join(static_url, 'mpi.getProgramRank.json')))
		mpi_getChannelTrend = load(open(os.path.join(static_url, 'mpi.getChannelTrend.json')))
		mpi_filters = load(open(os.path.join(static_url, 'mpi.filters.json')))
		mpi_quickcharts = load(open(os.path.join(static_url, 'mpi.quickcharts.json')))
	elif (request.path == '/cmo/v1/metadata/export.json'):
		return send_file('/static/export/mpi-revenue _won_to_cost_ratio_mt-previous_year.pptx')
	elif (request.path == '/cmo/v1/export/getExcelData.json'):
		return send_file('/static/export/mpi-revenue _won_to_cost_ratio_mt-previous_year.xlsx')

@app.route('/mpi')
@app.route('/marketo-performance')
@app.route('/marketing-performance')
def mpi_page():
	return render_template('mpi.html')

@app.route('/cmo/v1/metadata/<endpoint>.json')
def mpi_endpoint(endpoint):
	if (endpoint in ['getChannel', 'getProgramRank', 'getChannelTrend']):
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
		resp = {}
		
		if (not settings):
			settings = '{"Before Opportunity Created":[]}'
		elif (settings == '{"Before Opportunity Created":["Show First-Touch","Show Multi-Touch"]}'):
			if (search('{"First-Touch":', top_view_metrics)):
				settings = '{"Before Opportunity Created":["Show Multi-Touch"]}'
			elif (search('{"Multi-Touch":', top_view_metrics)):
				settings = '{"Before Opportunity Created":["Show First-Touch"]}'
			else:
				settings = '{"Before Opportunity Created":[]}'
		
		if (endpoint == 'getChannel'):
			resp = deepcopy(mpi_getChannel[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
		elif (endpoint == 'getProgramRank'):
			resp = deepcopy(mpi_getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
			if (channel_id):
				channel_id = loads(channel_id)
				resp['program'] = []
				for program in mpi_getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['program']:
					if (program['channelId'] in channel_id):
						resp['program'].append(program)
		
		elif (endpoint == 'getChannelTrend'):
			resp = deepcopy(mpi_getChannelTrend[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings])
		
		if (program_tag or workspace or abm_account_list or custom_attribute or investment_period or opportunity_type):
			filters = [program_tag, workspace, abm_account_list, custom_attribute, investment_period, opportunity_type]
			num_of_filters = sum(filter is not None for filter in filters)
			rand = 1
			for i in range(num_of_filters):
				rand *= (randint(33, 66) / 100)
			
			if (endpoint == 'getChannel'):
				global mpi_channel_ids
				resp['channel'] = []
				for channel in mpi_getChannel[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['channel']:
					if (random() <= rand):
						resp['channel'].append(channel)
				for channel in resp['channel']:
					mpi_channel_ids.append(channel['id'])
			elif (endpoint == 'getProgramRank'):
				resp['program'] = []
				for program in mpi_getProgramRank[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['program']:
					if (program['channelId'] in mpi_channel_ids):
						resp['program'].append(program)
					elif (not mpi_channel_ids and random() <= rand):
						resp['program'].append(program)
			elif (endpoint == 'getChannelTrend'):
				resp['metric']['channel'] = []
				for channelTrend in mpi_getChannelTrend[sidebar][tab_name][top_view_metrics][isAttribution][time_period][settings]['metric']['channel']:
					if (channelTrend['id'] in mpi_channel_ids):
						resp['metric']['channel'].append(program)
					elif (not mpi_channel_ids and random() <= rand):
						resp['metric']['channel'].append(program)
						
		if (mode == 'bottom'):
			resp['program'].reverse()
		
		return dumps(resp)
	elif (endpoint in ['getProgramTagName', 'getWorkspace', 'getAbmAccountList', 'getCustomAttributeName', 'getOpportunityType']):
		results_array = {
			'getProgramTagName': 'program_tag_name',
			'getWorkspace': 'workspace',
			'getAbmAccountList': 'abm_account_list',
			'getCustomAttributeName': 'custom_attribute_name',
			'getOpportunityType': 'opportunity_type'
		}
		page = request.args.get('page')
		resp = deepcopy(mpi_filters[endpoint])
		
		if (page == '0'):
			return dumps(resp)
		else:
			return dumps({'success': 'true', 'count': resp['count']})
	elif (endpoint in ['getProgramTagValue', 'getCustomAttributeValue']):
		results_array = {
			'getProgramTagValue': 'program_tag_value',
			'getCustomAttributeValue': 'custom_attribute_value'
		}
		name = request.args.get('name')
		page = request.args.get('page')
		resp = deepcopy(mpi_filters[endpoint][name])
		
		if (page == '0'):
			return dumps(resp)
		else:
			return dumps({'success': 'true', 'count': resp['count']})
	elif (endpoint == 'quickcharts'):
		resp = deepcopy(mpi_quickcharts)
		return dumps(resp)
	elif (endpoint == 'getUser'):
		return dumps({"munchkin_id":"000-AAA-000","customer_prefix":"mpi4marketolive","user_id":"mpi@marketolive.com"})
	elif (endpoint == '150'):
		return dumps({})

@app.route('/email')
@app.route('/email-insights')
def ei_page():
	return render_template('ei.html')