import importlib

updaters = {}
LAST_VERSION = 6


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
		del data.patch
		patches = importlib.import_module('patch_holder')
		data.patches = patches.PatchHolder(0)
		persist['update_version'] = 3


updaters[2] = update2


def update3(persist, data):
	for project in data.projects.values():
		if project.required == 2:
			project.counter = False
		else:
			project.counter = True
	persist['update_version'] = 4


updaters[3] = update3


def update4(persist, data):
	for project in data.projects.values():
		project.required = int(project.required)
	persist['update_version'] = 5


updaters[4] = update4


def update5(persist, data):
	for patch in data.patches.patches.values():
		if hasattr(patch, 'update'):
			patch.change = patch.update
			del patch.update
	persist['update_version'] = 6


updaters[5] = update5


def update(persist, data):
	run = False
	old_version = None
	if persist['update_version'] != LAST_VERSION:
		run = True
		old_version = persist['update_version']
	while persist['update_version'] != LAST_VERSION:
		updaters[persist['update_version']](persist, data)
	if run:
		print('Updated from version {} to version {}'.format(old_version, persist['update_version']))
	return run
