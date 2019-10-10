from common import JSONable
import json
import project as Project
from patch_holder import PatchHolder
from server import save
from ChangeSet import ChangeSet
from collections import deque
from typing import List


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
		self._cyclic_detection(change_set.id, change_set)
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

	def _complex_changes(self, change_set: ChangeSet):
		target = self.get_event_by_id(change_set.id)
		if change_set.counter is not None:
			target.counter = change_set.counter
		if change_set.progress is not None:
			target.progress = change_set.progress
		if change_set.required is not None:
			target.required = change_set.required
		# TODO: Cyclic detection
		for id in change_set.dependencies_remove:
			target.remove_dependency(id)
		for id in change_set.dependencies_add:
			target.add_dependency(id)

	def _update_status(self, project_id: int):
		changed_projects = []
		to_check = deque([project_id])
		while len(to_check) != 0:
			id = to_check.popleft()
			project = self.get_event_by_id(id)
			changed = project.update_status()
			if changed:
				changed_projects.append(id)
				to_check.extend(project.successors)
		self._add_update_changes(changed_projects)

	def _add_update_changes(self, changed_projects: List[int]):
		for project in changed_projects:
			changes = ChangeSet(project)
			changes.status = self.get_event_by_id(project).status
			self.patches.current_patch.add_change(changes)

	def _cyclic_detection(self, project_id: int, change_set: ChangeSet):
		pass

	@property
	def version(self):
		return self.patches.version
