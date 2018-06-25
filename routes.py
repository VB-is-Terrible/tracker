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
        return json.dumps(data, cls=project.JSONEncoder())
        
@app.route('/elements/<file>')
def elements(file):
        return send_from_directory('elements', file)
