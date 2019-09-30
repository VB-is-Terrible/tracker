from common import JSONable
import json
import project as Project
from patch_holder import PatchHolder
from server import save
from ChangeSet import ChangeSet


class System(JSONable):
	def __init__(self):
		self.projects = {}
		self.patches = PatchHolder()

	excludes = set(['patches'])
	includes = set(['version'])

	def json(self):
		result = super().json(self.excludes, self.includes)
		result['type'] = 'System'
		return result

	def get_event_by_id(self, id: int) -> Project.Project:
		return self.projects.get(id, None)

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
		response['version'] = self.version
		response['patches'] = patches
		return response

	def change_project_from_request(self, request):
		self.patches.create_patch()
		changeset_json = request.form['change']
		change_sets = json.loads(changeset_json)
		for change_set in change_sets:
			self.change_project(change_set)
		save()

	def change_project(self, change_set_obj):
		change_set = ChangeSet.fromJSONObj(change_set_obj, self)
		print('Got changeset: ')
		print(change_set)
		target = self.get_event_by_id(change_set.id)
		ChangeSet.validate_with_project(change_set, target)
		self._simple_changes(change_set)
		self.patches.current_patch.add_change(change_set)

	def _simple_changes(self, change_set: ChangeSet):
		target = self.get_event_by_id(change_set.id)
		if change_set.name is not None:
			target.name = change_set.name
		if change_set.desc is not None:
			target.desc = change_set.desc
		if change_set.meta is not None:
			target.meta = change_set.meta
		if change_set.name is not None:
			target.name = change_set.name



	@property
	def version(self):
		return self.patches.version
