from flask import Flask, Response
from flask import render_template, request, redirect, url_for, abort, send_from_directory, jsonify
import json, yaml
import project
from server import app, load, save, data

@app.route('/')
def index():
        return send_from_directory('./', 'projects.html')
        # return send_from_directory('./main.html')

@app.route('/start')
def start():
        return json.dumps(data, cls=project.ProjectEncoder)

@app.route('/elements/<path:path>')
def elements(path):
        return send_from_directory('elements', path)


@app.route('/main.js')
def mainjs():
        return send_from_directory('./', 'main.js')
