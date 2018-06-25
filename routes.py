from flask import Flask, Response
from flask import render_template, request, redirect, url_for, abort, send_from_directory, jsonify
import json, yaml
import project
from server import app, load, save

@app.route('/')
def index():
        content = open('projects2.yaml').read()
        return Response(content, mimetype='text/html')
        return send_from_directory('./', 'projects2.yaml')
        # return send_from_directory('./main.html')

@app.route('/elements/<file>')
def elements(file):
        return send_from_directory('elements', path)
