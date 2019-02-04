from common import JSONable
import json
import project as Project
from patch_holder import PatchHolder
from server import save


class System(JSONable):
	def __init__(self):
		self.projects = {}
		self.patches = PatchHolder()

	excludes = set('patches')

	def json(self):
		result = super().json(self.excludes)
		result['type'] = 'System'
		return result

	def get_event_by_id(self, id):
		return self.projects[id]

	def add_project(self, project_obj):
		project = Project.Project.fromJSONObj(project_obj, self)
		self.projects[project.id] = project
		print('Saved project {}'.format(project.id))
		self.patches.current_patch.add_create(project)

	def add_project_from_request(self, request):
		self.patches.create_patch()
		projects_json = request.form['create']
		projects = json.loads(projects_json)
		for project in projects:
			self.add_project(project)
		save()

	def get_updates(self, foreign_version: int):
		patches = self.patches.get_patches(foreign_version)
		response = {}
		response['verison'] = self.version
		response['patches'] = patches
		return response

	@property
	def version(self):
		return self.patches.version
