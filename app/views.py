from app import app
from flask import request, render_template, redirect
from re import search
from globals import *
import os, requests

# Global Vars
json_resp_headers = {
	'Content-Type': 'application/json; charset=UTF-8'
}

# Home Page
@app.route('/')
def home_page():
	return redirect('/mpi')

# MPI Page
@app.route('/mpi')
@app.route('/mpi/<jsonData>')
@app.route('/marketo-performance')
@app.route('/marketo-performance/<jsonData>')
@app.route('/marketing-performance')
@app.route('/marketing-performance/<jsonData>')
def mpi_page(jsonData):
	return render_template('mpi.html')

#MPI JSON Endpoints
@app.route('/mpi/metadata/getChannel.json')
@app.route('/mpi/metadata/getProgramRank.json')
@app.route('/mpi/metadata/getProgram.json')
@app.route('/mpi/metadata/getChannelTrend.json')
def mpi_getChannel():
	return mpi.get_data(request), None, json_resp_headers

@app.route('/mpi/metadata/getProgramTagName.json')
@app.route('/mpi/metadata/getWorkspace.json')
@app.route('/mpi/metadata/getAbmAccountList.json')
@app.route('/mpi/metadata/getCustomAttributeName.json')
@app.route('/mpi/metadata/getOpportunityType.json')
def mpi_get_filter_names():
	return mpi.get_filter_names(request), None, json_resp_headers

@app.route('/mpi/metadata/getProgramTagValue.json')
@app.route('/mpi/metadata/getCustomAttributeValue.json')
def mpi_get_filter_values():
	return mpi.get_filter_values(request), None, json_resp_headers

@app.route('/mpi/metadata/quickcharts.json')
def mpi_quickcharts():
	return mpi.quickcharts(request), None, json_resp_headers

@app.route('/mpi/metadata/getUser.json')
def mpi_getUser():
	return mpi.getUser(), None, json_resp_headers

@app.route('/mpi/metadata/export.json')
def mpi_export_ppt():
	return app.send_static_file('export/mpi-revenue_won_to_cost_ratio_mt-previous_year.pptx')

@app.route('/mpi/export/getExcelData.json')
def mpi_export_xls():
	return app.send_static_file('export/mpi-revenue_won_to_cost_ratio_mt-previous_year.xlsx')

# Endpoint which deletes a Quick Chart
'''
@app.route('/mpi/metadata/150.json', methods=['DELETE'])
def mpi_del_quickchart():
	return mpi.del_quickchart(), None, json_resp_headers
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