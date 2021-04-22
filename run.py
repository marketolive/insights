#!flask/bin/python

from debug import debug_based_on_env 
debug_based_on_env()

from app import app
app.run(host='0.0.0.0', debug=True)