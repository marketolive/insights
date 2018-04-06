from app import app
from flask import request, render_template, redirect
from re import search
import requests

# Global Vars
json_resp_headers = {
	'Content-Type': 'application/json; charset=UTF-8'
}

# Home Page
@app.route('/')
def home_page():
	return redirect('/mpi')

# MPI Home Page
@app.route('/mpi')
@app.route('/marketo-performance')
@app.route('/marketing-performance')
def mpi_default_page():
	return render_template('mpi.html')

# MPI Custom Page
@app.route('/mpi/<jsonData>')
@app.route('/marketo-performance/<jsonData>')
@app.route('/marketing-performance/<jsonData>')
def mpi_custom_page(jsonData):
	return render_template('mpi.html')

# MPI JSON Endpoints
@app.route('/mpi/metadata/getChannel.json')
@app.route('/mpi/metadata/getProgramRank.json')
@app.route('/mpi/metadata/getChannelTrend.json')
def mpi_getChannel():
	import app.packages.mpi as mpi
	return mpi.get_data(request), None, json_resp_headers

@app.route('/mpi/metadata/getProgram.json')
def mpi_getProgram():
	import app.packages.mpi as mpi
	return mpi.getProgram(request), None, json_resp_headers

@app.route('/mpi/metadata/getProgramTrend.json')
def mpi_getProgramTrend():
	import app.packages.mpi as mpi
	return mpi.getProgramTrend(request), None, json_resp_headers

@app.route('/mpi/metadata/getProgramTagName.json')
@app.route('/mpi/metadata/getWorkspace.json')
@app.route('/mpi/metadata/getAbmAccountList.json')
@app.route('/mpi/metadata/getCustomAttributeName.json')
@app.route('/mpi/metadata/getOpportunityType.json')
def mpi_get_filter_names():
	import app.packages.mpi as mpi
	return mpi.get_filter_names(request), None, json_resp_headers

@app.route('/mpi/metadata/getProgramTagValue.json')
@app.route('/mpi/metadata/getCustomAttributeValue.json')
def mpi_get_filter_values():
	import app.packages.mpi as mpi
	return mpi.get_filter_values(request), None, json_resp_headers

@app.route('/mpi/metadata/quickcharts.json')
def mpi_quickcharts():
	import app.packages.mpi as mpi
	return mpi.quickcharts(request), None, json_resp_headers

@app.route('/mpi/metadata/getUser.json')
def mpi_getUser():
	import app.packages.mpi as mpi
	return mpi.getUser(), None, json_resp_headers

@app.route('/mpi/metadata/export.json')
def mpi_export_ppt():
	return app.send_static_file('export/mpi.default.pptx')

@app.route('/mpi/export/getExcelData.json')
def mpi_export_xls():
	return app.send_static_file('export/mpi.default.xlsx')

# Endpoint which deletes a Quick Chart
'''
@app.route('/mpi/metadata/150.json', methods=['DELETE'])
def mpi_del_quickchart():
	import app.packages.mpi as mpi
	return mpi.del_quickchart(), None, json_resp_headers
'''


# Email Insights Home Page
@app.route('/email')
@app.route('/email-insights')
def ei_page():
	return render_template('ei.html')

# Email Insights JSON Endpoints
@app.route('/ei/metadata/dimensions.json')
@app.route('/ei/metadata/metrics.json')
@app.route('/ei/settings/user.json')
@app.route('/ei/analytics/kpis.json')
@app.route('/ei/settings/allfilters.json')
@app.route('/ei/settings/workspaces.json')
def ei_get_data_info():
	import app.packages.ei as ei
	return ei.get_data_info(request), None, json_resp_headers

@app.route('/ei/analytics/timeseries.json')
@app.route('/ei/analytics/breakdown.json')
def ei_analytics():
	import app.packages.ei as ei
	return ei.analytics(request), None, json_resp_headers

@app.route('/ei/analytics/drivers.json')
def ei_drivers():
	import app.packages.ei as ei
	return ei.drivers(request), None, json_resp_headers

@app.route('/ei/analytics/sends.json')
def ei_sends():
	import app.packages.ei as ei
	return ei.sends(request), None, json_resp_headers

@app.route('/ei/metadata/dimensions/<filter>/values.json')
def ei_filter_values(filter):
	import app.packages.ei as ei
	return ei.filter_values(request, filter), None, json_resp_headers

@app.route('/ei/metadata/quickcharts.json')
def ei_quickcharts():
	import app.packages.ei as ei
	return ei.quickcharts(request), None, json_resp_headers


# Robots route set to disallow search engine indexing of all pages
@app.route('/robots.txt')
def robots():
	return app.send_static_file('export/robots.txt')

# Sets Cache-Control header based upon the Content-Type header
@app.after_request
def add_header(response):
	if search('^text/html;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 300
	elif search('^application/json;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	elif search('/?javascript;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	elif search('^text/css;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	elif search('^image/', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	else:
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	return response