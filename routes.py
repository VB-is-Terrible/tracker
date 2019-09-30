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
@app.route('/project/elements/<path:path>')
def elements(path):
        return send_from_directory('elements', path)


@app.route('/main.js')
def mainjs():
        return send_from_directory('./', 'main.js')


@app.route('/project/main.js')
def project_main():
        return send_from_directory('./', 'project_main.js')


@app.route('/project/<project_id>')
def project(project_id):
        print('Got request for {}'.format(project_id))
        return send_from_directory('./', 'project_full.html')


@app.route('/update', methods=['POST'])
def update():
        version = int(request.form['version'])
        return json.dumps(data.get_updates(version), cls=Project.ProjectEncoder)


@app.route('/change', methods=['POST'])
def change():
        data.change_project_from_request(request)
        version = int(request.form['version'])
        return json.dumps(data.get_updates(version), cls=Project.ProjectEncoder)
