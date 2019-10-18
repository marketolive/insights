from app import app
from flask import request, render_template, redirect
from app.packages import mpi, ei
import re

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
@app.route('/performance-insights')
def mpi_default_page():
	return render_template('mpi.html')

# MPI Program Page
@app.route('/program')
def program_default_page():
	return render_template('program.html')

# MPI Custom Page
@app.route('/mpi/<jsonData>')
@app.route('/performance-insights/<jsonData>')
def mpi_custom_page(jsonData):
	return render_template('mpi.html')

# MPI JSON Endpoints
@app.route('/mpi/metadata/getChannel.json')
@app.route('/mpi/metadata/getProgramRank.json')
@app.route('/mpi/metadata/getChannelTrend.json')
def mpi_getChannel():
	return mpi.get_data(request), None, json_resp_headers

@app.route('/mpi/metadata/getProgram.json')
def mpi_getProgram():
	return mpi.getProgram(request), None, json_resp_headers

@app.route('/mpi/metadata/getProgramTrend.json')
def mpi_getProgramTrend():
	return mpi.getProgramTrend(request), None, json_resp_headers

@app.route('/mpi/metadata/getProgramTagName.json')
@app.route('/mpi/metadata/getWorkspace.json')
@app.route('/mpi/metadata/getAbmAccountList.json')
@app.route('/mpi/metadata/getAbmAccountName.json')
@app.route('/mpi/metadata/getCustomAttributeName.json')
@app.route('/mpi/metadata/getOpportunityForecast.json')
@app.route('/mpi/metadata/getOpportunityOwner.json')
@app.route('/mpi/metadata/getOpportunityStage.json')
@app.route('/mpi/metadata/getOpportunityType.json')
@app.route('/mpi/metadata/getOpportunityField.json')
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

@app.route('/mpi/metadata/export.json', methods=['POST'])
def mpi_export_ppt():
	jsonData = request.args.get('jsonData') or 'default'
	return app.send_static_file('export/mpi.' + jsonData + '.pptx')

@app.route('/mpi/export/getExcel.json')
def mpi_export_xls():
	jsonData = request.args.get('jsonData') or 'default'
	return app.send_static_file('export/mpi.' + jsonData + '.xlsx')

# Endpoints which reorders and deletes a Quick Chart
@app.route('/mpi/metadata/quickcharts/<chart>.json', methods=['PUT', 'DELETE'])
def mpi_modify_quickchart(chart):
	return mpi.modify_quickchart(), None, json_resp_headers

# Endpoint which saves a Quick Chart
@app.route('/mpi/metadata/quickcharts.json', methods=['POST'])
def mpi_save_quickchart():
	return mpi.save_quickchart(request), None, json_resp_headers


# Email Insights Home Page
@app.route('/email')
@app.route('/email-insights')
def ei_page():
	return render_template('ei.html')

# Email Insights Custom Page
@app.route('/email/<jsonData>')
@app.route('/email-insights/<jsonData>')
def ei_custom_page(jsonData):
	return render_template('ei.html')

# Email Insights JSON Endpoints
@app.route('/ei/metadata/dimensions.json')
@app.route('/ei/metadata/metrics.json')
@app.route('/ei/settings/user.json')
@app.route('/ei/settings/allfilters.json')
@app.route('/ei/settings/workspaces.json')
@app.route('/ei/settings/dimensions/custom.json')
def ei_get_data_info():
	return ei.get_data_info(request), None, json_resp_headers

@app.route('/ei/analytics/kpis.json')
def ei_kpis():
	return ei.kpis(request), None, json_resp_headers

@app.route('/ei/analytics/timeseries.json')
@app.route('/ei/analytics/breakdown.json')
def ei_analytics():
	return ei.analytics(request), None, json_resp_headers

@app.route('/ei/analytics/drivers.json')
def ei_drivers():
	return ei.drivers(request), None, json_resp_headers

@app.route('/ei/analytics/sends.json')
def ei_sends():
	return ei.sends(request), None, json_resp_headers

@app.route('/ei/metadata/dimensions/<filter>/values.json')
def ei_filter_values(filter):
	return ei.filter_values(request, filter), None, json_resp_headers

@app.route('/ei/settings/filter.json', methods=['PUT'])
def ei_filters():
	return ei.filters(request), None, json_resp_headers

@app.route('/ei/metadata/quickcharts.json')
def ei_quickcharts():
	return ei.quickcharts(request), None, json_resp_headers

@app.route('/ei/metadata/export.json', methods=['POST'])
def ei_export_ppt():
	jsonData = request.args.get('jsonData') or 'default'
	return app.send_static_file('export/ei.' + jsonData + '.pptx')

# Endpoint which gets a saved Quick Chart
@app.route('/ei/metadata/quickcharts/<chart>.json', methods=['GET'])
def ei_get_quickchart(chart):
	return ei.get_quickchart(request), None, json_resp_headers

# Endpoints which reorders and deletes a Quick Chart
@app.route('/ei/metadata/quickcharts/<chart>.json', methods=['PUT', 'DELETE'])
def ei_modify_quickchart(chart):
	return ei.modify_quickchart(), None, json_resp_headers

# Endpoint which saves a Quick Chart
@app.route('/ei/metadata/quickcharts.json', methods=['POST'])
def ei_save_quickchart():
	return ei.save_quickchart(request), None, json_resp_headers

@app.route('/ei/settings/dimensions/activate/<dimension>.json', methods=['PUT'])
def ei_activate_dimension(dimension):
	return ei.activate_dimension(request, dimension), None, json_resp_headers

@app.route('/ei/user/logout')
def ei_logout():
	return redirect('https://sj-ee-api.marketo.com')


# Robots route set to disallow search engine indexing of all pages
@app.route('/robots.txt')
def robots():
	return app.send_static_file('export/robots.txt')

# Sets Cache-Control header based upon the Content-Type header
@app.after_request
def add_header(response):
	if re.search('^text/html;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 300
	elif re.search('^application/json;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	elif re.search('/?javascript;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	elif re.search('^text/css;?', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	elif re.search('^image/', response.headers['Content-Type']):
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	else:
		response.cache_control.public = True
		response.cache_control.max_age = 31536000
	return response