import yaml
import project
import os
import subprocess
from flask import Flask

PROJECT = 'persist.yaml'
DATA = 'projects2.yaml'

def load():
        files = os.listdir()
        if DATA not in files:
                subprocess.call(['cp', 'data.empty', DATA])
        if PROJECT not in files:
                subprocess.call(['cp', 'project.empty', PROJECT])
        global data
        data = yaml.load(open(DATA))
        persist = yaml.load(open(PROJECT))
        project.CURRENT_ID = persist['project_id']

def save():
        persist = {'project_id': project.CURRENT_ID}
        project_out = open(PROJECT, 'w')
        data_out = open(DATA, 'w')
        project_out.write(yaml.dump(persist))
        data_out.write(yaml.dump(data))
        project_out.close()
        data_out.close()

app = Flask(__name__)
app.secret_key = b"\xc5S\xbe\xfa\xdf\xd5\x80I\xdfi\xa5[h\xda\xb8\xacb\xd2\xe2\x83Kc\x89]\xb2\xed\xbd\x8cc pM1(YC\x96\xf2Y+\xfd\x16\x99A\xc6\x80\xa2\x08\xe6\xa3\xfb\x17|\xf9\x82H\xb6\xb41\x8d\x13\x12B\xa6\xef\xab\xe7'8\x973\xec\x964jr4\xe5U\xf7\xe4|J\x88\xf3K\x96\xa2E6\x94\x85\x85\xc9\xf8\x07\xb0\xc3\xc1\xb4"
load()

def update():
        global data
        for proj in data.projects:
                proj.meta = 0
                proj.desc = ''
        for super in data.superprojects:
                proj = project.Project(super.name, id=super.id)
                proj.dependencies = super.projects
                proj.meta = 1
                data.projects.append(proj)
        del data.superprojects
        save()
