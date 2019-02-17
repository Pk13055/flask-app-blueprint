from functools import wraps

# Import flask and template operators
from flask import Flask, render_template,session, blueprints,jsonify
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect,CSRFError


# Define the WSGI application object
app = Flask(__name__, static_url_path = '/static')

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# # For CAS we do
# # For Central Authentication
# from app.flask_cas import CAS
# from app.flask_cas import login_required
# CAS(app)
# app.config['CAS_SERVER'] = 'https://login.iiit.ac.in/cas/login'
# app.config['CAS_AFTER_LOGIN'] = 'https://www.google.co.in/'


# csrf protection
csrf=CSRFProtect(app)
@app.errorhandler(CSRFError)
def csrf_error(reason):
    # return jsonify(success=True,error=reason)
    return render_template('error.html.j2', error=reason), 400

# HTTP error handling route
@app.errorhandler(404)
def not_found(error):
	return render_template('error.html.j2', error=error) , 404

# authorization for the logged in state
# modify this according to your needs
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		# FIXME: change this part according to your login mechanism
		if 'user_uid' not in session:
			return jsonify(success=False, message="Unauthorized entry. Login First"), 400
		return f(*args, **kwargs)
	return decorated

# Import a module / component using its blueprint handler variable (mod_auth)
from app.home.controller import home

# Register blueprint(s)
app.register_blueprint(home)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

