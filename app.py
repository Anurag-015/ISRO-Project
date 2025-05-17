from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

from api.placement import placement_bp
from api.search import search_bp
from api.waste import waste_bp
from api.simulate import simulate_bp
from api.import_export import import_export_bp
from api.logs import logs_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(placement_bp, url_prefix='/api')
app.register_blueprint(search_bp, url_prefix='/api')
app.register_blueprint(waste_bp, url_prefix='/api')
app.register_blueprint(simulate_bp, url_prefix='/api')
app.register_blueprint(import_export_bp, url_prefix='/api')
app.register_blueprint(logs_bp, url_prefix='/api')

# Global data store (in-memory database)
app.config['CONTAINERS'] = []
app.config['ITEMS'] = []
app.config['LOGS'] = []
app.config['CURRENT_DATE'] = "2025-04-06"

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/activity')
def activity():
    return render_template('activity.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/waste')
def waste():
    return render_template('waste.html')

@app.route('/add_items')
def add_items():
    return render_template('add_items.html')

@app.route('/ZoneUtil')
def zone_util():
    return render_template('ZoneUtil.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
