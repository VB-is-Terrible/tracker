from flask import request, send_from_directory
import json
import project as Project
from server import app, data


@app.route('/')
def index():
        return send_from_directory('./', 'projects.html')
        # return send_from_directory('./main.html')


@app.route('/start')
def start():
        return json.dumps(data, cls=Project.ProjectEncoder)


@app.route('/create', methods=['POST'])
def project_create():
        data.add_project_from_request(request)
        version = int(request.form['version'])
        return json.dumps(data.get_updates(version), cls=Project.ProjectEncoder)


@app.route('/elements/<path:path>')
def elements(path):
        return send_from_directory('elements', path)


@app.route('/main.js')
def mainjs():
        return send_from_directory('./', 'main.js')
