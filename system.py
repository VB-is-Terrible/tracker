from common import JSONable
import json
import project as Project
from patch import Patch

class System(JSONable):
	def __init__(self):
		self.projects = {}
		self.patch = Patch()

	excludes = set('patch')
	def json(self):
		result = super().json(self.excludes)
		result['type'] = 'System'
		return result

	def get_event_by_id(self, id):
		return self.projects[id]

	def add_project(self, project_obj):
		project = Project.Project.fromJSONObj(project_obj, self)
		self.projects[project.id] = project
		print ('Saved project {}'.format(project.id))
		self.patch.create.append(project)

	def add_project_from_request(self, request):
		projects_json = request.form['create']
		projects = json.loads(projects_json)
		for project in projects:
			self.add_project(project)

	def new_patch(self):
		patch = self.patch
		self.patch = Patch()
		return patch
