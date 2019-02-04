import importlib

updaters = {}
LAST_VERSION = 3


def update0(project_persist, data):
	if project_persist['update_version'] == 0:
		projs = {}
		for proj in data.projects:
			projs[proj.id] = proj
			data.projects = projs
		project_persist['update_version'] = 1


updaters[0] = update0


def update1(persist, data):
	if persist['update_version'] == 1:
		patch = importlib.import_module('patch')
		data.patch = patch.Patch()
		persist['update_version'] = 2


updaters[1] = update1


def update2(persist, data):
	if persist['update_version'] == 2:
		data.version = 0
		del data.patch
		patches = importlib.import_module('patch_holder')
		data.patches = patches.PatchHolder(0)
		persist['update_version'] = 3


updaters[2] = update2


def update(persist, data):
	run = False
	if persist['update_version'] != LAST_VERSION:
		run = True
	while persist['update_version'] != LAST_VERSION:
		updaters[persist['update_version']](persist, data)
	return run
